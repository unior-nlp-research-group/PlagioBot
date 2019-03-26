# -*- coding: utf-8 -*-

import logging
from bot_telegram import BOT, send_message, send_message_multi, send_message_query, exception_reporter, report_master
import utility
import bot_ui as ux
import telegram
import bot_ndb_user
from bot_ndb_user import NDB_User
import bot_ndb_game
from bot_ndb_game import NDB_Game
import utility
import time

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
        user.put()
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
            else:
                room_name = text_input.upper()
                game = bot_ndb_game.get_ongoing_game(room_name)
                if game:
                    if game.add_player(user):
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
                if (bot_ndb_game.get_ongoing_game(room_name)):
                    send_message(user, ux.MSG_NAME_NO_LONGER_AVAILBLE[lang].format(room_name))
                    redirect_to_state(user, state_CHOOSE_ROOM_NAME)
                else:
                    game = NDB_Game(room_name, user)
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
                restart_user(user)
                return
            else:
                assert(utility.represents_int_between(text_input,3,6))
        if utility.represents_int_between(text_input,2,100):
            number_players = int(text_input)
            game.set_number_of_players(number_players)
            redirect_to_state(user, state_ENTER_SPECIAL_RULES)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang], kb)

# ================================
# Choose number of players
# ================================
def state_ENTER_SPECIAL_RULES(user, message_obj):
    lang = user.language
    kb = [[ux.BUTTON_SKIP[lang]],[ux.BUTTON_ABORT[lang]]]
    if message_obj is None:
        user.set_keyboard(kb)
        send_message(user, ux.MSG_WRITE_GAME_SPECIAL_RULES[lang], kb)
    else:
        game = user.get_current_game()
        text_input = message_obj.text
        if text_input in utility.flatten(kb):
            if text_input == ux.BUTTON_ABORT[lang]:
                interrupt_game(game, user)
                restart_user(user)
            elif text_input == ux.BUTTON_SKIP[lang]:
                redirect_to_state(user, state_WAITING_FOR_OTHER_PLAYERS)
            else:
                assert(False)
        elif text_input:
            game.set_special_rules(text_input)
            redirect_to_state(user, state_WAITING_FOR_OTHER_PLAYERS)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang], kb)

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
            available_seats = game.available_seats()
            if available_seats==0:
                send_message_multi(players, ux.MSG_READY_TO_START[lang])
                special_rules = game.get_special_rules()
                if special_rules:
                    creator_name = players[0].get_name()
                    special_rules_msg = ux.MSG_TELL_SPECIAL_RULES[lang].format(creator_name, special_rules)
                    send_message_multi(players, special_rules_msg)
                game.setup()
                redirect_to_state_multi(players, state_GAME_READER_WRITES_BEGINNING)
            else:
                if available_seats>1:
                    msg_waiting = ux.MSG_WAITING_FOR_X_PLAYERS_PL[lang].format(available_seats, game.get_name())
                else:
                    msg_waiting = ux.MSG_WAITING_FOR_X_PLAYERS_SG[lang].format(available_seats, game.get_name())
                send_message_multi(players, msg_waiting)
    else:
        available_seats = game.available_seats()
        if user == players[0]:
            text_input = message_obj.text
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input==ux.BUTTON_ANNOUNCE_GAME_PUBLICLY[lang]:
                    send_message(user, ux.MSG_SENT_ANNOUNCEMENT[lang], remove_keyboard=True)
                    command = utility.escape_markdown('/game_{}'.format(game.key.id))
                    announce_msg = ux.MSG_ANNOUNCE_GAME_PUBLICLY[lang].format(user.get_name(), game.number_players, available_seats, command)
                    query = bot_ndb_user.get_query_lang_state_notification_on(lang, 'state_INITIAL')
                    send_message_query(query, announce_msg)
                    return
                else:
                    assert(False)
        if available_seats>1:
            msg = ux.MSG_WAITING_FOR_X_PLAYERS_PL[lang].format(available_seats, game.get_name())
        else:
            msg = ux.MSG_WAITING_FOR_X_PLAYERS_SG[lang].format(available_seats, game.get_name())
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
        if game.player_has_already_written_continuation(user):
            send_message(user, ux.MSG_ALREADY_SENT_CONTINUATION[lang])
            return
        if text_input:
            continuation = text_input.upper()
            continuation = utility.add_full_stop_if_missing_end_puct(continuation)
            remaining_names = game.set_player_text_continuation_and_get_remaining(user, continuation)
            if len(remaining_names)>0:
                all_but_users = [p for p in players if p!=user]
                send_message(user, ux.MSG_THANKS_FOR_CONTINUATION[lang])
                send_message_multi(all_but_users, ux.MSG_X_GAVE_CONTINUATION_WAITING_FOR_PLAYERS_NAME_CONTINUATION[lang].format(user.get_name(), ', '.join(remaining_names)))
            else:
                redirect_to_state_multi(players, state_GAME_VOTE_CONTINUATION)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang])

# ================================
# GAME_PLAYERS_WRITE_CONTINUATIONS
# ================================
def state_GAME_VOTE_CONTINUATION(user, message_obj):
    game = user.get_current_game()
    _, players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = players[0].language
    if message_obj is None:
        if user == players[0]:
            shuffled_indexes, shuffled_continuations = game.get_players_shuffled_indexes_and_continuations()
            intro_msg = ux.MSG_INTRO_NUMBERED_TEXT[lang]
            send_message_multi(players, intro_msg)
            beginning = game.get_reader_text_beginning()
            for num, cont in enumerate(shuffled_continuations,1):
                cont_msg = "{}: {} *{}*".format(num, beginning, cont)
                send_message_multi(players, cont_msg)
            send_message(reader, ux.MSG_WAIT_FOR_PLAYERS_TO_VOTE_PL[lang])
            numbers_list = list(range(1,game.number_players+1))
            for w in writers:
                w_index = players.index(w)
                w_shuffled_number = shuffled_indexes.index(w_index) + 1
                kb = [[str(i) for i in numbers_list if i != w_shuffled_number]]
                w.set_keyboard(kb)
                send_message(w, ux.MSG_VOTE[lang], kb, sleep=True)
    else:
        if user == reader:
            send_message(user, ux.MSG_WRONG_INPUT_WAIT_FOR_PLAYERS_TO_VOTE[lang])
        else:
            text_input = message_obj.text
            if game.user_has_already_voted(user):
                send_message(user, ux.MSG_ALREADY_VOTED_WAITING_FOR_OTHER_PLAYERS_VOTE[lang])
                return
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                voted_number = int(text_input)
                shuffled_indexes, shuffled_continuations = game.get_players_shuffled_indexes_and_continuations()
                voted_index = shuffled_indexes[voted_number-1]
                remaining_names = game.set_voted_index_and_points_and_get_remaining(user, voted_index)
                all_but_users = [p for p in players if p!=user]
                send_message_multi(all_but_users, ux.MSG_X_VOTED_WAITING_FOR_PLAYERS_VOTE[lang].format(user.get_name(), ', '.join(remaining_names)))
                if len(remaining_names)>0:
                    send_message(user, ux.MSG_THANKS_WAITING_FOR_OTHER_PLAYERS_VOTE[lang], remove_keyboard=True)                    
                else:
                    beginning = game.get_reader_text_beginning()
                    msg_summary = ux.MSG_VOTE_RECAP[lang]
                    send_message_multi(players, msg_summary, remove_keyboard=True)
                    get_shuffled_continuations_voters_name = game.get_shuffled_continuations_voters_name()
                    for i, cont in enumerate(shuffled_continuations,0):
                        author = game.get_player_index(shuffled_indexes[i])
                        author_name = author.get_name()
                        if author==reader:
                            author_name += ' ⭐️'
                        voters_list_name = get_shuffled_continuations_voters_name[i]
                        voters_summay = str(len(voters_list_name))
                        if voters_list_name:
                            voters_summay += " ({})".format(', '.join(voters_list_name))
                        msg_summary = "{} *{}* → {} *{}*\n{} {}".format(i+1, author_name, beginning, cont, ux.MSG_VOTED_BY[lang], voters_summay)
                        send_message_multi(players, msg_summary)
                    msg_point_hand_summary = ux.MSG_POINT_HAND_SUMMARY[lang].format(game.get_hand_point_summary())
                    send_message_multi(players, msg_point_hand_summary)
                    if game.is_last_hand():
                        msg_point_game_summary = ux.MSG_POINT_GAME_SUMMARY[lang].format(game.get_game_point_summary())
                        send_message_multi(players, msg_point_game_summary)
                        players = game.get_players()
                        for p in players:
                            p.current_game_key = None
                        game.state = 'ENDED'
                        game.put()
                        winners_names = game.get_winner_names()
                        winner_msg = ux.MSG_WINNER_SINGULAR[lang] if len(winners_names)==1 else ux.MSG_WINNER_PLURAL[lang]
                        winner_msg = winner_msg.format(', '.join(winners_names))
                        send_message_multi(players, winner_msg)
                        restart_multi(players)
                    else:
                        game.setup_next_hand()
                        redirect_to_state_multi(players, state_GAME_READER_WRITES_BEGINNING)
            else:
                send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang], kb)


def interrupt_game(game, user):
    game.state = 'INTERRUPTED'
    players = game.get_players()
    lang = players[0].language
    for p in players:
        p.current_game_key = None
    if len(players) > 0:
        send_message_multi(players, ux.MSG_EXIT_GAME[lang].format(user.get_name()))
    restart_multi(players)
    game.put()

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
            game = bot_ndb_game.get_game_from_id(int(game_id))
            if game:
                if game.add_player(user):
                    redirect_to_state(user, state_WAITING_FOR_OTHER_PLAYERS)
                else:
                    send_message(user, ux.MSG_NAME_NO_LONGER_AVAILBLE[lang])
            else:
                send_message(user, ux.MSG_NAME_NO_LONGER_AVAILBLE[lang])
        return True
    if user.is_master():
        if text_input == '/test':
            from bot_ndb_base import CLIENT
            fede_user_entry = CLIENT.get(CLIENT.key('User','telegram:130870321'))
            fede_user = NDB_User(entry=fede_user_entry)
            game = fede_user.get_current_game()
            _, players, _, _ = game.get_current_hand_players_reader_writers()
            for p in players:
                p.set_keyboard([['new_test']])
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
    user = NDB_User('telegram', user_obj.id, name, username, language)

    if message_obj.text:
        text_input = message_obj.text
        logging.debug('Message from @{} in state {} with text {}'.format(user.serial_number, user.state, text_input))
        if deal_with_universal_commands(user, text_input):
            return
    repeat_state(user, message_obj=message_obj)

possibles = globals().copy()
possibles.update(locals())

