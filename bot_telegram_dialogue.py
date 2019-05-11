import logging
from bot_telegram import BOT, send_message, send_messages, send_typing_action, send_text_document, send_message_multi, send_messages_multi, exception_reporter, report_master
import utility
import bot_ui as ux
import telegram
import bot_firestore_user
from bot_firestore_user import User
import bot_firestore_game
from bot_firestore_game import Game
import utility
import time
import parameters

# ================================
# CONFIG
# ================================
DEBUG = False

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
        user.set_state(new_state)
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
        msg = "⚠️ User {} sent to unknown method state: {}".format(user.serial_id, state)
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
            [ux.BUTTON_NEW_GAME[lang], ux.BUTTON_JOIN_GAME[lang]],
            [ux.BUTTON_CHANGE_LANGUAGE[lang], ux.BUTTON_INFO[lang]]
        ]
        notifications_button = [ux.BUTTON_DISABLE_NOTIFICATIONS[lang]] if user.notifications else [ux.BUTTON_ENABLE_NOTIFICATIONS[lang]]
        kb.append(notifications_button)
        msg_notifications = ux.MSG_NOTIFICATIONS_ON[lang] if user.notifications else ux.MSG_NOTIFICATIONS_OFF[lang]
        msg = '\n\n'.join([ux.MSG_HOME[lang],ux.MSG_LANGUAGE_INFO[lang],msg_notifications])
        send_message(user, msg, kb)
    else:
        text_input = message_obj.text
        kb = user.get_keyboard()
        if text_input in utility.flatten(kb):
            if text_input == ux.BUTTON_NEW_GAME[lang]:
                redirect_to_state(user, state_NEW_ROOM_NAME)
            elif text_input == ux.BUTTON_JOIN_GAME[lang]:
                redirect_to_state(user, state_JOIN_ROOM_NAME)                
            elif text_input == ux.BUTTON_INFO[lang]:
                send_message(user, ux.MSG_INFO[lang])
            elif text_input == ux.BUTTON_CHANGE_LANGUAGE[lang]:
                user.switch_language()
                repeat_state(user)
            elif text_input in [ux.BUTTON_DISABLE_NOTIFICATIONS[lang], ux.BUTTON_ENABLE_NOTIFICATIONS[lang]]:
                user.switch_notifications()
                repeat_state(user)
            else:
                assert(False)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_BUTTONS[lang], kb)


# ================================
# Join Room Name
# ================================
def state_JOIN_ROOM_NAME(user, message_obj):
    lang = user.language
    if message_obj is None:
        kb = [[ux.BUTTON_BACK[lang]]]
        send_message(user, ux.MSG_CHOOSE_EXITING_GAME_NAME[lang], kb)
    else:
        text_input = message_obj.text
        kb = user.get_keyboard()
        if text_input:
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK[lang]:
                    restart_user(user)
                else:
                    assert(False)
            elif ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)
            else:
                room_name = text_input.upper()
                game = Game.get_game_in_initial_state(room_name)
                if game:
                    if game.just_created():
                        send_message(user, ux.MSG_GAME_NOT_YET_READY[lang].format(room_name), kb)
                        send_typing_action(user, sleep_secs=2)
                        repeat_state(user)
                    elif Game.add_player(game, user):
                        redirect_to_state(user, state_WAITING_FOR_OTHER_PLAYERS)
                    else:
                        send_message(user, ux.MSG_GAME_ALREADY_STARTED[lang], kb)
                        send_typing_action(user, sleep_secs=2)
                        repeat_state(user)
                # else:
                #     if Game.get_game_in_started_state(room_name):
                #         send_message(user, ux.MSG_GAME_NAME_ALREADY_STARTED[lang].format(room_name), kb)
                else:
                    send_message(user, ux.MSG_NAME_DOES_NOT_EXIST[lang].format(room_name), kb)                
                    send_typing_action(user, sleep_secs=2)
                    repeat_state(user)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang], kb)

# ================================
# New Room Name
# ================================
def state_NEW_ROOM_NAME(user, message_obj):
    lang = user.language
    if message_obj is None:
        kb = [[ux.BUTTON_BACK[lang]]]
        send_message(user, ux.MSG_CHOOSE_NEW_GAME_NAME[lang], kb)
    else:
        text_input = message_obj.text
        kb = user.get_keyboard()
        if text_input:
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK[lang]:
                    restart_user(user)
                else:
                    assert(False)
            elif ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)
            else:
                room_name = text_input.upper()
                game = Game.get_game_in_initial_state(room_name)
                if game:
                    send_message(user, ux.MSG_GAME_ALREADY_ACTIVE[lang], kb)
                    send_typing_action(user, sleep_secs=2)
                    repeat_state(user)
                else:
                    game = Game.create_game(room_name, user.id)
                    user.set_current_game(game)
                    redirect_to_state(user, state_CHOOSE_NUMBER_PLAYERS)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang], kb)

# ================================
# Choose number of players
# ================================
def state_CHOOSE_NUMBER_PLAYERS(user, message_obj):
    lang = user.language
    kb = [['3','4','5','6'],[ux.BUTTON_ABORT[lang]]]
    if message_obj is None:
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
        if utility.represents_int_between(text_input,parameters.MIN_NUM_OF_PLAYERS,100):
            max_num_players = int(text_input)
            game.set_max_number_of_players(max_num_players)            
            redirect_to_state(user, state_SELECT_GAME_MODE)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_INSRT_NUMBER[lang], kb)


# ================================
# Select game mode
# ================================
def state_SELECT_GAME_MODE(user, message_obj):
    lang = user.language
    # todo: insert demo mode
    kb = [[ux.BUTTON_MODE_DEFAULT[lang], ux.BUTTON_MODE_TEACHER[lang]],[ux.BUTTON_ABORT[lang]]]
    if message_obj is None:
        send_message(user, ux.MSG_SELECT_GAME_MODE[lang], kb)
    else:
        game = user.get_current_game()
        text_input = message_obj.text
        if text_input:
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_ABORT[lang]:
                    interrupt_game(game, user)
                    restart_user(user)
                elif text_input == ux.BUTTON_MODE_DEFAULT[lang]:
                    game.set_game_mode("DEFAULT")
                    redirect_to_state(user, state_SELECT_GAME_TYPE)
                else:
                    assert text_input == ux.BUTTON_MODE_TEACHER[lang]
                    game.set_game_mode("TEACHER")
                    redirect_to_state(user, state_INSERT_NUMBER_OF_HANDS)
            elif ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)                
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang], kb)

# ================================
# Insert number of hands (only in tacher mode and demo)
# ================================
def state_INSERT_NUMBER_OF_HANDS(user, message_obj):
    lang = user.language
    kb = [['1','2','3','5','10'],[ux.BUTTON_ABORT[lang]]]
    if message_obj is None:
        send_message(user, ux.MSG_INSER_NUMBER_OF_HANDS[lang], kb)
    else:
        game = user.get_current_game()
        text_input = message_obj.text
        if text_input == ux.BUTTON_ABORT[lang]:
            interrupt_game(game, user)
        elif utility.represents_int(text_input):
            number_of_hands = int(text_input)
            game.set_num_hands(number_of_hands)            
            redirect_to_state(user, state_SELECT_GAME_TYPE)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_INSRT_NUMBER[lang], kb)

# ================================
# Select game mode
# ================================
def state_SELECT_GAME_TYPE(user, message_obj):
    lang = user.language
    kb = [[ux.BUTTON_TYPE_COMPLETION[lang], ux.BUTTON_TYPE_FILL[lang]],[ux.BUTTON_ABORT[lang]]]
    if message_obj is None:
        send_message(user, ux.MSG_SELECT_GAME_TYPE[lang], kb)
    else:
        game = user.get_current_game()
        text_input = message_obj.text
        if text_input:
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_ABORT[lang]:
                    interrupt_game(game, user)
                    restart_user(user)
                else:
                    if text_input == ux.BUTTON_TYPE_COMPLETION[lang]:
                        game.set_game_type("COMPLETION")
                        redirect_to_state(user, state_WAITING_FOR_OTHER_PLAYERS)
                    else:
                        assert text_input == ux.BUTTON_TYPE_FILL[lang]
                        game.set_game_type("FILL")
                        redirect_to_state(user, state_SELECT_GAME_REWARD_MODE)
            elif ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)                
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang], kb)

# ================================
# Select game mode
# ================================
def state_SELECT_GAME_REWARD_MODE(user, message_obj):
    lang = user.language
    kb = [[ux.BUTTON_REWARD_MODE_CREATIVITY[lang], ux.BUTTON_REWARD_MODE_EXACTNESS[lang]],[ux.BUTTON_ABORT[lang]]]
    if message_obj is None:
        send_message(user, ux.MSG_SELECT_GAME_REWARD_MODE[lang], kb)
    else:
        game = user.get_current_game()
        text_input = message_obj.text
        if text_input:
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_ABORT[lang]:
                    interrupt_game(game, user)
                    restart_user(user)
                else:
                    if text_input == ux.BUTTON_REWARD_MODE_CREATIVITY[lang]:
                        game.set_game_reward_mode("CREATIVITY")
                        redirect_to_state(user, state_WAITING_FOR_OTHER_PLAYERS)
                    else:
                        assert text_input == ux.BUTTON_REWARD_MODE_EXACTNESS[lang]
                        game.set_game_reward_mode("EXACTNESS")
                        redirect_to_state(user, state_WAITING_FOR_OTHER_PLAYERS)
            elif ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)                
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang], kb)


# ================================
# Enter special rules
# ================================
# def state_ENTER_SPECIAL_RULES(user, message_obj):
#     lang = user.language
#     kb = [[ux.BUTTON_SKIP[lang]],[ux.BUTTON_ABORT[lang]]]
#     if message_obj is None:
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
#             elif ux.text_is_button_or_digit(text_input):
#                 send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)
#             else:
#                 game.set_var('SPECIAL_RULES',text_input)
#                 redirect_to_state(user, state_WAITING_FOR_OTHER_PLAYERS)
#         else:
#             send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang], kb)

# ================================
# Waiting for game start
# ================================
def state_WAITING_FOR_OTHER_PLAYERS(user, message_obj):    
    game = user.get_current_game()
    players = game.get_players()
    # logging.debug("players[0]: {}".format(players[0]))
    lang = players[0].language    
    if message_obj is None:
        msg = ux.MSG_ENTERING_GAME_X[lang].format(game.get_name())
        send_message(user, msg, remove_keyboard=True)        
        # logging.debug("user: {}".format(user))
        # logging.debug("user == players[0]: {}".format(user == players[0]))
        if user == players[0]:
            kb = [
                [ux.BUTTON_ANNOUNCE_GAME_PUBLICLY[lang]],
                [ux.BUTTON_STOP_WAITING_START_GAME[lang]]
            ]
            msg_invite = ux.MSG_INVITE_PEOPLE_ANNOUNCE_OR_START[lang].format(game.get_name())
            send_message(user, msg_invite, kb)            
        else:
            msg_other_players = ux.MSG_PLAYER_X_JOINED_GAME[lang].format(user.get_name())
            send_message_multi(players, msg_other_players)
            get_available_seats = game.get_available_seats()
            if get_available_seats==0:
                send_message_multi(players, ux.MSG_READY_TO_START[lang])
                # special_rules = game.get_var('SPECIAL_RULES')
                # if special_rules:
                #     creator_name = players[0].get_name()
                #     special_rules_msg = ux.MSG_TELL_SPECIAL_RULES[lang].format(creator_name, special_rules)
                #     send_message_multi(players, special_rules_msg)
                if game.setup(user):
                    redirect_to_state_multi(players, state_GAME_READER_WRITES_BEGINNING)
                else:
                    send_message(user, ux.MSG_GAME_ALREADY_STARTED[lang])
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
                if text_input == ux.BUTTON_ANNOUNCE_GAME_PUBLICLY[lang]:
                    # send_message(user, ux.MSG_FEATURE_NOT_YET_IMPLEMENTED[lang])
                    kb = [[ux.BUTTON_STOP_WAITING_START_GAME[lang]]]
                    send_message(user, ux.MSG_SENT_ANNOUNCEMENT[lang], kb)
                    command = utility.escape_markdown('/game_{}'.format(game.id))
                    announce_msg = ux.MSG_ANNOUNCE_GAME_PUBLICLY[lang].format(user.get_name(), game.max_num_players, get_available_seats, command)
                    users = User.get_user_lang_state_notification_on(lang, 'state_INITIAL')
                    send_message_multi(users, announce_msg)
                elif text_input == ux.BUTTON_STOP_WAITING_START_GAME[lang]:
                    if len(players) >= parameters.MIN_NUM_OF_PLAYERS:
                        if game.setup(user):
                            redirect_to_state_multi(players, state_GAME_READER_WRITES_BEGINNING)
                            return
                        else:
                            send_message(user, ux.MSG_GAME_ALREADY_STARTED[lang])
                            return
                    else:
                        send_message(user, ux.MSG_NOT_ENOUGH_PLAYERS[lang])                        
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
    hand = game.get_hand_number()
    players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = players[0].language
    if message_obj is None:
        if hand == 1:
            msg_all = ux.MSG_GAME_HAS_STARTED_WITH_PLAYERS[lang].format(', '.join(game.players_names))
            send_message(user, msg_all, remove_keyboard=True)        
        if user == players[0]:
            msg_intro = ux.MSG_HAND_INFO[lang].format(hand, reader.get_name())
            send_message_multi(players, msg_intro)
            if game.game_type == 'COMPLETION':
                msg_reader = ux.MSG_READER_WRITES_BEGINNING[lang]
                msg_writers = ux.MSG_WRITERS_WAIT_READER_BEGINNING[lang].format(reader.get_name())
            else:
                assert game.game_type == 'FILL'
                msg_reader = ux.MSG_READER_WRITES_SENTENCE_WITH_GAP[lang]
                msg_writers = ux.MSG_WRITERS_WAIT_READER_SENTENCE_WITH_GAP[lang].format(reader.get_name())
            send_message(reader, msg_reader)            
            send_message_multi(writers, msg_writers)
    else:
        if user == reader:
            text_input = message_obj.text
            if text_input:
                if ux.text_is_button_or_digit(text_input):
                    send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang])
                elif utility.contains_markdown(text_input):
                    send_message(user, ux.MSG_INPUT_NO_MARKDOWN[lang])
                elif len(text_input) < parameters.MIN_BEGINNING_LENGTH:
                    send_message(user, ux.MSG_INPUT_TOO_SHORT[lang], sleep=True)
                elif game.game_type == 'FILL' and '???' not in text_input:
                    send_message(user, ux.MSG_INPUT_NO_GAP[lang], sleep=True)
                else:
                    incomplete_text = text_input.upper()
                    game.set_current_incomplete_text(incomplete_text)
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
    players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = players[0].language
    if message_obj is None:
        if user == players[0]:
            kb = [[ux.BUTTON_SKIP[lang]]]
            msg_reader = ux.MSG_READER_WRITES_TEXT_INFO[lang]
            send_message(reader, msg_reader, kb)    
            msg_writers = ux.MSG_WRITERS_WAIT_READER_TEXT_INFO[lang].format(reader.get_name())
            send_message_multi(writers, msg_writers)            
    else:
        if user == reader:
            text_input = message_obj.text
            kb = user.get_keyboard()
            if text_input:
                if text_input in utility.flatten(kb):
                    if text_input == ux.BUTTON_SKIP[lang]:
                        game.set_incomplete_text_info('')
                        redirect_to_state_multi(players, state_GAME_PLAYERS_WRITE_CONTINUATIONS)
                    else:
                        assert(False)                
                elif utility.contains_markdown(text_input):
                    send_message(user, ux.MSG_INPUT_NO_MARKDOWN[lang])
                elif ux.text_is_button_or_digit(text_input):
                    send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)
                elif len(text_input) < parameters.MIN_TEXT_INFO_LENGTH:
                    send_message(user, ux.MSG_INPUT_TOO_SHORT[lang])
                else:
                    game.set_incomplete_text_info(text_input)
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
    players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = players[0].language
    if message_obj is None:
        if user == players[0]:
            if game.game_type == 'COMPLETION':
                incomplete_text = '*{}*'.format(game.get_current_incomplete_text())
                msg_intro = ux.MSG_PLAYERS_BEGINNING_INTRO[lang].format(reader.get_name())
                msg_reader = ux.MSG_READER_WRITE_CORRECT_CONTINUATION[lang]
                msg_writers = ux.MSG_WRITERS_WRITE_CONTINUATION[lang].format(reader.get_name())
            else:
                assert game.game_type == 'FILL'
                pre_gap, post_gap = game.get_incomplete_text_pre_post_gap()
                gap = '\\_\\_\\_\\_\\_\\_\\_\\_'
                incomplete_text = '*{}*{}*{}*'.format(pre_gap, gap, post_gap)
                msg_intro = ux.MSG_PLAYERS_SENTENCE_WITH_GAP_INTRO[lang].format(reader.get_name())            
                msg_reader = ux.MSG_READER_WRITE_CORRECT_MISSING_PART[lang]
                msg_writers = ux.MSG_WRITERS_WRITE_MISSING_PART[lang].format(reader.get_name())
            send_messages_multi(players, [msg_intro, incomplete_text], remove_keyboard=True)
            text_info = game.get_incomplete_text_info()
            if text_info:
                msg_players = ux.MSG_WRITERS_TEXT_INFO[lang].format(text_info)
                send_message_multi(players, msg_players, remove_keyboard=True)
            send_message(reader, msg_reader, remove_keyboard=True)
            send_message_multi(writers, msg_writers, remove_keyboard=True)
    else:
        text_input = message_obj.text
        if game.has_player_already_written_completion(user):
            send_message(user, ux.MSG_ALREADY_SENT_CONTINUATION[lang])
            return
        if text_input:
            if ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang])            
            else:
                continuation = text_input.upper()
                if game.game_type == 'COMPLETION':
                    continuation = utility.normalize_continuation(continuation)                
                if utility.contains_markdown(continuation):
                    send_message(user, ux.MSG_INPUT_NO_MARKDOWN[lang])
                else:
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
    players, reader, writers = game.get_current_hand_players_reader_writers()
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
        incomplete_text = game.get_current_incomplete_text()
        msg_summary = ux.MSG_VOTE_RECAP[lang]
        send_message_multi(players, msg_summary, remove_keyboard=True)
        shuf_cont_voters_names = game.get_shuffled_continuations_voters()                
        for i, cont in enumerate(shuffled_continuations):
            if game.game_type == 'COMPLETION':
                completed_text = "{} *{}*".format(incomplete_text, cont)
            else:
                assert game.game_type == 'FILL'
                pre_gap, post_gap = game.get_incomplete_text_pre_post_gap()
                completed_text = '{}*{}*{}'.format(pre_gap, cont, post_gap)
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
                msg_summary = "{} *{}* ⭐️ → {}\n{}".format(
                    i+1, reader.get_name(), completed_text, \
                    ux.MSG_GUESSED_BY_AND_VOTED_BY[lang].format(guessers_summary, voters_summay))
            else:
                author_names = ', '.join(p.get_name() for p in authors)
                msg_summary = "{} *{}* → {}\n{}".format(
                    i+1, author_names, completed_text, ux.MSG_VOTED_BY[lang].format(voters_summay))
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
            game.setup_next_hand(user)
            redirect_to_state_multi(players, state_GAME_READER_WRITES_BEGINNING)

    if message_obj is None:
        if user == players[0]:
            if len(exact_guessers)>0:
                exact_guessers_names_str = ', '.join(exact_guessers_names)
                if len(exact_guessers)==1:
                    msg = ux.MSG_X_PLAYER_SG_GUESSED_EXACT_CONTINUATIONS[lang].format(exact_guessers_names_str)
                else:
                    msg = ux.MSG_X_PLAYERS_PL_GUESSED_EXACT_CONTINUATIONS[lang].format(exact_guessers_names_str)
                send_message_multi(players, msg)
            if all_guessed_correctly:
                recap_votes()
                return            
            #report_master("player_to_shuffled_cont_index: {}".format(player_to_shuffled_cont_index))
            #report_master("shuffled_continuations: {}".format(shuffled_continuations))
            number_continuations = len(shuffled_continuations)
            intro_msg = ux.MSG_INTRO_NUMBERED_TEXT[lang]
            send_message_multi(players, intro_msg)
            incomplete_text = game.get_current_incomplete_text()
            for num, cont in enumerate(shuffled_continuations,1):
                if game.game_type == 'COMPLETION':
                    num_completed_text = "{}: {} *{}*".format(num, incomplete_text, cont)
                else:
                    assert game.game_type == 'FILL'
                    pre_gap, post_gap = game.get_incomplete_text_pre_post_gap()
                    num_completed_text = '{}: {}*{}*{}'.format(num, pre_gap, cont, post_gap)
                send_message_multi(players, num_completed_text)
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
                    send_message(w, ux.MSG_VOTE[lang], kb, sleep=True)
    else:
        if user == reader:
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
    game.set_state('ENDED')
    restart_multi(players)

def interrupt_game(game, user):
    game.set_state('INTERRUPTED')
    players = game.get_players()
    lang = players[0].language
    for p in players:
        p.current_game_id = None
    if len(players) > 0:
        send_message_multi(players, ux.MSG_EXIT_GAME[lang].format(user.get_name()))
    restart_multi(players)

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
            players = game.get_players()
            if user == players[0]:
                # only game creator can terminate it
                interrupt_game(game, user)
            else:
                send_message(user, ux.MSG_ONLY_CREATOR_CAN_TERMINATE_GAME[lang])
        else:
            send_message(user, ux.MSG_NO_GAME_TO_EXIT[lang])
        return True
    if text_input.startswith('/chat '):
        game = user.get_current_game()
        chat_msg = ' '.join(text_input.split()[1:])
        if game:
            if len(text_input)>200:
                send_message(user, ux.MSG_CHAT_MSG_TOO_LONG[lang])    
            else:
                players = game.get_players()
                other_players = [p for p in players if p != user]
                if other_players:
                    send_message_multi(other_players, "📩 *{}*: {}".format(user.get_name(), chat_msg))
                    send_message(user, ux.MSG_CHAT_SENT[lang])
                else:
                    send_message(user, ux.MSG_CHAT_NO_PLAYERS_IN_ROOM[lang])
        else:
            send_message(user, ux.MSG_NO_GAME_NO_CHAT[lang])
        return True
    if text_input.startswith('/game_'):
        if user.current_game_id:
            send_message(user, ux.MSG_CANT_JOIN_ALREADY_IN_GAME[lang])
            return True
        game_id = text_input.split('/game_')[1]
        game = Game.get(game_id)
        if game:
            if game.add_player(user):
                redirect_to_state(user, state_WAITING_FOR_OTHER_PLAYERS)
            else:
                send_message(user, ux.MSG_NAME_NO_LONGER_AVAILBLE[lang])
        else:
            send_message(user, ux.MSG_WRONG_COMMAND[lang])
        return True
    if user.is_master():
        if text_input == '/debug':
            import json
            game = user.get_current_game()
            send_text_document(user, 'tmp_vars.json', json.dumps(game.variables))
            return True
        if text_input == '/refresh':
            repeat_state(user)
            return True
        if text_input == '/image':
            from bot_telegram import send_photo_from_data
            import render_leaderboard
            img_data = render_leaderboard.test()
            send_photo_from_data(user, 'test.png', img_data, caption='test')
            return True
        if text_input.startswith('/test '):
            repetitions = int(text_input.split()[1])
            for i in range(repetitions):
                send_message(user, "Test {}".format(i+1))
                time.sleep(1)
            return True
        if text_input.startswith('/markdown '):
            text = ' '.join(text_input.split()[1:])
            send_message(user, text)
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
        logging.debug('Message from @{} in state {} with text {}'.format(user.serial_id, user.state, text_input))
        if DEBUG and not user.is_tester():
            send_message(user, ux.MSG_WORK_IN_PROGRESS[user.language])
            return
        if deal_with_universal_commands(user, text_input):
            return
        repeat_state(user, message_obj=message_obj)
    else:
        send_message(user, ux.MSG_WRONG_INPUT_ONLY_TEXT_ACCEPTED[user.language])

possibles = globals().copy()
possibles.update(locals())

