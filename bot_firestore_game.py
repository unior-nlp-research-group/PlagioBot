import key
import parameters
from bot_firestore_user import User

import logging
from utility import escape_markdown
from random import shuffle
import itertools

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
from google.cloud import firestore

from dataclasses import dataclass, field

# https://gitlab.com/futureprojects/firestore-model/blob/master/examples/main.py
import firestore_model
from firestore_model import Model

# Use the application default credentials
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred, {
#   'projectId': key.APP_NAME,
# })

# firestore_model.db = firestore.client()
firestore_model.db = firestore.Client()

@dataclass
class Game(Model):
    name: str
    creator_id: str
    state: str
    sub_state: str
    number_players: int
    players_id: list
    variables:dict = field(default_factory={}, init=False, repr=False, compare=False)

    @staticmethod
    def create_game(name, creator_id):
        game = Game.make(
            name = name,
            creator_id = creator_id,
            state = "INITIAL", # INITIAL, STARTED, ENDED, INTERRUPTED
            sub_state = "INITIAL:JUST_CREATED", #INITIAL:JUST_CREATED, INITIAL:WAITING_FOR_PLAYERS
            number_players = -1,
            players_id = [creator_id],
            save=True
        )
        return game

    def refresh(self):
        self.set(Game.get(self.id).to_dict())

    def get_name(self):
        return escape_markdown(self.name)

    def set_number_of_players(self, num_players):
        self.sub_state = "INITIAL:WAITING_FOR_PLAYERS"
        self.number_players = num_players
        self.save()

    def get_player_at_index(self,i):        
        p_id = self.players_id[i]
        return User.get(p_id)

    def get_players(self):
        players = [User.get(p_id) for p_id in self.players_id]
        return players

    def get_available_seats(self):
        return self.number_players - len(self.players_id)

    @firestore.transactional 
    def add_player(self, user):
        logging.debug('{} Entering transactional add_player'.format(user.get_name()))          
        self.refresh()
        if self.sub_state != "INITIAL:WAITING_FOR_PLAYERS":
            return False
        if self.get_available_seats==0:
            return False
        self.players_id.append(user.key)
        self.save()
        user.set_current_game(self)
        logging.debug('{} Exiting transactional add_player'.format(user.get_name()))          
        return True

    def setup(self):
        players = self.get_players()
        size = self.number_players  #used only locally  
        self.variables = {
            'PLAYERS_NAMES': [p.get_name() for p in players],
            'SPECIAL_RULES': '',
            'HAND': 0,
            'TEXT_BEGINNINGS': [],
            'TEXT_INFO':[],
            'PLAYERS_CONTINUATIONS': [['']*size for i in range(size)], # one per player in order of players
            'CONTINUATIONS_INFO': [{} for i in range(size)], 
                # for each continuation in key: 
                # {
                #     shuffled_index: int,
                #     authors: list(int) -> index of players writing that continuation
                #     correct: bool -> if correct continuation
                #     voted_by: list(int) -> indexes of players voting that continuation
                # }
            'HAND_POINTS': [[0]*size for i in range(size)],
            'GAME_POINTS': [],
            'WINNERS': []
        }
        self.state = 'STARTED'
        self.setup_next_hand()

    def just_created(self):
        return self.sub_state == 'INITIAL:JUST_CREATED'

    def get_creator_name(self):
        creator_name = self.get_var('PLAYERS_NAMES')[0]
        return escape_markdown(creator_name)

    def set_special_rules(self, rule):
        self.set_var('SPECIAL_RULES',rule)

    def get_special_rules(self):
        return self.get_var('SPECIAL_RULES')

    def setup_next_hand(self):
        var_dict = self.variables
        var_dict['HAND'] += 1
        self.variables = var_dict

    def is_last_hand(self):
        var_dict = self.variables
        hand = var_dict['HAND']
        return hand == self.number_players

    def get_current_hand_players_reader_writers(self):
        hand = self.get_var('HAND')
        players = self.get_players()
        reader = players[hand-1]
        writers = [p for p in players if p != reader]
        return hand, players, reader, writers

    def set_reader_text_beginning(self, text):
        var_dict = self.variables
        var_dict['TEXT_BEGINNINGS'].append(text)
        self.variables = var_dict

    def get_reader_text_beginning(self):
        var_dict = self.variables
        return var_dict['TEXT_BEGINNINGS'][-1]

    def set_reader_text_info(self, text):
        var_dict = self.variables
        var_dict['TEXT_INFO'].append(text)
        self.variables = var_dict

    def get_reader_text_info(self):
        var_dict = self.variables
        return var_dict['TEXT_INFO'][-1]

    def has_player_already_written_continuation(self, user):
        var_dict = self.variables
        player_index = self.players_id.index(user.key)
        hand_index = var_dict['HAND']-1
        players_continuations = var_dict['PLAYERS_CONTINUATIONS'][hand_index]
        return players_continuations[player_index] != ''

    @firestore.transactional
    @staticmethod 
    def set_player_text_continuation_and_get_remaining(self, user, text):
        logging.debug('{} Entering transactional set_player_text_continuation_and_get_remaining'.format(user.get_name()))          
        self.refresh()
        var_dict = self.variables
        player_index = self.players_id.index(user.key)
        names = var_dict['PLAYERS_NAMES']
        hand_index = var_dict['HAND']-1
        players_continuations = var_dict['PLAYERS_CONTINUATIONS'][hand_index]
        players_continuations[player_index] = text
        self.variables = var_dict
        remaining_names = [names[i] for i,t in enumerate(players_continuations) if t=='']
        self.save()
        logging.debug('{} Exiting transactional set_player_text_continuation_and_get_remaining'.format(user.get_name()))          
        return remaining_names
        
    def prepare_voting(self):
        var_dict = self.variables
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        players_continuations = var_dict['PLAYERS_CONTINUATIONS'][hand_index]
        players_continuations_unique = sorted(set(players_continuations))
        shuffled_indexes = list(range(len(players_continuations_unique)))
        shuffle(shuffled_indexes)
        for i,unique_cont in enumerate(players_continuations_unique):
            continuations_info[unique_cont] = {
                'shuffled_index': shuffled_indexes[i],
                'authors_indexes': [i for i,c in enumerate(players_continuations) if c == unique_cont],
                'correct': players_continuations[hand_index] == unique_cont,
                'voted_by': []
            }
        self.variables = var_dict

    def get_guessers_indexes(self):
        var_dict = self.variables
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        continuation_correct_info = next(info for c,info in continuations_info.items() if info['correct'])
        return [i for i in continuation_correct_info['authors_indexes'] if i!=hand_index]

    # def get_correct_continuation_shuffled_index(self):
    #     var_dict = self.variables
    #     hand_index = var_dict['HAND']-1
    #     continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
    #     correct_continuation_shuffled_index = next(info['shuffled_index'] for info in continuations_info.values() if info['correct'])
    #     return correct_continuation_shuffled_index

    def get_continuation_shuffled_index(self, author_index):
            var_dict = self.variables
            hand_index = var_dict['HAND']-1
            continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
            author_shuffled_index = next(info['shuffled_index'] for info in continuations_info.values() if author_index in info['authors_indexes'])
            return author_shuffled_index

    def has_user_already_voted(self, user):
        user_index = self.players_id.index(user.key)
        var_dict = self.variables
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        return any(user_index in info['voted_by'] for info in continuations_info.values())

    def get_names_remaining_voters(self):
        var_dict = self.variables
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        names = var_dict['PLAYERS_NAMES']        
        voted_by_list = [info['voted_by'] for info in continuations_info.values()] 
        voters_indexes = list(itertools.chain(*voted_by_list))
        exact_author_list = next(info['authors_indexes'] for info in continuations_info.values() if info['correct'])
        remaining_names = [n for i,n in enumerate(names) if i not in voters_indexes and i not in exact_author_list] 
        return remaining_names   

    @firestore.transactional
    def set_voted_indexes_and_points_and_get_remaining(self, user, voted_shuffled_index):
        logging.debug('{} Entering transactional set_voted_indexes_and_points_and_get_remaining'.format(user.get_name()))
        self.refresh()
        var_dict = self.variables
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        user_index = self.players_id.index(user.key)
        assert user_index != hand_index # reader doesn't receive points        
        names = var_dict['PLAYERS_NAMES']        
        voted_cont_info = next(info for c,info in continuations_info.items() if info['shuffled_index']==voted_shuffled_index)
        voted_cont_info['voted_by'].append(user_index)   
        voted_by_list = [info['voted_by'] for info in continuations_info.values()] 
        voters_indexes = list(itertools.chain(*voted_by_list))        
        # report_master("🐛 voters_indexes: {}".format(voters_indexes))
        exact_author_list = next(info['authors_indexes'] for info in continuations_info.values() if info['correct'])
        remaining_names = [n for i,n in enumerate(names) if i not in voters_indexes and i not in exact_author_list] 
        self.variables = var_dict
        logging.debug('{} Exiting transactional set_voted_indexes_and_points_and_get_remaining'.format(user.get_name()))
        return remaining_names

    def get_hand_continuations_info(self):
        var_dict = self.variables
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]        
        return continuations_info

    '''
    For each continuations (in shuffled order), 
    return the list of player names voting that continuation
    '''
    def get_shuffled_continuations_voters(self):
        var_dict = self.variables
        hand_index = var_dict['HAND']-1
        players_names = var_dict['PLAYERS_NAMES']
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        shuf_cont_voters_names = []
        for cont_info in sorted(continuations_info.values(), key=lambda i: i['shuffled_index']):
            voeters_name = [n for i,n in enumerate(players_names) if i in cont_info['voted_by']]
            shuf_cont_voters_names.append(voeters_name)
        return shuf_cont_voters_names

    def get_shuffled_continuations(self):
        var_dict = self.variables
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        shuffled_continuations = [k for k,v in sorted(continuations_info.items(), key=lambda kv: kv[1]['shuffled_index'])]
        return shuffled_continuations

    def get_continuations_authors_indexes(self, continuation):
        var_dict = self.variables
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        authors_indexes = continuations_info[continuation]['authors_indexes']
        return authors_indexes

    def prepare_hand_poins(self):
        var_dict = self.variables
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        continuation_correct_info = next(info for c,info in continuations_info.items() if info['correct'])
        hand_points = var_dict['HAND_POINTS'][hand_index]
        for i in range(self.number_players):
            if i==hand_index:
                continue # reader doesn't give/receive points
            cont_i_info = next(info for info in continuations_info.values() if i in info['authors_indexes'])
            cont_voted_info = next((info for info in continuations_info.values() if i in info['voted_by']),None)
            if cont_i_info['correct']:
                hand_points[i] += parameters.POINTS_FOR_EXACT_GUESSING
            if i in continuation_correct_info['voted_by']:
                hand_points[i] += parameters.POINTS_FOR_CORRECT_VOTING
            if cont_voted_info and not cont_voted_info['correct']: # give points only if continuation is not the exact one (reader)
                for j in cont_voted_info['authors_indexes']:
                    hand_points[j] += parameters.POINTS_FOR_BEING_VOTED
        self.variables = var_dict         


    def prepare_and_send_hand_point_img_data(self, players):
        # prepare hand points:
        self.prepare_hand_poins()            
        
        from render_leaderboard import get_image_data_from_points
        from bot_telegram import send_photo_from_data_multi
        var_dict = self.variables
        hand_index = var_dict['HAND']-1
        hand_points = var_dict['HAND_POINTS'][hand_index]
        players_names = var_dict['PLAYERS_NAMES']
        img_data = get_image_data_from_points(players_names, hand_points)
        send_photo_from_data_multi(players, 'leaderboard_hand.png', img_data, sleep=True)

    def prepare_and_send_game_point_img_data(self, players, save=False):
        from render_leaderboard import get_image_data_from_points
        from bot_telegram import send_photo_from_data_multi
        var_dict = self.variables
        points = var_dict['HAND_POINTS']
        players_names = var_dict['PLAYERS_NAMES']
        game_points = []
        for i in range(self.number_players):
            game_points.append(sum(hand_points[i] for hand_points in points))
        if save:
            var_dict['GAME_POINTS'] = game_points
            self.variables = var_dict            
        img_data = get_image_data_from_points(players_names, game_points)
        send_photo_from_data_multi(players, 'leaderboard_hand.png', img_data, sleep=True)

    def get_winner_names(self):
        var_dict = self.variables
        points = var_dict['HAND_POINTS']
        players_names = var_dict['PLAYERS_NAMES']
        players_total_points = [sum(hand_points[i] for hand_points in points) for i in range(self.number_players)]
        max_point = max(players_total_points)
        winner_names = [players_names[i] for i,p in enumerate(players_total_points) if p==max_point]
        var_dict['WINNERS'] = winner_names
        self.variables = var_dict            
        return winner_names

    def set_var(self, var_name, var_value, save=True):
        var_dict = self.variables
        var_dict[var_name] = var_value
        self.variables = var_dict
        if save: self.save()

    def get_var(self, var_name):
        var_dict = self.variables
        return var_dict.get(var_name,None)

    @staticmethod
    def get_ongoing_game(name):
        games = Game.query([
            ('name', '=', name), 
            ('state', '=', 'INITIAL')
        ]).get()
        if games:
            return next(games)
        return None