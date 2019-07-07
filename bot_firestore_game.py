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
    sub_state: str = None # players states
    game_type: str = 'CONTINUATION' # 'CONTINUATION', 'FILL'
    game_control: str = 'DEFAULT' # 'DEFAULT', 'TEACHER', 'DEMO'
    game_reward_mode: str = 'CREATIVITY' # 'CREATIVITY' 'EXACTNESS'    
    special_rules: str = ''
    num_hands: int = 5
    players_names: List = None                
    num_players: int = -1
    announced: bool = False
    ask_text_info: bool = False
    translate_help: bool = False
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

    def set_announced(self, value, save=True):
        self.announced = value
        if save: self.save()
    
    def set_translate_help(self, value, save=True):
        self.translate_help = value
        if save: self.save()

    def set_game_type(self, t, save=True):
        assert t in ['CONTINUATION', 'FILL']
        self.game_type = t
        if save: self.save()
    
    def set_game_reward_mode(self, m, save=True):
        assert m in ['CREATIVITY', 'EXACTNESS']
        self.game_reward_mode = m
        if save: self.save()

    def set_game_control(self, m, save=True):
        assert m in ['DEFAULT', 'TEACHER', 'DEMO']
        self.game_control = m
        if save: self.save()

    def set_num_hands(self, h, save=True):
        self.num_hands = h
        if save: self.save()

    def set_special_rules(self, rules, save=True):
        self.special_rules = rules
        if save: self.save()

    def set_ask_text_info(self, v, save=True):
        self.ask_text_info = v
        if save: self.save()

    @staticmethod
    def get_game(name, timestamp):
        id_str = "{}_{}".format(name, timestamp)
        return Game.get(id_str)

    def refresh(self):
        self.copy_from_dict(Game.get(self.id).to_dict())

    def get_name(self):
        return escape_markdown(self.name)

    def get_player_at_index(self,i):  
        from bot_firestore_user import User      
        p_id = self.players_id[i]
        return User.get(p_id)

    def get_players(self):
        from bot_firestore_user import User
        players = [User.get(p_id) for p_id in self.players_id]
        return players

    def set_state(self, state, save=True):
        self.state = state
        if save: self.save()
    
    def set_sub_state(self, sub_state, save=True):
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
            if self.state != "INITIAL":
                return False
            self.players_id.append(user.id)
            self.save_transactional(transaction)            
            user.set_current_game(self)  
            logging.debug('{} Exiting transactional add_player'.format(user.get_name()))                      
            return True
        
        result = update_in_transaction(db.transaction())        
        return result

    # --------------------------
    # TRANSACTIONAL OPERATION
    # --------------------------
    def setup(self, user):

        @firestore.transactional 
        def update_in_transaction(transaction): 
            logging.debug('{} Entering transactional stop_new_players'.format(user.get_name()))                      
            self.refresh_from_transaction(transaction)
            if self.state != 'INITIAL':
                return False
            players = self.get_players()
            self.num_players = len(self.players_id)
            if self.game_control == 'DEFAULT':
                self.num_hands = self.num_players
                # otherwise set manually            
            self.players_names = [p.get_name() for p in players]
            self.variables = {
                'HAND': 1,
                'INCOMPLETE_TEXTS': [],
                'INCOMPLETE_TEXT_INFO':[],
                'PLAYERS_COMPLETIONS': [{} for i in range(self.num_hands)], # for each hand, one per player in order of players
                'COMPLETION_INFO': [{} for i in range(self.num_hands)], 
                    # COMPLETION (STRING) in key:  (UPPER CASE)
                    # mapping to value:
                    # {
                    #     'shuffled_index': int,
                    #     'authors': list(int) -> index of players writing that completion
                    #     'correct': bool -> if correct completion
                    #     'voted_by': list(int) -> indexes of players voting that completion
                    # }
                'HAND_POINTS': [{str(i):0 for i in range(self.num_players)} for i in range(self.num_hands)], 
                'GAME_POINTS': [],
                'WINNERS_NAMES': []
            }
            self.set_state('STARTED',save=False)
            self.save_transactional(transaction)            
            logging.debug('{} Exiting transactional add_player'.format(user.get_name()))                      
            return True

        return update_in_transaction(db.transaction())

    def get_creator_name(self):
        creator_name = self.players_names[0]
        return escape_markdown(creator_name)

    def setup_next_hand(self, save=True):
        self.variables['HAND'] += 1
        if save: self.save()

    def is_last_hand(self):
        return self.variables['HAND'] == self.num_hands

    def get_reader_index(self):
        if self.game_control == 'TEACHER':
            return 0
        return self.variables['HAND'] - 1

    def get_hand_number(self):
        return self.variables['HAND']

    def get_current_hand_players_reader_writers(self):
        players = self.get_players()
        reader = players[self.get_reader_index()]
        writers = [p for p in players if p != reader]
        return players, reader, writers

    def set_current_incomplete_text(self, text, save=True):        
        self.variables['INCOMPLETE_TEXTS'].append(text)
        if save: self.save()

    def get_current_incomplete_text(self):        
        return self.variables['INCOMPLETE_TEXTS'][-1]

    def get_reader_completion(self):        
        reader_index = self.get_reader_index()
        hand_index = self.variables['HAND']-1
        current_players_completions = self.variables['PLAYERS_COMPLETIONS'][hand_index]
        return current_players_completions[str(reader_index)]
        

    def get_incomplete_text_pre_post_gap(self):        
        incomplete_text = self.get_current_incomplete_text()
        gap_string = '???'
        gap_index = incomplete_text.index(gap_string)
        pre_gap = incomplete_text[:gap_index]
        post_gap = incomplete_text[gap_index+len(gap_string):]
        return pre_gap, post_gap

    def set_incomplete_text_info(self, text, save=True):        
        self.variables['INCOMPLETE_TEXT_INFO'].append(text)
        if save: self.save()

    def get_incomplete_text_info(self):  
        if self.ask_text_info:      
            return self.variables['INCOMPLETE_TEXT_INFO'][-1]
        return None

    def has_player_already_written_completion(self, user):        
        player_index = self.players_id.index(user.id)
        hand_index = self.variables['HAND']-1
        current_players_completions = self.variables['PLAYERS_COMPLETIONS'][hand_index]
        return str(player_index) in current_players_completions

    #--------------------------
    # TRANSACTIONAL OPERATION
    #--------------------------
    def set_player_text_completion_and_get_remaining(self, user, text): 

        @firestore.transactional 
        def update_in_transaction(transaction): 
            logging.debug('{} Entering transactional set_player_text_completion_and_get_remaining'.format(user.get_name()))                      
            self.refresh_from_transaction(transaction)
            player_index = self.players_id.index(user.id)
            names = self.players_names
            hand_index = self.variables['HAND']-1
            current_players_completions = self.variables['PLAYERS_COMPLETIONS'][hand_index]
            current_players_completions[str(player_index)] = text
            remaining_names = [names[i] for i in range(self.num_players) if str(i) not in current_players_completions]            
            self.save_transactional(transaction)            
            logging.debug('{} Exiting transactional set_player_text_completion_and_get_remaining'.format(user.get_name()))          
            return remaining_names
        
        result = update_in_transaction(db.transaction())
        self.refresh()
        return result

    def prepare_voting(self):        
        hand_index = self.variables['HAND']-1
        completions_info = self.variables['COMPLETION_INFO'][hand_index]
        current_players_completions_upper = [ # upper in order of player index
            c.upper() 
            for i,c in sorted(
                self.variables['PLAYERS_COMPLETIONS'][hand_index].items(), 
                key=lambda ic: int(ic[0])
            )
        ]
        players_completions_unique_upper = sorted(set(current_players_completions_upper))
        shuffled_indexes = list(range(len(players_completions_unique_upper)))
        shuffle(shuffled_indexes)
        original_completion_upper = current_players_completions_upper[self.get_reader_index()]
        for i,unique_cont in enumerate(players_completions_unique_upper):
            completions_info[unique_cont] = {
                'shuffled_index': shuffled_indexes[i],
                'authors_indexes': [
                    i for i,c in enumerate(current_players_completions_upper)
                    if c == unique_cont
                ],
                'correct': unique_cont == original_completion_upper,
                'voted_by': []
            }
        self.save()

    def get_guessers_indexes(self):        
        hand_index = self.variables['HAND']-1
        completions_info = self.variables['COMPLETION_INFO'][hand_index]
        completion_correct_info = next(info for c,info in completions_info.items() if info['correct'])
        return [i for i in completion_correct_info['authors_indexes'] if i!=self.get_reader_index()]

    def get_completion_shuffled_index(self, author_index):            
        hand_index = self.variables['HAND']-1
        completions_info = self.variables['COMPLETION_INFO'][hand_index]
        author_shuffled_index = next(
            info['shuffled_index'] 
            for info in completions_info.values() 
            if author_index in info['authors_indexes']
        )
        return author_shuffled_index

    def has_user_already_voted(self, user):
        player_index = self.players_id.index(user.id)        
        hand_index = self.variables['HAND']-1
        completions_info = self.variables['COMPLETION_INFO'][hand_index]
        return any(player_index in info['voted_by'] for info in completions_info.values())

    def get_names_remaining_voters(self):        
        hand_index = self.variables['HAND']-1
        completions_info = self.variables['COMPLETION_INFO'][hand_index]
        names = self.players_names        
        voted_by_list = [info['voted_by'] for info in completions_info.values()] 
        voters_indexes = list(itertools.chain(*voted_by_list))
        exact_author_list = next(info['authors_indexes'] for info in completions_info.values() if info['correct'])
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
            names = self.players_names
            hand_index = self.variables['HAND']-1
            completions_info = self.variables['COMPLETION_INFO'][hand_index]
            player_index = self.players_id.index(user.id)
            assert player_index != self.get_reader_index() # reader doesn't receive points        
            names = self.players_names        
            voted_cont_info = next(info for c,info in completions_info.items() if info['shuffled_index']==voted_shuffled_index)
            voted_cont_info['voted_by'].append(player_index)   
            voted_by_list = [info['voted_by'] for info in completions_info.values()] 
            voters_indexes = list(itertools.chain(*voted_by_list))        
            exact_author_list = next(info['authors_indexes'] for info in completions_info.values() if info['correct'])
            remaining_names = [n for i,n in enumerate(names) if i not in voters_indexes and i not in exact_author_list] 
            self.save_transactional(transaction)            
            logging.debug('{} Exiting transactional set_voted_indexes_and_points_and_get_remaining'.format(user.get_name()))
            return remaining_names
        
        result = update_in_transaction(db.transaction())
        self.refresh()
        return result

    def get_hand_completions_info(self):        
        hand_index = self.variables['HAND']-1
        completions_info = self.variables['COMPLETION_INFO'][hand_index]        
        return completions_info

    '''
    For each completions (in shuffled order), 
    return the list of player names voting that completion
    '''
    def get_shuffled_completions_voters(self):        
        hand_index = self.variables['HAND']-1
        players_names = self.players_names
        completions_info = self.variables['COMPLETION_INFO'][hand_index]
        shuf_cont_voters_names = []
        for cont_info in sorted(completions_info.values(), key=lambda i: i['shuffled_index']):
            voeters_name = [n for i,n in enumerate(players_names) if i in cont_info['voted_by']]
            shuf_cont_voters_names.append(voeters_name)
        return shuf_cont_voters_names

    def get_shuffled_completions(self):        
        hand_index = self.variables['HAND']-1
        completions_info = self.variables['COMPLETION_INFO'][hand_index]
        shuffled_completions = [k for k,v in sorted(completions_info.items(), key=lambda kv: kv[1]['shuffled_index'])]
        return shuffled_completions

    def get_completions_authors_indexes(self, completion):        
        hand_index = self.variables['HAND']-1
        completions_info = self.variables['COMPLETION_INFO'][hand_index]
        authors_indexes = completions_info[completion]['authors_indexes']
        return authors_indexes

    def prepare_hand_poins(self):        
        hand_index = self.variables['HAND']-1
        completions_info = self.variables['COMPLETION_INFO'][hand_index]
        completion_correct_info = next(info for c,info in completions_info.items() if info['correct'])
        current_hand_points = self.variables['HAND_POINTS'][hand_index]
        reader_index = self.get_reader_index()
        for i in range(self.num_players):
            if i==reader_index:
                continue # reader doesn't give/receive points
            cont_i_info = next(info for info in completions_info.values() if i in info['authors_indexes'])
            cont_voted_info = next((info for info in completions_info.values() if i in info['voted_by']),None)            
            if cont_i_info['correct']:
                current_hand_points[str(i)] += parameters.POINTS[self.game_reward_mode]['EXACT_GUESSING']
            if i in completion_correct_info['voted_by']:
                current_hand_points[str(i)] += parameters.POINTS[self.game_reward_mode]['CORRECT_VOTING']
            if cont_voted_info and not cont_voted_info['correct']: 
                # give points only if completion is not the exact one (reader)
                for j in cont_voted_info['authors_indexes']:
                    current_hand_points[str(j)] += parameters.POINTS[self.game_reward_mode]['POINTS_PER_RECEIVED_VOTE']
        self.save()


    def prepare_and_send_hand_point_img_data(self, players):
        # prepare hand_index points:
        self.prepare_hand_poins()            
        
        from render_leaderboard import get_image_data_from_points
        from bot_telegram import send_photo_from_data_multi
        
        hand_index = self.variables['HAND']-1
        current_hand_points = self.variables['HAND_POINTS'][hand_index]
        players_names = list(self.players_names)
        current_hand_points_list = [current_hand_points[str(i)] for i in range(self.num_players)]
        if self.game_control == 'TEACHER':
            del(players_names[0])
            del(current_hand_points_list[0])
        img_data = get_image_data_from_points(players_names, current_hand_points_list)
        send_photo_from_data_multi(players, 'leaderboard_hand.png', img_data, sleep=True)

    def prepare_and_send_game_point_img_data(self, players, save=False):
        from render_leaderboard import get_image_data_from_points
        from bot_telegram import send_photo_from_data_multi
        
        points = self.variables['HAND_POINTS']
        players_names = list(self.players_names)
        self.variables['GAME_POINTS'] = game_points = [
            sum(current_hand_points[str(i)] for current_hand_points in points) 
            for i in range(self.num_players)
        ]
        if self.game_control == 'TEACHER':
            del(players_names[0])
            del(game_points[0])
        if save:            
            self.save()
        img_data = get_image_data_from_points(players_names, self.variables['GAME_POINTS'])
        send_photo_from_data_multi(players, 'leaderboard_hand.png', img_data, sleep=True)

    def get_winner_names(self):        
        players_names = self.players_names
        max_point = max(self.variables['GAME_POINTS'])
        winner_names = [players_names[i] for i,p in enumerate(self.variables['GAME_POINTS']) if p==max_point]
        self.variables['WINNERS_NAMES'] = winner_names
        self.save()
        return winner_names

    @staticmethod
    def get_game_in_initial_state(name):
        games_generator = Game.query([
            ('name', '==', name), 
            ('state', '==', 'INITIAL')
        ]).get()
        try:
            return next(games_generator)
        except StopIteration:
            return None

    @staticmethod
    def get_game_in_started_state(name):
        games_generator = Game.query([
            ('name', '==', name), 
            ('state', '==', 'STARTED')
        ]).get()
        try:
            return next(games_generator)
        except StopIteration:
            return None

    @staticmethod
    def get_game_state_stats():
        for s in ['INITIAL', 'STARTED', 'ENDED', 'INTERRUPTED']:
            count = len(list(Game.query([('state', '==', s)]).get()))
            print("{}:{}".format(s, count))

if __name__ == "__main__":
    pass
