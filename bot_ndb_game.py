# -*- coding: utf-8 -*-

import logging
from google.cloud import datastore
from bot_ndb_base import NDB_Base
import key
import json
from bot_ndb_base import transactional

import bot_ui as ux
from utility import escape_markdown
from random import shuffle
import parameters
import itertools

from bot_telegram import report_master

CLIENT = datastore.Client()
KIND = 'Game'

class NDB_Game(NDB_Base):

    def __init__(self, name=None, creator=None, entry=None, key=None):
        if entry or key:
            super().__init__(entry=entry, key=key)
            return
        self.entry = datastore.Entity(key=CLIENT.key(KIND),exclude_from_indexes=['variables'])
        self.entry.update(
            name = name,
            state = "INITIAL", # INITIAL, STARTED, ENDED, INTERRUPTED
            sub_state = "INITIAL:JUST_CREATED", #INITIAL:JUST_CREATED, INITIAL:WAITING_FOR_PLAYERS
            players_keys = [creator.key],
            number_players = -1,
            variables = json.dumps({})
        )
        self.put()

    def __str__(self):
        return "NDB_Game: {}".format(self.name)

    def __repr__(self):
        return self.__str__()

    def refresh(self):
        # from bot_telegram import report_master
        # log_str = 'Refreshing game {}'.format(self.get_name())
        # logging.debug(log_str)
        # report_master("🐛 {}".format(log_str))
        game = NDB_Game(key=self.key) #refreshing game from db
        self.entry = game.entry # copied refreshed copy into self

    def get_name(self):
        return escape_markdown(self.name)

    def set_number_of_players(self, num_players):
        self.sub_state = "INITIAL:WAITING_FOR_PLAYERS"
        self.number_players = num_players
        self.put()

    def get_player_at_index(self,i):
        from bot_ndb_user import NDB_User
        key = self.players_keys[i]
        return NDB_User(entry=CLIENT.get(key))

    def get_players(self):
        from bot_ndb_user import NDB_User
        players = [NDB_User(entry=CLIENT.get(k)) for k in self.players_keys]
        return players

    def get_variables(self):
        return json.loads(self.variables)

    def set_variables(self, var_dict):
        self.variables = json.dumps(var_dict, ensure_ascii=False)
        self.put()

    def available_seats(self):
        return self.number_players - len(self.players_keys)

    @transactional
    def add_player(self, user):            
        logging.debug('{} Entering transactional add_player'.format(user.get_name()))      
        if self.sub_state != "INITIAL:WAITING_FOR_PLAYERS":
            return False
        if self.available_seats==0:
            return False
        self.players_keys.append(user.key)
        self.put()
        user.set_current_game(self)
        logging.debug('{} Exiting transactional add_player'.format(user.get_name()))
        return True

    def setup(self):
        players = self.get_players()
        size = self.number_players  #used only locally  
        self.variables = json.dumps({
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
        })
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
        var_dict = self.get_variables()
        var_dict['HAND'] += 1
        self.set_variables(var_dict)

    def is_last_hand(self):
        var_dict = self.get_variables()
        hand = var_dict['HAND']
        return hand == self.number_players

    def get_current_hand_players_reader_writers(self):
        hand = self.get_var('HAND')
        players = self.get_players()
        reader = players[hand-1]
        writers = [p for p in players if p != reader]
        return hand, players, reader, writers

    def set_reader_text_beginning(self, text):
        var_dict = self.get_variables()
        var_dict['TEXT_BEGINNINGS'].append(text)
        self.set_variables(var_dict)

    def get_reader_text_beginning(self):
        var_dict = self.get_variables()
        return var_dict['TEXT_BEGINNINGS'][-1]

    def set_reader_text_info(self, text):
        var_dict = self.get_variables()
        var_dict['TEXT_INFO'].append(text)
        self.set_variables(var_dict)

    def get_reader_text_info(self):
        var_dict = self.get_variables()
        return var_dict['TEXT_INFO'][-1]

    def has_player_already_written_continuation(self, user):
        var_dict = self.get_variables()
        player_index = self.players_keys.index(user.key)
        hand_index = var_dict['HAND']-1
        players_continuations = var_dict['PLAYERS_CONTINUATIONS'][hand_index]
        return players_continuations[player_index] != ''

    @transactional
    def set_player_text_continuation_and_get_remaining(self, user, text):
        logging.debug('{} Entering transactional set_player_text_continuation_and_get_remaining'.format(user.get_name()))
        var_dict = self.get_variables()
        player_index = self.players_keys.index(user.key)
        names = var_dict['PLAYERS_NAMES']
        hand_index = var_dict['HAND']-1
        players_continuations = var_dict['PLAYERS_CONTINUATIONS'][hand_index]
        players_continuations[player_index] = text
        self.set_variables(var_dict)
        remaining_names = [names[i] for i,t in enumerate(players_continuations) if t=='']
        logging.debug('{} Exiting transactional set_player_text_continuation_and_get_remaining'.format(user.get_name()))
        return remaining_names
        
    def prepare_voting(self):
        var_dict = self.get_variables()
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
        self.set_variables(var_dict)

    def get_guessers_indexes(self):
        var_dict = self.get_variables()
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        continuation_correct_info = next(info for c,info in continuations_info.items() if info['correct'])
        return [i for i in continuation_correct_info['authors_indexes'] if i!=hand_index]

    # def get_correct_continuation_shuffled_index(self):
    #     var_dict = self.get_variables()
    #     hand_index = var_dict['HAND']-1
    #     continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
    #     correct_continuation_shuffled_index = next(info['shuffled_index'] for info in continuations_info.values() if info['correct'])
    #     return correct_continuation_shuffled_index

    def get_continuation_shuffled_index(self, author_index):
            var_dict = self.get_variables()
            hand_index = var_dict['HAND']-1
            continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
            author_shuffled_index = next(info['shuffled_index'] for info in continuations_info.values() if author_index in info['authors_indexes'])
            return author_shuffled_index

    def has_user_already_voted(self, user):
        user_index = self.players_keys.index(user.key)
        var_dict = self.get_variables()
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        return any(user_index in info['voted_by'] for info in continuations_info.values())

    def get_names_remaining_voters(self):
        var_dict = self.get_variables()
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        names = var_dict['PLAYERS_NAMES']        
        voted_by_list = [info['voted_by'] for info in continuations_info.values()] 
        voters_indexes = list(itertools.chain(*voted_by_list))
        exact_author_list = next(info['authors_indexes'] for info in continuations_info.values() if info['correct'])
        remaining_names = [n for i,n in enumerate(names) if i not in voters_indexes and i not in exact_author_list] 
        return remaining_names   

    @transactional
    def set_voted_indexes_and_points_and_get_remaining(self, user, voted_shuffled_index):
        logging.debug('{} Entering transactional set_voted_indexes_and_points_and_get_remaining'.format(user.get_name()))
        var_dict = self.get_variables()
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        user_index = self.players_keys.index(user.key)
        assert user_index != hand_index # reader doesn't receive points        
        names = var_dict['PLAYERS_NAMES']        
        voted_cont_info = next(info for c,info in continuations_info.items() if info['shuffled_index']==voted_shuffled_index)
        voted_cont_info['voted_by'].append(user_index)   
        voted_by_list = [info['voted_by'] for info in continuations_info.values()] 
        voters_indexes = list(itertools.chain(*voted_by_list))        
        # report_master("🐛 voters_indexes: {}".format(voters_indexes))
        exact_author_list = next(info['authors_indexes'] for info in continuations_info.values() if info['correct'])
        remaining_names = [n for i,n in enumerate(names) if i not in voters_indexes and i not in exact_author_list] 
        self.set_variables(var_dict)
        logging.debug('{} Exiting transactional set_voted_indexes_and_points_and_get_remaining'.format(user.get_name()))
        return remaining_names

    def get_hand_continuations_info(self):
        var_dict = self.get_variables()
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]        
        return continuations_info

    '''
    For each continuations (in shuffled order), 
    return the list of player names voting that continuation
    '''
    def get_shuffled_continuations_voters(self):
        var_dict = self.get_variables()
        hand_index = var_dict['HAND']-1
        players_names = var_dict['PLAYERS_NAMES']
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        shuf_cont_voters_names = []
        for cont_info in sorted(continuations_info.values(), key=lambda i: i['shuffled_index']):
            voeters_name = [n for i,n in enumerate(players_names) if i in cont_info['voted_by']]
            shuf_cont_voters_names.append(voeters_name)
        return shuf_cont_voters_names

    def get_shuffled_continuations(self):
        var_dict = self.get_variables()
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        shuffled_continuations = [k for k,v in sorted(continuations_info.items(), key=lambda kv: kv[1]['shuffled_index'])]
        return shuffled_continuations

    def get_continuations_authors_indexes(self, continuation):
        var_dict = self.get_variables()
        hand_index = var_dict['HAND']-1
        continuations_info = var_dict['CONTINUATIONS_INFO'][hand_index]
        authors_indexes = continuations_info[continuation]['authors_indexes']
        return authors_indexes

    def prepare_hand_poins(self):
        var_dict = self.get_variables()
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
        self.set_variables(var_dict)         


    def prepare_and_send_hand_point_img_data(self, players):
        # prepare hand points:
        self.prepare_hand_poins()            
        
        from render_leaderboard import get_image_data_from_points
        from bot_telegram import send_photo_from_data_multi
        var_dict = self.get_variables()
        hand_index = var_dict['HAND']-1
        hand_points = var_dict['HAND_POINTS'][hand_index]
        players_names = var_dict['PLAYERS_NAMES']
        img_data = get_image_data_from_points(players_names, hand_points)
        send_photo_from_data_multi(players, 'leaderboard_hand.png', img_data, sleep=True)

    def prepare_and_send_game_point_img_data(self, players, save=False):
        from render_leaderboard import get_image_data_from_points
        from bot_telegram import send_photo_from_data_multi
        var_dict = self.get_variables()
        points = var_dict['HAND_POINTS']
        players_names = var_dict['PLAYERS_NAMES']
        game_points = []
        for i in range(self.number_players):
            game_points.append(sum(hand_points[i] for hand_points in points))
        if save:
            var_dict['GAME_POINTS'] = game_points
            self.set_variables(var_dict)            
        img_data = get_image_data_from_points(players_names, game_points)
        send_photo_from_data_multi(players, 'leaderboard_hand.png', img_data, sleep=True)

    def get_winner_names(self):
        var_dict = self.get_variables()
        points = var_dict['HAND_POINTS']
        players_names = var_dict['PLAYERS_NAMES']
        players_total_points = [sum(hand_points[i] for hand_points in points) for i in range(self.number_players)]
        max_point = max(players_total_points)
        winner_names = [players_names[i] for i,p in enumerate(players_total_points) if p==max_point]
        var_dict['WINNERS'] = winner_names
        self.set_variables(var_dict)            
        return winner_names

    def set_var(self, var_name, var_value, put=True):
        var_dict = self.get_variables()
        var_dict[var_name] = var_value
        self.variables = json.dumps(var_dict)
        if put:
            self.put()

    def get_var(self, var_name):
        var_dict = self.get_variables()
        return var_dict.get(var_name,None)

def get_game_from_id(game_id):
    from utility import represents_int
    assert represents_int(game_id)
    key = CLIENT.key(KIND, game_id)
    entry = CLIENT.get(key)
    if entry:
        return NDB_Game(entry=entry)
    else:
        return None

def get_ongoing_game(name):
    query = CLIENT.query(kind=KIND)
    query.add_filter('name', '=', name)
    query.add_filter('state', '=', 'INITIAL')
    matched = list(query.fetch(1))
    if matched:
        return NDB_Game(entry=matched[0])
    else:
        return None

    #keys = list([entity.key for entity in query.fetch(limit=1)])

if __name__ == '__main__':
    #game = NDB_Game('test',4)
    print('test room available: {}'.format(get_ongoing_game('test')))
    print('test1 room available: {}'.format(get_ongoing_game('test1')))


