import key
import parameters
from utility import escape_markdown, get_milliseconds

import json
import logging
from random import shuffle
import itertools
import parameters
import copy

from dataclasses import dataclass, field
from typing import List, Dict, Any

from firestore_model import Model, transactional

@dataclass
class Game(Model):
    name: str
    creator_id: str
    language: str
    players_id: List    
    state: str = "INITIAL" # INITIAL, STARTED, ENDED, INTERRUPTED    
    game_type: str = 'CONTINUATION' # 'CONTINUATION', 'FILL', 'SYNONYM'
    game_control: str = 'DEFAULT' # 'DEFAULT', 'TEACHER'
    num_hands: int = parameters.NUM_HANDS_IN_TEACHER_MODE
    players_names: List = None                
    num_players: int = -1
    announced: bool = False
    translate_help: bool = False    
    variables: Dict = field(default_factory=dict)

    @staticmethod
    def create_game(name, user):
        game = Game.make(
            name = name,
            creator_id = user.id,
            players_id = [user.id],   
            language = user.language
        )
        game.id = '{}_{}'.format(game.name, game.created)        
        game.save()
        return game

    @staticmethod
    def get_game(name, timestamp):
        id_str = "{}_{}".format(name, timestamp)
        return Game.get(id_str)

    def get_player_at_index(self,i):  
        from bot_firestore_user import User      
        p_id = self.players_id[i]
        return User.get(p_id)

    def get_players(self):
        from bot_firestore_user import User
        players = [User.get(p_id) for p_id in self.players_id]
        return players
    
    def reset_variables(self, save=True):
        self.variables = {}
        if save: self.save()
    
    def set_var(self, var_name, var_value, save=True):
        self.variables[var_name] = var_value
        if save: self.save()

    def get_var(self, var_name, init_value=None):
        if var_name in self.variables:
            return self.variables[var_name]
        self.variables[var_name] = init_value
        return init_value

    def is_voting_no_or_multiple_answers_allowed(self):
        return self.game_type == 'SYNONYM'

    def teacher_validation_enabled(self):
        return self.game_control == 'TEACHER' and self.game_type == 'SYNONYM'

    ##########################################
    # START of TRANSACTIONAL FUNCTIONS
    ##########################################

    @transactional
    def set_announced(self, value):
        self.announced = value

    @transactional
    def set_translate_help(self, value):
        self.translate_help = value

    @transactional
    def set_game_type(self, t):
        assert t in ['CONTINUATION', 'FILL', 'SYNONYM']
        self.game_type = t
    
    @transactional
    def set_game_control(self, m):
        assert m in ['DEFAULT', 'TEACHER']
        self.game_control = m

    @transactional
    def set_num_hands(self, h):
        self.num_hands = h

    @transactional
    def set_state(self, state):
        self.state = state

    @transactional
    def add_player(self, user): 
        if self.state != "INITIAL":
            return False
        self.players_id.append(user.id)            
        user.set_current_game(self)  
        return True

    @transactional
    def setup(self, user):
        if self.state != 'INITIAL':
            return False
        players = self.get_players()
        self.num_players = len(self.players_id)
        if self.game_control == 'DEFAULT':
            self.num_hands = self.num_players
            # otherwise set it manually
        self.players_names = [p.get_name() for p in players]
        self.variables = {
            'HAND': 0, # 1 for the first hand
            'COMPLETED_HANDS': [False for _ in range(self.num_hands)], # weather each hand has been completed
            'CONFIRMED_CURRENT_HAND': [False for _ in range(self.num_players)], # weather each player has confirmed answer in current hand
            'SELECTED_CURRENT_HAND': [False for _ in range(self.num_players)], # weather each player has made a selection in current hand
            'INCOMPLETE_TEXTS': ['' for _ in range(self.num_hands)],
            'ORIGINAL_COMPLETION': ['' for _ in range(self.num_hands)], # original completion from reader
            'PLAYERS_ANSWERS': [{} for _ in range(self.num_hands)], # one dict per hand
                # str(player_index) in key mapping to its answer
                # we use str in keys because of firebase constraints
            'ANSWERS_INFO': [{} for _ in range(self.num_hands)], # one dict per hand
                # ANSWER (STRING) in key  (UPPER CASE)
                # mapping to dictionary:
                # {
                #     'answer': str, --> repetition of the key (for convenience)    
                #     'shuffled_number': int,  --> number that will appear in the voting for this answer
                #     'authors': list(int) -> index of players writing that answer
                #     'correct': bool -> if correct answer
                #     'voted_by': list(int) -> indexes of players' indexes voting that answer
                # }
            'HAND_POINTS': [{str(i):0 for i in range(self.num_players)} for i in range(self.num_hands)], # we can't have list of list in firestore
            'GAME_POINTS': [], # list of points (int) for each player
            'WINNERS_NAMES': []
        }
        self.state = 'STARTED'
        return True

    @transactional
    def set_player_text_answer_and_get_remaining(self, user, text): 
        player_index = self.players_id.index(user.id)
        hand_index = self.variables['HAND']-1
        current_players_answers = self.variables['PLAYERS_ANSWERS'][hand_index]
        current_players_answers[str(player_index)] = text
        remaining_players_indexes = [i for i in range(self.num_players) if str(i) not in current_players_answers]
        remaining_players_indexes.remove(self.get_reader_index())
        return len(remaining_players_indexes)

    @transactional
    def set_voted_indexes_and_get_remaining(self, user, voted_shuffled_number): 
        answers_info = self.get_current_hand_answers_info()
        player_index = self.players_id.index(user.id)
        reader_index = self.get_reader_index()
        assert player_index != reader_index # reader doesn't vote                    
        voted_answer_info = next(info for c,info in answers_info.items() if info['shuffled_number']==voted_shuffled_number)
        voted_answer_info['voted_by'].append(player_index)   
        voted_by_list = [info['voted_by'] for info in answers_info.values()] 
        voters_indexes = list(itertools.chain(*voted_by_list))        
        exact_author_list = next((info['authors'] for info in answers_info.values() if info['correct']),[reader_index])
        remaining_players_indexes = [i for i in range(self.num_players) if i not in voters_indexes and i not in exact_author_list]
        return len(remaining_players_indexes)

    @transactional 
    def set_confirm(self, user):
        player_index = self.players_id.index(user.id)
        if self.variables['CONFIRMED_CURRENT_HAND'][player_index]:
            return False
        self.variables['CONFIRMED_CURRENT_HAND'][player_index] = True
        return True

    @transactional 
    def set_selected(self, user):
        player_index = self.players_id.index(user.id)
        if self.variables['SELECTED_CURRENT_HAND'][player_index]:
            return False
        self.variables['SELECTED_CURRENT_HAND'][player_index] = True
        return True

    @transactional
    def setup_next_hand(self):
        hand_index = self.variables['HAND']-1
        if self.variables['COMPLETED_HANDS'][hand_index]:
            # already setup next hand (double button press)
            return False
        self.variables['COMPLETED_HANDS'][hand_index] = True
        self.variables['CONFIRMED_CURRENT_HAND'] = [False for _ in range(self.num_players)]
        self.variables['SELECTED_CURRENT_HAND'] = [False for _ in range(self.num_players)]
        self.variables['HAND'] += 1
        return True


    ##########################################
    # END of TRANSACTIONAL FUNCTIONS
    ##########################################

    def auto_exercise_mode(self):
        False
        # return self.game_type=='SYNONYM' and self.language == 'en' and self.game_control == 'TEACHER'

    def fill_exercises_automatically(self, batch_number, save=True):
        import exercise_data_utils
        exercises = exercise_data_utils.extract_random_exercises(batch_number, self.num_hands)
        # list of dict {"SENTENCE": <str>, "MWE": <str>}
        for e in exercises:
            self.variables['INCOMPLETE_TEXTS'].append(e['SENTENCE'].upper())
            self.variables['ORIGINAL_COMPLETION'].append(e['MWE'].upper())
        if save: self.save()

    def get_creator_name(self):
        creator_name = self.players_names[0]
        return escape_markdown(creator_name)

    def is_last_hand(self):
        return self.variables['HAND'] == self.num_hands

    def get_reader_index(self):
        if self.game_control == 'TEACHER':
            return 0
        return (self.variables['HAND'] - 1 ) % self.num_players

    def get_hand_number(self):
        return self.variables['HAND']

    def get_current_hand_players_reader_writers(self):
        players = self.get_players()
        reader = players[self.get_reader_index()]
        writers = [p for p in players if p != reader]
        return players, reader, writers

    def set_current_incomplete_text(self, text, save=True):        
        hand_index = self.variables['HAND']-1
        self.variables['INCOMPLETE_TEXTS'][hand_index] = text
        if save: self.save()

    def get_current_incomplete_text(self):        
        hand_index = self.variables['HAND']-1
        return self.variables['INCOMPLETE_TEXTS'][hand_index]

    def get_current_incomplete_text_and_original_completion(self):        
        hand_index = self.variables['HAND']-1
        incomplete_text = self.variables['INCOMPLETE_TEXTS'][hand_index]
        original_completion = self.variables['ORIGINAL_COMPLETION'][hand_index]
        return incomplete_text, original_completion

    def set_current_completion_text(self, text, save=True):        
        hand_index = self.variables['HAND']-1
        self.variables['ORIGINAL_COMPLETION'][hand_index] = text
        if save: self.save()

    def get_current_completion_text(self):        
        hand_index = self.variables['HAND']-1
        return self.variables['ORIGINAL_COMPLETION'][hand_index]

    def get_current_hand_answers_info(self):        
        hand_index = self.variables['HAND']-1
        return self.variables['ANSWERS_INFO'][hand_index]

    def get_incomplete_text_pre_post_gap(self):        
        incomplete_text = self.get_current_incomplete_text()
        gap_string = '???'
        gap_index = incomplete_text.index(gap_string)
        pre_gap = incomplete_text[:gap_index]
        post_gap = incomplete_text[gap_index+len(gap_string):]
        return pre_gap, post_gap

    def has_player_already_written_answer(self, user):        
        player_index = self.players_id.index(user.id)
        hand_index = self.variables['HAND']-1
        current_players_answers = self.variables['PLAYERS_ANSWERS'][hand_index]
        return str(player_index) in current_players_answers

    def set_correct_answers(self, correct_answers_number_list, save=True):
        answers_info = self.get_current_hand_answers_info()
        for d in answers_info.values():
            if d['shuffled_number'] in correct_answers_number_list:
                d['correct'] = True
        if save: self.save()

    def get_remaining_answers_names(self):
        hand_index = self.variables['HAND']-1
        current_players_answers = self.variables['PLAYERS_ANSWERS'][hand_index]
        remaining_players_indexes = [i for i in range(self.num_players) if str(i) not in current_players_answers]
        remaining_players_indexes.remove(self.get_reader_index())
        remaining_names = [self.players_names[i] for i in remaining_players_indexes]            
        return remaining_names

    def prepare_voting(self):                
        hand_index = self.variables['HAND']-1
        answers_info = self.variables['ANSWERS_INFO'][hand_index]
        players_answers = self.variables['PLAYERS_ANSWERS'][hand_index]
        original_completion = self.variables['ORIGINAL_COMPLETION'][hand_index]
        players_answers_unique = sorted(set(players_answers.values()))
        number_displayed_answers = len(players_answers_unique)
        original_in_players_answers = original_completion in players_answers_unique
        if not self.is_voting_no_or_multiple_answers_allowed() and not original_in_players_answers:
            number_displayed_answers += 1 # adding the original one
        shuffled_numbers = list(range(1,number_displayed_answers+1))
        shuffle(shuffled_numbers)
        iter_shuffled_numbers = iter(shuffled_numbers)
        
        for answer in players_answers_unique:
            is_original = answer == original_completion
            answers_info[answer] = {
                'answer': answer,
                'shuffled_number': next(iter_shuffled_numbers),
                'authors': [
                    int(i) for i,c in players_answers.items()
                    if c == answer
                ],
                'correct': is_original,
                'voted_by': []
            }
        if self.is_voting_no_or_multiple_answers_allowed():
            # for collecting the NO CORRECT ANSWERS votes (applicabole e.g., in SYNONYM)
            # -1 is used for shuffled_number
            answers_info[parameters.NO_ANSWER_KEY] = {
                'answer': parameters.NO_ANSWER_KEY,
                'shuffled_number': -1,
                'authors': [],
                'correct': False,
                'voted_by': []
            }
        else:
            reader_index = self.get_reader_index()
            if original_in_players_answers:
                correct_answer = answers_info[original_completion]
                correct_answer['authors'].append(reader_index)
                correct_answer['correct'] = True
            else:
                # add correct answer
                answers_info[original_completion] = {
                    'answer': original_completion,
                    'shuffled_number': next(iter_shuffled_numbers),
                    'authors': [reader_index],
                    'correct': True,
                    'voted_by': []
                }   
        
        # selection is enabled only if there are at least 2 unique answers
        # we should not count the answer given by the same person
        self.set_var('SELECTION_ENABLED', len(answers_info) > 2)
        
        self.save()

    def get_correct_answers_authors_indexes(self):        
        answers_info = self.get_current_hand_answers_info()
        answer_correct_info = next((info for c,info in answers_info.items() if info['correct']), None)
        if answer_correct_info is None:
            return []
        return [i for i in answer_correct_info['authors'] if i!=self.get_reader_index()]

    def has_user_already_voted(self, user):
        player_index = self.players_id.index(user.id)        
        answers_info = self.get_current_hand_answers_info()
        return any(player_index in info['voted_by'] for info in answers_info.values())

    def get_names_remaining_voters(self):        
        answers_info = self.get_current_hand_answers_info()
        names = self.players_names        
        voted_by_list = [info['voted_by'] for info in answers_info.values()] 
        voters_indexes = list(itertools.chain(*voted_by_list))
        reader_index = self.get_reader_index()
        exact_author_list = next((info['authors'] for info in answers_info.values() if info['correct']),[reader_index])
        remaining_names = [n for i,n in enumerate(names) if i not in voters_indexes and i not in exact_author_list] 
        return remaining_names   

    '''
    Return answers (in shuffled order), possibly including the empty answer (for no vote)
    '''
    def get_shuffled_answers_info(self, include_no_vote):
        answers_info = self.get_current_hand_answers_info()
        shuffled_answers = [
            v for v in sorted(answers_info.values(), key=lambda v: v['shuffled_number'])
            if v['shuffled_number'] != -1
        ]
        if include_no_vote:
            no_vote_answer = next(v for v in answers_info.values() if v['shuffled_number'] == -1)
            shuffled_answers.append(no_vote_answer)
        return shuffled_answers

    def prepare_hand_poins_and_get_points_feedbacks(self):     
        POINT_SYSTEM = parameters.POINTS[self.game_type]
        hand_index = self.variables['HAND']-1
        answers_info = self.variables['ANSWERS_INFO'][hand_index]
        current_hand_points = self.variables['HAND_POINTS'][hand_index]
        reader_index = self.get_reader_index()
        
        points_feedbacks = [{} for i in range(self.num_players)]         
            # one dict per player
            # feedbacks[i] = {
            #     'POINTS': <int>,
            #     'ANSWERED_CORRECTLY': <bool>,
            #     'NO_ANSWER': <bool>,
            #     'SELECTED_CORRECTLY': <bool>,
            #     'NO_SELECTION': <bool>,
            #     'NUM_VOTES_RECEIVED': <int> # not applicable in teacher mode
            # }
        
        # init received_votes
        for pfi in points_feedbacks: 
            pfi['NUM_VOTES_RECEIVED'] = 0
            pfi['POINTS'] = 0            

        for i in range(self.num_players):            
            if i==reader_index:
                continue # reader doesn't give/receive points
            pfi = points_feedbacks[i]
            player_answer_info = next((info for info in answers_info.values() if i in info['authors']),None)
            player_voted_answer_info = next((info for info in answers_info.values() if i in info['voted_by']),None)            

            if player_answer_info is None:
                # player didn't answer
                pfi['POINTS'] += POINT_SYSTEM['NO_ANSWER']
            elif player_answer_info['correct']:    
                pfi['POINTS'] += POINT_SYSTEM['CORRECT_ANSWER']
            else: # incorrect answer (0)
                pfi['POINTS'] += POINT_SYSTEM['INCORRECT_ANSWER']

            pfi['ANSWERED_CORRECTLY'] = player_answer_info and player_answer_info['correct']
            pfi['NO_ANSWER'] = player_answer_info is None
            pfi['NO_SELECTION'] = player_voted_answer_info is None

            if player_voted_answer_info:
                # player has voted
                if player_voted_answer_info['shuffled_number'] == -1:
                    # player voted NONE ANSWER 
                    # NONE is relative to the option available
                    all_available_answers_are_wrong = not any(
                        info['correct'] for info in answers_info.values() 
                        if info['shuffled_number']!=-1 and i not in info['authors']
                    )
                    player_selected_correctly = all_available_answers_are_wrong
                else:
                    player_selected_correctly = player_voted_answer_info['correct']
                pfi['SELECTED_CORRECTLY'] = player_selected_correctly
                if player_selected_correctly:
                    pfi['POINTS'] += POINT_SYSTEM['CORRECT_SELECTION']                    
                elif self.teacher_validation_enabled():
                    # wrong answer (we penalize wrong answers only if teacher validation is on)
                    pfi['POINTS'] += POINT_SYSTEM['INCORRECT_SELECTION']                
            elif not pfi['ANSWERED_CORRECTLY'] and self.get_var('SELECTION_ENABLED'):
                # penalize player for not voting
                pfi['POINTS'] += POINT_SYSTEM['NO_SELECTION']                
            if not self.teacher_validation_enabled():    
                # peole get awarded points when voted by others only if teacher validation is off
                if player_voted_answer_info:                                         
                    for j in player_voted_answer_info['authors']:
                        if j != reader_index:
                            # don't give point to reader
                            points_feedbacks[j]['POINTS'] += POINT_SYSTEM['RECEIVED_VOTE']
                            points_feedbacks[j]['NUM_VOTES_RECEIVED'] += 1
            # if 'SELECTED_CORRECTLY' not in pfi:
            #     # either i) she previous answered correctly or ii) she didn't provide a selection (jump)
            #     pfi['SELECTED_CORRECTLY'] = False
        
        for i in range(self.num_players):  
            current_hand_points[str(i)] = points_feedbacks[i]['POINTS']
        
        # recalculate game points
        self.variables['GAME_POINTS'] = [
            sum(
                current_hand_points[str(i)] 
                for current_hand_points in self.variables['HAND_POINTS']
            ) 
            for i in range(self.num_players)
        ]
        self.save()
        return points_feedbacks

    def send_points_img_data(self, players, save=False):
        from render_leaderboard import get_image_data_from_hands_points
        from bot_telegram import send_photo_from_data_multi        

        hand_number = self.variables['HAND']
        hands_points = copy.deepcopy(self.variables['HAND_POINTS'])
        game_points = copy.deepcopy(self.variables['GAME_POINTS'])
        players_names = [p.get_name(escape_md=False) for p in players]
        hands_points_list = [
            [hp[str(i)] for i in range(self.num_players)]
            for hp in hands_points[:hand_number]
        ]          

        if self.game_control == 'TEACHER':
            del(players_names[0])            
            del(game_points[0])  
            for hp in hands_points_list:
                del(hp[0])        
              
        img_data = get_image_data_from_hands_points(players_names, hands_points_list, game_points)
        send_photo_from_data_multi(players, 'leaderboard_hand.png', img_data, sleep=True)

    def get_winner_names(self):        
        players_names = list(self.players_names)
        game_points = copy.deepcopy(self.variables['GAME_POINTS'])
        
        if self.game_control == 'TEACHER':
            del(players_names[0])            
            del(game_points[0])  

        max_point = max(game_points)
        winner_names = [players_names[i] for i,p in enumerate(game_points) if p==max_point]
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
            games = list(Game.query([('state', '==', s)]).get())
            count = len(games)
            id_list = [g.id for g in games]
            print("{}:{} {}".format(s, count, id_list))

    @staticmethod
    def get_expired_games():
        from utility import get_milliseconds
        from parameters import EXPIRATION_DELTA_MILLISECONDS
        now = get_milliseconds()        
        expiration = now - EXPIRATION_DELTA_MILLISECONDS
        games_generator = Game.query([
            ('state', 'in', ['INITIAL', 'STARTED']),
            ('modified', '<', expiration)
        ]).get()
        # for g in games_generator:
        #     print(g.name)
        # return len(list(games_generator))
        return games_generator

if __name__ == "__main__":
    Game.get_game_state_stats()
