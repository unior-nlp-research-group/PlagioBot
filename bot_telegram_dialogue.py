# -*- coding: utf-8 -*-

import logging
from bot_telegram import BOT, send_message, send_messages, send_typing_action, send_text_document, send_message_multi, exception_reporter, report_master
import utility
import bot_ui as ux
import telegram
import bot_firestore_user
from bot_firestore_user import User
import bot_firestore_game
from bot_firestore_game import Game
import utility
import time

# ================================
# CONFIG
# ================================
DEBUG = True

# ================================
# RESTART
# ================================
def restart_multi(users):
    for u in users:
        redirect_to_state(u, state_INITIAL, message_obj=None)


def restart_user(user):
    redirect_to_state(user, state_INITIAL, message_obj=None)

# ================================
# REDIRECT TO STATE
# ================================
def redirect_to_state_multi(users, new_function, message_obj=None):
    reversed_users = list(reversed(users)) # so that game creator is last
    for u in reversed_users:
        redirect_to_state(u, new_function, message_obj)

def redirect_to_state(user, new_function, message_obj=None):
    new_state = new_function.__name__
    if user.state != new_state:
        logging.debug("In redirect_to_state. current_state:{0}, new_state: {1}".format(str(user.state), str(new_state)))
        user.state = new_state
        user.save()
    repeat_state(user, message_obj)


# ================================
# REPEAT STATE
# ================================
def repeat_state(user, message_obj=None):
    state = user.state
    if state is None:
        restart_user(user)
        return
    method = possibles.get(state)
    if not method:
        msg = "⚠️ User {} sent to unknown method state: {}".format(user.serial_number, state)
        report_master(msg)
    else:
        method(user, message_obj)

# ================================
# Initial State
# ================================
def state_INITIAL(user, message_obj):
    lang = user.language
    if message_obj is None:
        kb = [
            [ux.BUTTON_START_GAME[lang]],
            [ux.BUTTON_CHANGE_LANGUAGE[lang], ux.BUTTON_INFO[lang]]
        ]
        notifications_button = [ux.BUTTON_DISABLE_NOTIFICATIONS[lang]] if user.notifications else [ux.BUTTON_ENABLE_NOTIFICATIONS[lang]]
        kb.append(notifications_button)
        user.set_keyboard(kb)
        msg_notifications = ux.MSG_NOTIFICATIONS_ON[lang] if user.notifications else ux.MSG_NOTIFICATIONS_OFF[lang]
        msg = '\n\n'.join([ux.MSG_HOME[lang],ux.MSG_LANGUAGE_INFO[lang],msg_notifications])
        send_message(user, msg, kb)
    else:
        text_input = message_obj.text
        kb = user.get_keyboard()
        if text_input in utility.flatten(kb):
            if text_input == ux.BUTTON_START_GAME[lang]:
                redirect_to_state(user, state_CHOOSE_ROOM_NAME)
            elif text_input == ux.BUTTON_INFO[lang]:
                send_message(user, ux.MSG_INFO[lang])
            elif text_input == ux.BUTTON_CHANGE_LANGUAGE[lang]:
                redirect_to_state(user, state_CHANGE_LANGUAGE)
            elif text_input in [ux.BUTTON_DISABLE_NOTIFICATIONS[lang], ux.BUTTON_ENABLE_NOTIFICATIONS[lang]]:
                user.switch_notifications()
                repeat_state(user)
            else:
                assert(False)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_BUTTONS[lang], kb)

# ================================
# Change Language
# ================================
def state_CHANGE_LANGUAGE(user, message_obj):
    lang = user.language
    if message_obj is None:
        msg = ux.MSG_CHANGE_LANGUAGE[lang]
        kb = [[ux.IT_FLAG_SYMBOL, ux.EN_FLAG_SYMBOL],[ux.BUTTON_BACK[lang]]]
        user.set_keyboard(kb)
        send_message(user, msg, kb)
    else:
        text_input = message_obj.text
        kb = user.get_keyboard()
        if text_input in utility.flatten(kb):
            if text_input == ux.IT_FLAG_SYMBOL:
                user.language = lang = 'it'
                send_message(user, ux.MSG_LANGUAGE_INFO[lang])
                restart_user(user)
            elif text_input == ux.EN_FLAG_SYMBOL:
                user.language = lang = 'en'
                send_message(user, ux.MSG_LANGUAGE_INFO[lang])
                restart_user(user)
            elif text_input == ux.BUTTON_BACK[lang]:
                restart_user(user)
            else:
                assert(False)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_BUTTONS[lang], kb)

# ================================
# Choose Room Name
# ================================
def state_CHOOSE_ROOM_NAME(user, message_obj):
    lang = user.language
    if message_obj is None:
        kb = [[ux.BUTTON_BACK[lang]]]
        user.set_keyboard(kb)
        send_message(user, ux.MSG_CHOOSE_GAME_NAME[lang], kb)
    else:
        text_input = message_obj.text
        kb = user.get_keyboard()
        if text_input:
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK[lang]:
                    restart_user(user)
                else:
                    assert(False)
            elif text_input in ux.ALL_BUTTONS_TEXT_LIST:
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)
            else:
                room_name = text_input.upper()
                game = Game.get_ongoing_game(room_name)
                if game:
                    if game.just_created():
                        send_message(user, ux.MSG_GAME_NOT_YET_READY[lang].format(room_name), kb)
                        send_typing_action(user, sleep_secs=2)
                        repeat_state(user)
                    elif Game.add_player(game, user):
                        redirect_to_state(user, state_WAITING_FOR_OTHER_PLAYERS)
                    else:
                        send_message(user, ux.MSG_GAME_ALREADY_STARTED[lang], kb)
                else:
                    user.set_var('GAME_NAME',room_name)
                    redirect_to_state(user, state_CREATE_GAME)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang], kb)

# ================================
# Create Game
# ================================
def state_CREATE_GAME(user, message_obj):
    lang = user.language
    room_name = user.get_var('GAME_NAME')
    if message_obj is None:
        kb = [[ux.BUTTON_YES[lang], ux.BUTTON_NO[lang]]]
        user.set_keyboard(kb)
        msg = ux.MSG_NEW_GAME_CONFIRM[lang].format(room_name)
        send_message(user, msg, kb)
    else:
        text_input = message_obj.text
        kb = user.get_keyboard()
        if text_input in utility.flatten(kb):
            if text_input == ux.BUTTON_YES[lang]:
                if (Game.get_ongoing_game(room_name)):
                    send_message(user, ux.MSG_NAME_NO_LONGER_AVAILBLE[lang].format(room_name))
                    redirect_to_state(user, state_CHOOSE_ROOM_NAME)
                else:
                    game = Game(room_name, user)
                    user.set_current_game(game)
                    redirect_to_state(user, state_CHOOSE_NUMBER_PLAYERS)
            elif text_input == ux.BUTTON_NO[lang]:
                redirect_to_state(user, state_CHOOSE_ROOM_NAME)
            else:
                assert(False)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_BUTTONS[lang], kb)

# ================================
# Choose number of players
# ================================
def state_CHOOSE_NUMBER_PLAYERS(user, message_obj):
    lang = user.language
    kb = [['3','4','5','6'],[ux.BUTTON_ABORT[lang]]]
    if message_obj is None:
        user.set_keyboard(kb)
        send_message(user, ux.MSG_NUMBER_OF_PLAYERS[lang], kb)
    else:
        game = user.get_current_game()
        text_input = message_obj.text
        if text_input in utility.flatten(kb):
            if text_input == ux.BUTTON_ABORT[lang]:
                interrupt_game(game, user)
                return
            else:
                assert(utility.represents_int_between(text_input,3,6))
        if utility.represents_int_between(text_input,2,100):
            number_players = int(text_input)
            game.set_number_of_players(number_players)
            # redirect_to_state(user, state_ENTER_SPECIAL_RULES)
            redirect_to_state(user, state_WAITING_FOR_OTHER_PLAYERS)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang], kb)

# ================================
# Enter special rules
# ================================
# def state_ENTER_SPECIAL_RULES(user, message_obj):
#     lang = user.language
#     kb = [[ux.BUTTON_SKIP[lang]],[ux.BUTTON_ABORT[lang]]]
#     if message_obj is None:
#         user.set_keyboard(kb)
#         send_message(user, ux.MSG_WRITE_GAME_SPECIAL_RULES[lang], kb)
#     else:
#         game = user.get_current_game()
#         text_input = message_obj.text
#         if text_input:
#             if text_input in utility.flatten(kb):
#                 if text_input == ux.BUTTON_ABORT[lang]:
#                     interrupt_game(game, user)
#                     restart_user(user)
#                 elif text_input == ux.BUTTON_SKIP[lang]:
#                     redirect_to_state(user, state_WAITING_FOR_OTHER_PLAYERS)
#                 else:
#                     assert(False)
#             elif text_input in ux.ALL_BUTTONS_TEXT_LIST:
#                 send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)
#             else:
#                 game.set_special_rules(text_input)
#                 redirect_to_state(user, state_WAITING_FOR_OTHER_PLAYERS)
#         else:
#             send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang], kb)

# ================================
# Waiting for game start
# ================================
def state_WAITING_FOR_OTHER_PLAYERS(user, message_obj):    
    game = user.get_current_game()
    players = game.get_players()
    lang = players[0].language
    if message_obj is None:
        msg = ux.MSG_ENTERING_GAME_X[lang].format(game.get_name())
        send_message(user, msg, remove_keyboard=True)
        if user == players[0]:
            # kb = [[ux.BUTTON_ANNOUNCE_GAME_PUBLICLY[lang]]]
            # user.set_keyboard(kb)
            msg_invite = ux.MSG_INVITE_PEOPLE_OR_ANNOUNCE[lang].format(game.get_name())
            # send_message(user, msg_invite, kb)
            send_message(user, msg_invite, remove_keyboard=True)
        else:
            msg_other_players = ux.MSG_PLAYER_X_JOINED_GAME[lang].format(user.get_name())
            send_message_multi(players, msg_other_players)
            get_available_seats = game.get_available_seats()
            if get_available_seats==0:
                send_message_multi(players, ux.MSG_READY_TO_START[lang])
                special_rules = game.get_special_rules()
                if special_rules:
                    creator_name = players[0].get_name()
                    special_rules_msg = ux.MSG_TELL_SPECIAL_RULES[lang].format(creator_name, special_rules)
                    send_message_multi(players, special_rules_msg)
                game.setup()
                redirect_to_state_multi(players, state_GAME_READER_WRITES_BEGINNING)
            else:
                if get_available_seats>1:
                    msg_waiting = ux.MSG_WAITING_FOR_X_PLAYERS_PL[lang].format(get_available_seats, game.get_name())
                else:
                    msg_waiting = ux.MSG_WAITING_FOR_X_PLAYERS_SG[lang].format(get_available_seats, game.get_name())
                send_message_multi(players, msg_waiting)
    else:
        get_available_seats = game.get_available_seats()
        if user == players[0]:
            text_input = message_obj.text
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input==ux.BUTTON_ANNOUNCE_GAME_PUBLICLY[lang]:
                    send_message(user, ux.MSG_SENT_ANNOUNCEMENT[lang], remove_keyboard=True)
                    command = utility.escape_markdown('/game_{}'.format(game.key.id))
                    announce_msg = ux.MSG_ANNOUNCE_GAME_PUBLICLY[lang].format(user.get_name(), game.number_players, get_available_seats, command)
                    users = User.get_user_lang_state_notification_on(lang, 'state_INITIAL')
                    send_message_multi(users, announce_msg)
                    return
                else:
                    assert(False)
        if get_available_seats>1:
            msg = ux.MSG_WAITING_FOR_X_PLAYERS_PL[lang].format(get_available_seats, game.get_name())
        else:
            msg = ux.MSG_WAITING_FOR_X_PLAYERS_SG[lang].format(get_available_seats, game.get_name())
        send_message(user, msg)

# ================================
# GAME_READER_WRITES_BEGINNING
# ================================
def state_GAME_READER_WRITES_BEGINNING(user, message_obj):
    game = user.get_current_game()
    hand, players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = players[0].language
    if message_obj is None:
        if user == players[0]:
            msg_intro = ux.MSG_HAND_INFO[lang].format(hand, reader.get_name())
            send_message_multi(players, msg_intro)
            msg_reader = ux.MSG_READER_WRITES_BEGINNING[lang]
            send_message(reader, msg_reader)
            msg_writers = ux.MSG_WRITERS_WAIT_READER_BEGINNING[lang].format(reader.get_name())
            send_message_multi(writers, msg_writers)
    else:
        if user == reader:
            text_input = message_obj.text
            if text_input:
                if text_input in ux.ALL_BUTTONS_TEXT_LIST:
                    send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang])
                else:
                    beginning = text_input.upper()
                    game.set_reader_text_beginning(beginning)
                    redirect_to_state_multi(players, state_GAME_READER_WRITES_TEXT_INFO)
            else:
                send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang])
        else:
            msg = ux.MSG_WRONG_INPUT_WAIT_FOR_READER[lang].format(reader.get_name())
            send_message(user, msg)

# ================================
# GAME_READER_WRITES_TEXT_INFO
# ================================
def state_GAME_READER_WRITES_TEXT_INFO(user, message_obj):
    game = user.get_current_game()
    _, players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = players[0].language
    if message_obj is None:
        if user == players[0]:
            kb = [[ux.BUTTON_SKIP[lang]]]
            msg_reader = ux.MSG_READER_WRITES_TEXT_INFO[lang]
            send_message(reader, msg_reader, kb)    
            reader.set_keyboard(kb)        
            msg_writers = ux.MSG_WRITERS_WAIT_READER_TEXT_INFO[lang].format(reader.get_name())
            send_message_multi(writers, msg_writers)            
    else:
        if user == reader:
            text_input = message_obj.text
            kb = user.get_keyboard()
            if text_input:
                if text_input in utility.flatten(kb):
                    if text_input == ux.BUTTON_SKIP[lang]:
                        game.set_reader_text_info('')
                        msg_writers = ux.MSG_WRITERS_NO_INFO_BOOK[lang].format(reader.get_name())
                        send_message_multi(writers, msg_writers)
                        redirect_to_state_multi(players, state_GAME_PLAYERS_WRITE_CONTINUATIONS)
                    else:
                        assert(False)                
                elif text_input in ux.ALL_BUTTONS_TEXT_LIST:
                    send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)
                else:
                    game.set_reader_text_info(text_input)
                    msg_writers = ux.MSG_WRITERS_INFO_BOOK[lang].format(reader.get_name(), text_input)
                    send_message_multi(writers, msg_writers)
                    redirect_to_state_multi(players, state_GAME_PLAYERS_WRITE_CONTINUATIONS)
            else:
                send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang])
        else:
            msg = ux.MSG_WRONG_INPUT_WAIT_FOR_READER[lang].format(reader.get_name())
            send_message(user, msg)

# ================================
# GAME_PLAYERS_WRITE_CONTINUATIONS
# ================================
def state_GAME_PLAYERS_WRITE_CONTINUATIONS(user, message_obj):
    game = user.get_current_game()
    _, players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = players[0].language
    if message_obj is None:
        if user == players[0]:
            beginning = '*{}*'.format(utility.escape_markdown(game.get_reader_text_beginning()))
            msg_intro = ux.MSG_PLAYERS_BEGINNING_INFO[lang].format(reader.get_name())
            send_message_multi(players, msg_intro)
            send_message_multi(players, beginning)
            msg_reader = ux.MSG_READER_WRITE_CONTINUATION[lang]
            send_message(reader, msg_reader, remove_keyboard=True)
            msg_writers = ux.MSG_WRITERS_WRITE_CONTINUATION[lang].format(reader.get_name())
            send_message_multi(writers, msg_writers)
    else:
        text_input = message_obj.text
        if game.has_player_already_written_continuation(user):
            send_message(user, ux.MSG_ALREADY_SENT_CONTINUATION[lang])
            return
        if text_input:
            if text_input in ux.ALL_BUTTONS_TEXT_LIST:
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang])
            else:
                continuation = text_input.upper()
                continuation = utility.add_full_stop_if_missing_end_puct(continuation)
                remaining_names = game.set_player_text_continuation_and_get_remaining(user, continuation)            
                if len(remaining_names)>0:
                    all_but_users = [p for p in players if p!=user]
                    remaining_names_str = ', '.join(remaining_names)
                    msgs = [ux.MSG_THANKS[lang],ux.MSG_WAIT_FOR[lang].format(remaining_names_str)]
                    send_messages(user, msgs, remove_keyboard=True)
                    logging.debug("Remainig names ({}): {}".format(len(remaining_names), remaining_names_str))
                    send_message_multi(all_but_users, ux.MSG_X_GAVE_CONTINUATION_WAITING_FOR_PLAYERS_NAME_CONTINUATION[lang].format(user.get_name(), remaining_names_str))
                else:
                    game.prepare_voting()
                    redirect_to_state_multi(players, state_GAME_VOTE_CONTINUATION)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang])

# ================================
# GAME_PLAYERS_WRITE_CONTINUATIONS 
# invoked only for last user inserting continuation
# ================================
def state_GAME_VOTE_CONTINUATION(user, message_obj):
    game = user.get_current_game()
    _, players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = players[0].language
    # continuations_info = game.get_hand_continuations_info()
    exact_guessers_indexes = game.get_guessers_indexes()
    exact_guessers = [players[i] for i in exact_guessers_indexes]
    exact_guessers_names = [p.get_name() for p in exact_guessers]
    all_guessed_correctly = len(exact_guessers_indexes) == len(players) - 1
    shuffled_continuations = game.get_shuffled_continuations()
    # report_master("🐛 exact_guessers_names: {}".format(exact_guessers_names))
    # correct_continuation_position = game.get_correct_continuation_shuffled_index() + 1 
    remaining_names = game.get_names_remaining_voters()
    remaining_names_str = ', '.join(remaining_names)

    def recap_votes():
        beginning = game.get_reader_text_beginning()
        msg_summary = ux.MSG_VOTE_RECAP[lang]
        send_message_multi(players, msg_summary, remove_keyboard=True)
        shuf_cont_voters_names = game.get_shuffled_continuations_voters()                
        for i, cont in enumerate(shuffled_continuations):
            authors_indexes = game.get_continuations_authors_indexes(cont)
            authors = [players[i] for i in authors_indexes]            
            voters_names = shuf_cont_voters_names[i]
            voters_summay = str(len(voters_names))
            if voters_names:
                voters_summay += " ({})".format(', '.join(voters_names))
            if reader in authors:
                guessers_summary = str(len(exact_guessers_names))
                if exact_guessers_names:
                    guessers_summary += " ({})".format(', '.join(exact_guessers_names))
                msg_summary = "{} *{}* ⭐️ → {} *{}*\n{}".format(
                    i+1, reader.get_name(), beginning, cont, \
                    ux.MSG_GUESSED_BY_AND_VOTED_BY[lang].format(guessers_summary, voters_summay))
            else:
                author_names = ', '.join(p.get_name() for p in authors)
                msg_summary = "{} *{}* → {} *{}*\n{}".format(
                    i+1, author_names, beginning, cont, ux.MSG_VOTED_BY[lang].format(voters_summay))
            send_message_multi(players, msg_summary)
        send_message_multi(players, ux.MSG_POINT_HAND_SUMMARY[lang])
        game.prepare_and_send_hand_point_img_data(players)                    
        if game.is_last_hand():
            send_message_multi(players, ux.MSG_POINT_GAME_SUMMARY[lang])
            game.prepare_and_send_game_point_img_data(players, save=True)
            winners_names = game.get_winner_names()
            winner_msg = ux.MSG_WINNER_SINGULAR[lang] if len(winners_names)==1 else ux.MSG_WINNER_PLURAL[lang]
            winner_msg = winner_msg.format(', '.join(winners_names))
            send_message_multi(players, winner_msg)
            end_game(game, players)
        else:
            send_message_multi(players, ux.MSG_POINT_GAME_PARTIAL_SUMMARY[lang])
            game.prepare_and_send_game_point_img_data(players)
            game.setup_next_hand()
            redirect_to_state_multi(players, state_GAME_READER_WRITES_BEGINNING)

    if message_obj is None:
        if user == players[0]:
            if all_guessed_correctly:
                send_message_multi(writers, ux.MSG_GUESSED_NO_VOTE[lang], remove_keyboard=True)
                state_GAME_VOTE_CONTINUATION(user, message_obj=True)
                return            
            #report_master("player_to_shuffled_cont_index: {}".format(player_to_shuffled_cont_index))
            #report_master("shuffled_continuations: {}".format(shuffled_continuations))
            number_continuations = len(shuffled_continuations)
            intro_msg = ux.MSG_INTRO_NUMBERED_TEXT[lang]
            send_message_multi(players, intro_msg)
            beginning = game.get_reader_text_beginning()
            for num, cont in enumerate(shuffled_continuations,1):
                cont_msg = "{}: {} *{}*".format(num, beginning, cont)
                send_message_multi(players, cont_msg)
            send_message(reader, ux.MSG_WAIT_FOR_PLAYERS_TO_VOTE_PL[lang])
            numbers_list = list(range(1,number_continuations+1))            
            
            #report_master("reader {} continuation in position: {}".format(reader.get_name(), correct_continuation_position))            
            for w in writers:
                w_index = players.index(w)
                w_shuffled_number = game.get_continuation_shuffled_index(w_index) + 1
                #report_master("writer {} continuation in position {}".format(w.get_name(), w_shuffled_number))
                if w_index in exact_guessers_indexes:    
                    msgs = [ux.MSG_GUESSED_NO_VOTE[lang],ux.MSG_WAIT_FOR[lang].format(remaining_names_str)]
                    send_messages(w, msgs, remove_keyboard=True)
                else:
                    kb = [[str(i) for i in numbers_list if i != w_shuffled_number]]
                    w.set_keyboard(kb)
                    send_message(w, ux.MSG_VOTE[lang], kb, sleep=True)
    else:
        if all_guessed_correctly:
            recap_votes()
        elif user == reader:
            send_message(user, ux.MSG_WRONG_INPUT_WAIT_FOR_PLAYERS_TO_VOTE[lang])
        else:
            text_input = message_obj.text
            if game.has_user_already_voted(user):                
                send_message(user, ux.MSG_ALREADY_VOTED_WAITING_FOR[lang].format(remaining_names_str))
                return
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                voted_shuffled_index = int(text_input) - 1
                remaining_names = game.set_voted_indexes_and_points_and_get_remaining(user, voted_shuffled_index)
                remaining_names_str = ', '.join(remaining_names)
                all_but_users = [p for p in players if p!=user]
                send_message_multi(all_but_users, ux.MSG_X_VOTED[lang].format(user.get_name()))
                if len(remaining_names)>0:
                    user.set_keyboard([])
                    msgs = [ux.MSG_THANKS[lang],ux.MSG_WAIT_FOR[lang].format(remaining_names_str)]
                    send_messages(user, msgs, remove_keyboard=True)
                    send_message_multi(all_but_users, ux.MSG_WAIT_FOR[lang].format(remaining_names_str))
                else:
                    #only once
                    recap_votes()                    
            else:
                send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang], kb)


def end_game(game, players):
    for p in players:
        p.current_game_id = None
    game.state = 'ENDED'                        
    game.save()
    restart_multi(players)

def interrupt_game(game, user):
    game.state = 'INTERRUPTED'
    players = game.get_players()
    lang = players[0].language
    for p in players:
        p.current_game_id = None
    if len(players) > 0:
        send_message_multi(players, ux.MSG_EXIT_GAME[lang].format(user.get_name()))
    restart_multi(players)
    game.save()

def deal_with_universal_commands(user, text_input):
    #logging.debug('In universal command with input "{}". User is master: {}'.format(text_input, user.is_master()))
    lang = user.language
    if text_input == '/start':
        game = user.get_current_game()
        if game:
            send_message(user, ux.MSG_NO_START_COMMAND_AVAILABLE_DURING_GAME[lang])
            return True
        else:
            send_message(user, ux.MSG_WELCOME[lang])
            restart_user(user)
            return True
    if text_input == '/state':
        s = user.state
        msg = "You are in state {}".format(s)
        send_message(user, msg, markdown=False)
        return True
    if text_input == '/exit_game':
        game = user.get_current_game()
        if game:
            interrupt_game(game, user)
        else:
            send_message(user, ux.MSG_NO_GAME_TO_EXIT[lang])
        return True
    if text_input.startswith('/game_'):
        game_id = text_input.split('/game_')[1]
        if not utility.represents_int(game_id):
            send_message(user, ux.MSG_COMMAND_NOT_RECOGNIZED[lang])
        else:
            game = Game.get(game_id)
            if game:
                if game.add_player(user):
                    redirect_to_state(user, state_WAITING_FOR_OTHER_PLAYERS)
                else:
                    send_message(user, ux.MSG_NAME_NO_LONGER_AVAILBLE[lang])
            else:
                send_message(user, ux.MSG_NAME_NO_LONGER_AVAILBLE[lang])
        return True
    if user.is_master():
        if text_input == '/debug':
            game = user.get_current_game()
            send_text_document(user, 'tmp_vars.json', game.variables)
            return True
        if text_input == '/test_image':
            from bot_telegram import send_photo_from_data
            import render_leaderboard
            img_data = render_leaderboard.test()
            send_photo_from_data(user, 'test.png', img_data, caption='test')
            return True
        if text_input == '/exception':
            1/0
            return True
    return False

# ================================
# DEAL WITH REQUEST
# ================================
'''
python-telegram-bot documentation
https://python-telegram-bot.readthedocs.io/en/stable/
'''
@exception_reporter
def deal_with_request(request_json):
    # retrieve the message in JSON and then transform it to Telegram object
    update_obj = telegram.Update.de_json(request_json, BOT)
    message_obj = update_obj.message
    user_obj = message_obj.from_user
    username = user_obj.username
    last_name = user_obj.last_name if user_obj.last_name else ''
    name = (user_obj.first_name + ' ' + last_name).strip()
    language = user_obj.language_code
    
    user = User.get_user('telegram', user_obj.id)
    if user == None:
        user = User.create_user('telegram', user_obj.id, name, username, language)
        report_master('New user: {}'.format(user.get_name_at_username()))
    else:
        user.update_user(name, username)

    if message_obj.text:
        text_input = message_obj.text        
        logging.debug('Message from @{} in state {} with text {}'.format(user.serial_number, user.state, text_input))
        if DEBUG and not user.is_tester():
            send_message(user, ux.MSG_WORK_IN_PROGRESS[user.language])
            return
        if deal_with_universal_commands(user, text_input):
            return
    repeat_state(user, message_obj=message_obj)

possibles = globals().copy()
possibles.update(locals())

