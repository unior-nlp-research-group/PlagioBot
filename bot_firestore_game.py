import key
import parameters
from utility import escape_markdown, get_milliseconds

import json
import logging
from random import shuffle
import itertools

# https://firebase.google.com/docs/firestore/manage-data/add-data
from google.cloud import firestore
# google/cloud/firestore_v1beta1/transaction

from dataclasses import dataclass, field
from typing import List, Dict, Any

# https://gitlab.com/futureprojects/firestore-model/blob/master/examples/main.py
import firestore_model
from firestore_model import Model

db = firestore.Client()


@dataclass
class Game(Model):
    name: str
    creator_id: str
    players_id: List
    state: str = "INITIAL" # INITIAL, STARTED, ENDED, INTERRUPTED
    sub_state: str = "INITIAL:JUST_CREATED" #INITIAL:JUST_CREATED, INITIAL:WAITING_FOR_PLAYERS    
    max_number_players: int = -1
    num_players: int = -1
    variables: Dict = field(default_factory=dict)

    @staticmethod
    def create_game(name, creator_id):
        game = Game.make(
            name = name,
            creator_id = creator_id,
            players_id = [creator_id],            
        )
        game.id = '{}_{}'.format(game.name, game.created)
        game.save()
        return game

    @staticmethod
    def get_game(name, timestamp):
        id_str = "{}_{}".format(name, timestamp)
        return Game.get(id_str)

    def refresh(self):
        self.copy_from_dict(Game.get(self.id).to_dict())

    def get_name(self):
        return escape_markdown(self.name)

    def set_max_number_of_players(self, num_players):
        self.sub_state = "INITIAL:WAITING_FOR_PLAYERS"
        self.max_number_players = num_players
        self.save()

    def get_player_at_index(self,i):  
        from bot_firestore_user import User      
        p_id = self.players_id[i]
        return User.get(p_id)

    def get_players(self):
        from bot_firestore_user import User
        players = [User.get(p_id) for p_id in self.players_id]
        return players

    def get_available_seats(self):
        return self.max_number_players - len(self.players_id)

    def set_state(self, state, sub_state=None, save=True):
        self.state = state
        self.sub_state = sub_state
        if save: self.save()

    def reset_variables(self, save=True):
        self.variables = {}
        if save: self.save()
    
    def set_var(self, var_name, var_value, save=True):
        self.variables[var_name] = var_value
        if save: self.save()

    def get_var(self, var_name):
        return self.variables.get(var_name,None)

    # --------------------------
    # TRANSACTIONAL OPERATION
    # --------------------------
    def add_player(self, user): 

        @firestore.transactional 
        def update_in_transaction(transaction): 
            logging.debug('{} Entering transactional add_player'.format(user.get_name()))                      
            self.refresh_from_transaction(transaction)
            if self.sub_state != "INITIAL:WAITING_FOR_PLAYERS":
                return False
            if self.get_available_seats==0:
                return False
            self.players_id.append(user.id)
            self.save_transactional(transaction)            
            user.set_current_game(self)  
            logging.debug('{} Exiting transactional add_player'.format(user.get_name()))                      
            return True
        
        result = update_in_transaction(db.transaction())        
        return result


    def setup(self):
        players = self.get_players()
        self.num_players = num_hands = len(self.players_id)
        self.state = 'STARTED'
        self.variables = {
            'PLAYERS_NAMES': [p.get_name() for p in players],
            'SPECIAL_RULES': '',
            'HAND': 1,
            'TEXT_BEGINNINGS': [],
            'TEXT_INFO':[],
            'PLAYERS_CONTINUATIONS': [{} for i in range(num_hands)], # one per player in order of players
            'CONTINUATIONS_INFO': [{} for i in range(num_hands)], 
                # for each continuation in key: 
                # {
                #     shuffled_index: int,
                #     authors: list(int) -> index of players writing that continuation
                #     correct: bool -> if correct continuation
                #     voted_by: list(int) -> indexes of players voting that continuation
                # }
            'HAND_POINTS': [{str(i):0 for i in range(num_hands)} for i in range(num_hands)], 
            'GAME_POINTS': [],
            'WINNERS_NAMES': []
        }
        self.save()

    def just_created(self):
        return self.sub_state == 'INITIAL:JUST_CREATED'

    def get_creator_name(self):
        creator_name = self.variables['PLAYERS_NAMES'][0]
        return escape_markdown(creator_name)

    def setup_next_hand(self, save=True):
        self.variables['HAND'] += 1
        if save: self.save()

    def is_last_hand(self):
        return self.variables['HAND'] == self.num_players

    def get_current_hand_players_reader_writers(self):
        hand = self.variables['HAND']
        players = self.get_players()
        reader = players[hand-1]
        writers = [p for p in players if p != reader]
        return hand, players, reader, writers

    def set_reader_text_beginning(self, text, save=True):        
        self.variables['TEXT_BEGINNINGS'].append(text)
        if save: self.save()

    def get_reader_text_beginning(self):        
        return self.variables['TEXT_BEGINNINGS'][-1]

    def set_reader_text_info(self, text, save=True):        
        self.variables['TEXT_INFO'].append(text)
        if save: self.save()

    def get_reader_text_info(self):        
        return self.variables['TEXT_INFO'][-1]

    def has_player_already_written_continuation(self, user):        
        player_index = self.players_id.index(user.id)
        hand_index = self.variables['HAND']-1
        current_players_continuations = self.variables['PLAYERS_CONTINUATIONS'][hand_index]
        return str(player_index) in current_players_continuations

    #--------------------------
    # TRANSACTIONAL OPERATION
    #--------------------------
    def set_player_text_continuation_and_get_remaining(self, user, text): 

        @firestore.transactional 
        def update_in_transaction(transaction): 
            logging.debug('{} Entering transactional set_player_text_continuation_and_get_remaining'.format(user.get_name()))                      
            self.refresh_from_transaction(transaction)
            player_index = self.players_id.index(user.id)
            names = self.variables['PLAYERS_NAMES']
            hand_index = self.variables['HAND']-1
            current_players_continuations = self.variables['PLAYERS_CONTINUATIONS'][hand_index]
            current_players_continuations[str(player_index)] = text
            remaining_names = [names[i] for i in range(self.num_players) if str(i) not in current_players_continuations]            
            self.save_transactional(transaction)            
            logging.debug('{} Exiting transactional set_player_text_continuation_and_get_remaining'.format(user.get_name()))          
            return remaining_names
        
        result = update_in_transaction(db.transaction())
        self.refresh()
        return result

    def prepare_voting(self):        
        hand_index = self.variables['HAND']-1
        continuations_info = self.variables['CONTINUATIONS_INFO'][hand_index]
        current_players_continuations = self.variables['PLAYERS_CONTINUATIONS'][hand_index]
        players_continuations_unique = sorted(set(current_players_continuations.values()))
        shuffled_indexes = list(range(len(players_continuations_unique)))
        shuffle(shuffled_indexes)
        original_continuation = current_players_continuations[str(hand_index)]
        for i,unique_cont in enumerate(players_continuations_unique):
            continuations_info[unique_cont] = {
                'shuffled_index': shuffled_indexes[i],
                'authors_indexes': [
                    int(str_i) for str_i,c in current_players_continuations.items()
                    if c == unique_cont
                ],
                'correct': unique_cont == original_continuation,
                'voted_by': []
            }
        self.save()

    def get_guessers_indexes(self):        
        hand_index = self.variables['HAND']-1
        continuations_info = self.variables['CONTINUATIONS_INFO'][hand_index]
        continuation_correct_info = next(info for c,info in continuations_info.items() if info['correct'])
        return [i for i in continuation_correct_info['authors_indexes'] if i!=hand_index]

    def get_continuation_shuffled_index(self, author_index):            
        hand_index = self.variables['HAND']-1
        continuations_info = self.variables['CONTINUATIONS_INFO'][hand_index]
        author_shuffled_index = next(
            info['shuffled_index'] 
            for info in continuations_info.values() 
            if author_index in info['authors_indexes']
        )
        return author_shuffled_index

    def has_user_already_voted(self, user):
        player_index = self.players_id.index(user.id)        
        hand_index = self.variables['HAND']-1
        continuations_info = self.variables['CONTINUATIONS_INFO'][hand_index]
        return any(player_index in info['voted_by'] for info in continuations_info.values())

    def get_names_remaining_voters(self):        
        hand_index = self.variables['HAND']-1
        continuations_info = self.variables['CONTINUATIONS_INFO'][hand_index]
        names = self.variables['PLAYERS_NAMES']        
        voted_by_list = [info['voted_by'] for info in continuations_info.values()] 
        voters_indexes = list(itertools.chain(*voted_by_list))
        exact_author_list = next(info['authors_indexes'] for info in continuations_info.values() if info['correct'])
        remaining_names = [n for i,n in enumerate(names) if i not in voters_indexes and i not in exact_author_list] 
        return remaining_names   

    #--------------------------
    # TRANSACTIONAL OPERATION
    #--------------------------
    def set_voted_indexes_and_points_and_get_remaining(self, user, voted_shuffled_index): 

        @firestore.transactional 
        def update_in_transaction(transaction): 
            logging.debug('{} Entering transactional set_voted_indexes_and_points_and_get_remaining'.format(user.get_name()))
            self.refresh_from_transaction(transaction)
            names = self.variables['PLAYERS_NAMES']
            hand_index = self.variables['HAND']-1
            continuations_info = self.variables['CONTINUATIONS_INFO'][hand_index]
            player_index = self.players_id.index(user.id)
            assert player_index != hand_index # reader doesn't receive points        
            names = self.variables['PLAYERS_NAMES']        
            voted_cont_info = next(info for c,info in continuations_info.items() if info['shuffled_index']==voted_shuffled_index)
            voted_cont_info['voted_by'].append(player_index)   
            voted_by_list = [info['voted_by'] for info in continuations_info.values()] 
            voters_indexes = list(itertools.chain(*voted_by_list))        
            exact_author_list = next(info['authors_indexes'] for info in continuations_info.values() if info['correct'])
            remaining_names = [n for i,n in enumerate(names) if i not in voters_indexes and i not in exact_author_list] 
            self.save_transactional(transaction)            
            logging.debug('{} Exiting transactional set_voted_indexes_and_points_and_get_remaining'.format(user.get_name()))
            return remaining_names
        
        result = update_in_transaction(db.transaction())
        self.refresh()
        return result

    def get_hand_continuations_info(self):
        
        hand_index = self.variables['HAND']-1
        continuations_info = self.variables['CONTINUATIONS_INFO'][hand_index]        
        return continuations_info

    '''
    For each continuations (in shuffled order), 
    return the list of player names voting that continuation
    '''
    def get_shuffled_continuations_voters(self):
        
        hand_index = self.variables['HAND']-1
        players_names = self.variables['PLAYERS_NAMES']
        continuations_info = self.variables['CONTINUATIONS_INFO'][hand_index]
        shuf_cont_voters_names = []
        for cont_info in sorted(continuations_info.values(), key=lambda i: i['shuffled_index']):
            voeters_name = [n for i,n in enumerate(players_names) if i in cont_info['voted_by']]
            shuf_cont_voters_names.append(voeters_name)
        return shuf_cont_voters_names

    def get_shuffled_continuations(self):
        
        hand_index = self.variables['HAND']-1
        continuations_info = self.variables['CONTINUATIONS_INFO'][hand_index]
        shuffled_continuations = [k for k,v in sorted(continuations_info.items(), key=lambda kv: kv[1]['shuffled_index'])]
        return shuffled_continuations

    def get_continuations_authors_indexes(self, continuation):
        
        hand_index = self.variables['HAND']-1
        continuations_info = self.variables['CONTINUATIONS_INFO'][hand_index]
        authors_indexes = continuations_info[continuation]['authors_indexes']
        return authors_indexes

    def prepare_hand_poins(self):
        
        hand_index = self.variables['HAND']-1
        continuations_info = self.variables['CONTINUATIONS_INFO'][hand_index]
        continuation_correct_info = next(info for c,info in continuations_info.items() if info['correct'])
        current_hand_points = self.variables['HAND_POINTS'][hand_index]
        for i in range(self.num_players):
            if i==hand_index:
                continue # reader doesn't give/receive points
            cont_i_info = next(info for info in continuations_info.values() if i in info['authors_indexes'])
            cont_voted_info = next((info for info in continuations_info.values() if i in info['voted_by']),None)            
            if cont_i_info['correct']:
                current_hand_points[str(i)] += parameters.POINTS_FOR_EXACT_GUESSING
            if i in continuation_correct_info['voted_by']:
                current_hand_points[str(i)] += parameters.POINTS_FOR_CORRECT_VOTING
            if cont_voted_info and not cont_voted_info['correct']: # give points only if continuation is not the exact one (reader)
                for j in cont_voted_info['authors_indexes']:
                    current_hand_points[str(j)] += parameters.POINTS_FOR_BEING_VOTED
        self.save()


    def prepare_and_send_hand_point_img_data(self, players):
        # prepare hand points:
        self.prepare_hand_poins()            
        
        from render_leaderboard import get_image_data_from_points
        from bot_telegram import send_photo_from_data_multi
        
        hand_index = self.variables['HAND']-1
        current_hand_points = self.variables['HAND_POINTS'][hand_index]
        players_names = self.variables['PLAYERS_NAMES']
        current_hand_points_list = [current_hand_points[str(i)] for i in range(self.num_players)]
        img_data = get_image_data_from_points(players_names, current_hand_points_list)
        send_photo_from_data_multi(players, 'leaderboard_hand.png', img_data, sleep=True)

    def prepare_and_send_game_point_img_data(self, players, save=False):
        from render_leaderboard import get_image_data_from_points
        from bot_telegram import send_photo_from_data_multi
        
        points = self.variables['HAND_POINTS']
        players_names = self.variables['PLAYERS_NAMES']
        self.variables['GAME_POINTS'] = [
            sum(current_hand_points[str(i)] for current_hand_points in points) 
            for i in range(self.num_players)
        ]
        if save:            
            self.save()
        img_data = get_image_data_from_points(players_names, self.variables['GAME_POINTS'])
        send_photo_from_data_multi(players, 'leaderboard_hand.png', img_data, sleep=True)

    def get_winner_names(self):        
        players_names = self.variables['PLAYERS_NAMES']
        max_point = max(self.variables['GAME_POINTS'])
        winner_names = [players_names[i] for i,p in enumerate(self.variables['GAME_POINTS']) if p==max_point]
        self.variables['WINNERS_NAMES'] = winner_names
        self.save()
        return winner_names

    @staticmethod
    def get_ongoing_game(name):
        games_generator = Game.query([
            ('name', '==', name), 
            ('state', '==', 'INITIAL')
        ]).get()
        try:
            return next(games_generator)
        except StopIteration:
            return None


if __name__ == "__main__":
    # from bot_firestore_user import User
    # user = User.create_user('test', '123', 'name', 'username', 'it')
    # game = Game.create_game('test','creator_0000')
    # game.set_state('INITIAL','INITIAL:WAITING_FOR_PLAYERS')
    # game.add_player(user)
    # print(game)
    game = Game.get_game('TEST','1555590090748')
    game.prepare_voting()

