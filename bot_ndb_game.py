# -*- coding: utf-8 -*-

import logging
from google.cloud import datastore
from bot_ndb_base import NDB_Base
import key
import json

import bot_ui as ux
from utility import escape_markdown

CLIENT = datastore.Client()
KIND = 'Game'

class NDB_Game(NDB_Base):

    def __init__(self, name=None, creator=None, entry=None): 
        if entry:
            self.entry = entry
            return                
        self.entry = datastore.Entity(key=CLIENT.key(KIND))
        self.entry.update(
            name = name,
            state = "INITIAL", # INITIAL, STARTED, ENDED, INTERRUPTED
            players_keys = [creator.key],
            number_players = -1,
            variables = json.dumps({})
        )
        self.put()             

    def get_name(self):
        return escape_markdown(self.name)

    def set_number_of_players(self, num_players):
        self.number_players = num_players
        self.put() 

    def get_player_index(self,i):
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
        self.variables = json.dumps(var_dict)
        self.put()

    def available_seats(self):
        return self.number_players - len(self.players_keys)

    def add_player(self, user):
        if self.state != "INITIAL":
            return False
        if self.available_seats==0:
            return False
        self.players_keys.append(user.key)        
        self.put()
        user.set_current_game(self)
        return True

    def setup(self):
        from random import shuffle
        players = self.get_players()
        size = self.number_players
        shuffles = [ list(range(size)) for i in range(size) ]
        for x in shuffles:
            shuffle(x)
        self.variables = json.dumps({
            'PLAYERS_NAMES': [p.get_name() for p in players],
            'SPECIAL_RULES': '',
            'HAND': 0,
            'TEXT_BEGINNINGS': [],
            'TEXT_CONTINUATIONS': [['']*size for i in range(size)],
            'SHUFFLE_INDEXES': shuffles,
            'VOTES': [[0]*size for i in range(size)],
            'POINTS': [[0]*size for i in range(size)],
        })
        self.state = 'STARTED'        
        self.setup_next_hand()   

    def get_game_creator_name(self):
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

    def set_player_text_continuation_and_get_remaining(self, user, text):
        var_dict = self.get_variables()
        player_index = self.players_keys.index(user.key)
        names = var_dict['PLAYERS_NAMES']
        hand_index = var_dict['HAND']-1
        hand_continuations = var_dict['TEXT_CONTINUATIONS'][hand_index]
        hand_continuations[player_index] = text
        self.set_variables(var_dict)
        remaining_names = [names[i] for i,t in enumerate(hand_continuations) if t=='']
        return remaining_names

    def get_players_shuffled_indexes_and_continuations(self):
        var_dict = self.get_variables()
        hand_index = var_dict['HAND']-1
        hand_continuations = var_dict['TEXT_CONTINUATIONS'][hand_index]
        shuffled_indexes = var_dict['SHUFFLE_INDEXES'][hand_index]
        shuffled_continuations = [hand_continuations[i] for i in shuffled_indexes]
        return shuffled_indexes, shuffled_continuations

    def set_voted_index_and_points_and_get_remaining(self, user, voted_index):        
        var_dict = self.get_variables()
        hand_index = var_dict['HAND']-1
        names = var_dict['PLAYERS_NAMES']
        user_index = self.players_keys.index(user.key)
        hand_votes = var_dict['VOTES'][hand_index]
        hand_points = var_dict['POINTS'][hand_index]
        hand_votes[user_index] = voted_index
        if user_index != hand_index: # reader doesn't receive points
            if voted_index == hand_index:
                hand_points[user_index] += 1
            else:
                hand_points[voted_index] += 1
        self.set_variables(var_dict)
        remaining_names = [names[i] for i,t in enumerate(hand_votes) if t==-1 and i!=hand_index]
        return remaining_names

    def get_shuffled_continuations_voters_name(self):
        var_dict = self.get_variables()
        hand_index = var_dict['HAND']-1        
        shuffled_indexes = var_dict['SHUFFLE_INDEXES'][hand_index]
        hand_votes = var_dict['VOTES'][hand_index]
        shuffled_continuations_voters_name = [[] for i in range(self.number_players)]
        players_names = var_dict['PLAYERS_NAMES']
        for i in range(self.number_players):
            if i == hand_index:
                continue
            voted_index_by_player_i = hand_votes[i]
            shuffled_voted_index_by_player_i = shuffled_indexes.index(voted_index_by_player_i)
            shuffled_continuations_voters_name[shuffled_voted_index_by_player_i].append(players_names[i])
        return shuffled_continuations_voters_name

    def get_hand_point_summary(self):
        var_dict = self.get_variables()
        hand_index = var_dict['HAND']-1 
        hand_points = var_dict['POINTS'][hand_index]
        players_names = var_dict['PLAYERS_NAMES']
        return '\n'.join(['- {}: {}'.format(players_names[i], hand_points[i]) for i in range(self.number_players)])

    def get_game_point_summary(self):
        var_dict = self.get_variables()
        points = var_dict['POINTS']
        players_names = var_dict['PLAYERS_NAMES']
        string_list = []        
        for i in range(self.number_players):
            total_points = sum(hand_points[i] for hand_points in points)
            string_list.append('- {}: {}'.format(players_names[i], total_points))
        return '\n'.join(string_list)

    def get_winner_names(self):
        var_dict = self.get_variables()
        points = var_dict['POINTS']
        players_names = var_dict['PLAYERS_NAMES']
        max_point = max(points)        
        winner_names = [players_names[i] for i,p in enumerate(points) if p==max_point]
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
    

