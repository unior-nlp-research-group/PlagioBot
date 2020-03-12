import logging
from bot_telegram import BOT, send_message, send_typing_action, send_text_document, exception_reporter, report_master
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
import re
import translate

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
        current_game = user.get_current_game()
        if current_game and current_game.sub_state != new_state:
            current_game.set_sub_state(new_state)
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
        msg = '\n'.join([ux.MSG_HOME[lang],ux.MSG_LANGUAGE_INFO[lang],msg_notifications])
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
            elif ' ' in text_input or utility.contains_markdown(text_input):
                send_message(user, ux.MSG_INPUT_CONTAINS_SPACE_OR_MARKDOWN[lang], kb)
                repeat_state(user)
            else:
                room_name = text_input.upper()
                game = Game.get_game_in_initial_state(room_name)
                if game:
                    send_message(user, ux.MSG_GAME_ALREADY_ACTIVE[lang], kb)
                    # send_typing_action(user, sleep_secs=2)
                    repeat_state(user)
                else:
                    game = Game.create_game(room_name, user)
                    user.set_current_game(game)
                    redirect_to_state(user, state_WAITING_FOR_START)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang], kb)

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
                    if Game.add_player(game, user):
                        redirect_to_state(user, state_WAITING_FOR_START)
                    else:
                        send_message(user, ux.MSG_GAME_NOT_AVAILABLE[lang], kb)
                        # send_typing_action(user, sleep_secs=2)
                        repeat_state(user)
                # else:
                #     if Game.get_game_in_started_state(room_name):
                #         send_message(user, ux.MSG_GAME_NAME_ALREADY_STARTED[lang].format(room_name), kb)
                else:
                    send_message(user, ux.MSG_NAME_DOES_NOT_EXIST[lang].format(room_name), kb)
                    # send_typing_action(user, sleep_secs=2)
                    repeat_state(user)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang], kb)

# ================================
# Waiting for game start
# ================================
def state_WAITING_FOR_START(user, message_obj):
    game = user.get_current_game()
    players = game.get_players()
    creator, writers = players[0], players[1:]
    lang = game.language
    creator_name = creator.get_name()
    if message_obj is None:        

        players_names = [p.get_name() for p in players]        
        game_name = ux.MSG_GAME_NAME[lang].format(game.get_name())
        game_settings_info = ux.MSG_GAME_SETTINGS_INFO[lang].format(game.game_type, game.game_control)
        num_players_msg = (ux.MSG_CURRENT_PLAYERS if len(players)>1
            else ux.MSG_CURRENT_PLAYER)[lang].format(
                len(players),', '.join(players_names))

        def send_message_to_writers():
            msg_list = [
                game_name,
                game_settings_info,
                num_players_msg,
                ux.MSG_WAITING_FOR_START_GAME[lang].format(creator_name, game.get_name()),
                ux.MSG_CHAT_INFO[lang]
            ]
            send_message(writers, '\n'.join(msg_list), remove_keyboard=True)

        if user == creator:
            msg_list = [
                game_name,
                game_settings_info,
                num_players_msg
            ]
            kb = [
                [ux.BUTTON_GAME_SETTINGS[lang]]
            ]            
            if len(players) > 1:
                msg_list.append(ux.MSG_CHAT_INFO[lang])
            if len(players) >= parameters.MIN_NUM_OF_PLAYERS:
                msg_list.append(ux.MSG_YOU_CAN_START_GAME[lang])
                kb.insert(0, [ux.BUTTON_START_GAME[lang]])
            else:
                msg_list.append(ux.MSG_WAIT_FOR_MORE_PEOPLE_TO_START[lang])
            if not game.announced:
                kb.append([ux.BUTTON_ANNOUNCE_GAME_PUBLICLY[lang]])
                msg_list.append(ux.MSG_INVITE_OTHER_PLAYERS_ANNOUNCE[lang])
            send_message(creator, '\n'.join(msg_list), kb)
            send_message_to_writers()
        else:
            others_players = [p for p in players if p!=user]
            msg_others = ux.MSG_PLAYER_X_JOINED_GAME[lang].format(user.get_name())
            send_message(others_players, msg_others)

            send_message_to_writers()
            if creator.state == 'state_WAITING_FOR_START':
                repeat_state(creator)
            else:
                pass
                # game creator is changing setting of the game
    else:
        if user == creator:
            text_input = message_obj.text
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_ANNOUNCE_GAME_PUBLICLY[lang]:                    
                    kb.pop() # remove last button (BUTTON_ANNOUNCE_GAME_PUBLICLY)
                    send_message(user, ux.MSG_SENT_ANNOUNCEMENT[lang], kb)
                    command = utility.escape_markdown('/game_{}'.format(game.id))
                    announce_msg = ux.MSG_ANNOUNCE_GAME_PUBLICLY[lang].format(user.get_name(), command)
                    users = User.get_user_lang_state_notification_on(lang, 'state_INITIAL')
                    send_message(users, announce_msg)
                    game.set_announced(True)
                    repeat_state(user)                    
                elif text_input == ux.BUTTON_GAME_SETTINGS[lang]:
                    redirect_to_state(user, state_GAME_SETTINGS)
                elif text_input == ux.BUTTON_START_GAME[lang]:
                    assert len(players) >= parameters.MIN_NUM_OF_PLAYERS
                    if game.setup(user):
                        if game.auto_exercise_mode():
                            game.fill_exercises_automatically()
                            redirect_to_state_multi(players, state_WRITERS_WRITE_ANSWERS)
                        else:
                            redirect_to_state_multi(players, state_READER_WRITES_INCOMPLETE_TEXT)
                    else:
                        send_message(user, ux.MSG_GAME_NOT_AVAILABLE[lang])
                else:
                    assert(False)
            else:
                msg = ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang]
                send_message(user, msg)
        else:
            msg = ux.MSG_WAITING_FOR_START_GAME[lang].format(creator_name, game.get_name())
            send_message(user, msg)

# ================================
# GAME SETTINGS
# ================================
def state_GAME_SETTINGS(user, message_obj):
    lang = user.language
    game = user.get_current_game()
    kb_action = {
        ux.BUTTON_GAME_TYPE[lang]: {
            'row': 0, 'col': 0,
            'info': game.game_type,
            'action': 'redirect_to_state(user, state_SETTINGS_GAME_TYPE)' ,
            'show_button': True,
            'show_description': True,
        },
        ux.BUTTON_GAME_TRANSLATE_HELP[lang]: {
            'row': 2, 'col': 0,
            'info': game.translate_help,
            'action': 'redirect_to_state(user, state_SETTINGS_GAME_TRANSLATE_HELP)' ,
            'show_button': user.is_tester(),
            'show_description': True,
        },
        ux.BUTTON_GAME_CONTROL[lang]: {
            'row': 3, 'col': 0,
            'info': game.game_control,
            'action': 'redirect_to_state(user, state_SETTINGS_GAME_CONTROL)',
            'show_button': True,
            'show_description': True,
        },
        ux.BUTTON_ROUNDS_NUMBER[lang]: {
            'row': 4, 'col': 0,
            'info': ux.MSG_NUM_PLAYERS[lang] if game.game_control=='DEFAULT' else game.num_hands,
            'action': 'redirect_to_state(user, state_SETTINGS_NUMBER_OF_HANDS)',
            'show_button': game.game_control!='DEFAULT',
            'show_description': True,
        },
        ux.BUTTON_BACK[lang]: {
            'row': 5, 'col': 0,
            'info': '',
            'action': 'redirect_to_state(user, state_WAITING_FOR_START)',
            'show_button': True,
            'show_description': False,
        }
    }
    if message_obj is None:
        kb = ux.make_keyboard_from_keyboard_action(kb_action)
        msg = '\n'.join(
            [ux.MSG_SETTINGS_RECAP[lang]] +
            [
                '{} {}: {}'.format(
                    ux.BULLET_SYMBOL,
                    b[re.search("[A-Z]", b).start():],
                    ux.GAME_SETTINGS_BUTTON_VALUE_UX_MAPPING(lang)[b][v['info']] if b in ux.GAME_SETTINGS_BUTTON_VALUE_UX_MAPPING(lang) else v['info']
                )
                for b,v in sorted(kb_action.items(), key=lambda kv:(kv[1]['row'],kv[1]['col']))
                if v['show_description']
            ]
        )
        send_message(user, msg, kb)
    else:
        text_input = message_obj.text
        kb = user.get_keyboard()
        if text_input:
            if text_input in utility.flatten(kb):
                exec(kb_action[text_input]['action'])
            elif ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang], kb)

# ================================
# SETTINGS GAME TYPE
# ================================
def state_SETTINGS_GAME_TYPE(user, message_obj):    
    game = user.get_current_game()
    game_type = game.game_type
    lang = game.language
    _, _, writers = game.get_current_hand_players_reader_writers()
    buttons_value_description = {
        ux.BUTTON_GAME_TYPE_CONTINUATION[lang]: {
            'order': 1,
            'value': 'CONTINUATION',
            'description': ux.MSG_GAME_TYPE_CONTINUATION_DESCR[lang]
        },
        ux.BUTTON_GAME_TYPE_FILL[lang]: {
            'order': 2,
            'value': 'FILL',
            'description': ux.MSG_GAME_TYPE_FILL_DESCR[lang]
        },
        ux.BUTTON_GAME_TYPE_SYNONYM[lang]: {
            'order': 3,
            'value': 'SYNONYM',
            'description': ux.MSG_GAME_TYPE_SYNONYM_DESCR[lang]
        }

    }
    if message_obj is None:
        kb = [
            ux.check_multi_button(buttons_value_description, game_type, multi_line=False),
            [ux.BUTTON_BACK[lang]]
        ]
        msg = '\n'.join([
            ux.MSG_SELECT_GAME_TYPE[lang],
            ux.check_multi_description(buttons_value_description, game_type)
        ])
        send_message(user, msg, kb)
    else:
        game = user.get_current_game()
        text_input = message_obj.text
        kb = user.get_keyboard()
        if text_input:
            if text_input in utility.flatten(kb):
                if text_input.startswith(ux.BUTTON_BACK[lang]):
                    redirect_to_state(user, state_GAME_SETTINGS)
                else:
                    new_game_type = next(
                        v['value'] for b,v in buttons_value_description.items()
                        if text_input.startswith(b)
                    )
                    game.set_game_type(new_game_type)
                    msg = ux.MSG_X_CHANGED_GAME_TYPE_TO_Y[lang].format(user.get_name(), new_game_type)
                    send_message(writers, msg)
                    redirect_to_state(user, state_GAME_SETTINGS)
            elif ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang], kb)


# ================================
# SETTINGS TRANSLATE HELP
# ================================
def state_SETTINGS_GAME_TRANSLATE_HELP(user, message_obj):
    game = user.get_current_game()
    lang = game.language
    translate_help = game.translate_help
    buttons_value_description = {
        ux.BUTTON_YES[lang]: {
            'order': 1,
            'value': True,
        },
        ux.BUTTON_NO[lang]: {
            'order': 2,
            'value': False,
        }
    }
    if message_obj is None:
        kb = [
            ux.check_multi_button(buttons_value_description, translate_help, multi_line=False),
            [ux.BUTTON_BACK[lang]]
        ]
        msg = ux.MSG_GAME_TRANSLATE[lang]
        send_message(user, msg, kb)
    else:
        game = user.get_current_game()
        text_input = message_obj.text
        kb = user.get_keyboard()
        if text_input:
            if text_input in utility.flatten(kb):
                if text_input.startswith(ux.BUTTON_BACK[lang]):
                    redirect_to_state(user, state_GAME_SETTINGS)
                else:
                    new_translate_help = next(
                        v['value'] for b,v in buttons_value_description.items()
                        if text_input.startswith(b)
                    )
                    game.set_translate_help(new_translate_help)
                    redirect_to_state(user, state_GAME_SETTINGS)
            elif ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang], kb)

# ================================
# SETTINGS GAME MODE
# ================================
def state_SETTINGS_GAME_CONTROL(user, message_obj):
    game = user.get_current_game()
    lang = game.language
    game_control = game.game_control
    buttons_value_description = {
        ux.BUTTON_GAME_CONTROL_DEFAULT[lang]: {
            'order': 1,
            'value': 'DEFAULT',
            'description': ux.MSG_GAME_CONTROL_DEFAULT_DESCR[lang]
        },
        ux.BUTTON_GAME_CONTROL_TEACHER[lang]: {
            'order': 2,
            'value': 'TEACHER',
            'description': ux.MSG_GAME_CONTROL_TEACHER_DESCR[lang]
        }
    }
    if message_obj is None:
        kb = [
            ux.check_multi_button(buttons_value_description, game_control, multi_line=False),
            [ux.BUTTON_BACK[lang]]
        ]
        msg = '\n'.join([
            ux.MSG_SELECT_GAME_CONTROL[lang],
            ux.check_multi_description(buttons_value_description, game_control)
        ])
        send_message(user, msg, kb)
    else:
        game = user.get_current_game()
        text_input = message_obj.text
        kb = user.get_keyboard()
        if text_input:
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK[lang]:
                    redirect_to_state(user, state_GAME_SETTINGS)
                else:
                    new_game_control = next(
                        v['value'] for b,v in buttons_value_description.items()
                        if text_input.startswith(b)
                    )
                    game.set_game_control(new_game_control)
                    redirect_to_state(user, state_GAME_SETTINGS)
            elif ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang], kb)

# ================================
# SETTINGS NUMBER OF HANDS (only in teacher mode) # and demo when implemented
# ================================
def state_SETTINGS_NUMBER_OF_HANDS(user, message_obj):
    game = user.get_current_game()
    lang = game.language
    num_hands = game.num_hands
    if message_obj is None:
        default_values = [1, 2, 3, 5, 10]
        if num_hands not in default_values:
            default_values.append(num_hands)
        default_values_str = [str(b) for b in sorted(default_values)]
        buttons_value_description = {
            b: {
                'order': default_values_str.index(b),
                'value': b,
                'description': None
            }
            for b in default_values_str
        }
        kb = [
            ux.check_multi_button(buttons_value_description, str(num_hands), multi_line=False),
            [ux.BUTTON_BACK[lang]]
        ]
        msg = ux.MSG_INSERT_NUMBER_OF_ROUNDS[lang].format(num_hands)
        send_message(user, msg, kb)
    else:
        game = user.get_current_game()
        kb = user.get_keyboard()
        text_input = message_obj.text
        if text_input == ux.BUTTON_BACK[lang]:
            redirect_to_state(user, state_GAME_SETTINGS)
        elif utility.represents_int_between(text_input,1,parameters.MAX_NUM_HANDS):
            number_of_hands = int(text_input)
            game.set_num_hands(number_of_hands)
            redirect_to_state(user, state_GAME_SETTINGS)
        else:
            msg = ux.MSG_WRONG_INPUT_INSRT_NUMBER_BETWEEN[lang].format(1,parameters.MAX_NUM_HANDS)
            send_message(user, msg, kb)

# ================================
# GAME_READER_WRITES_INCOMPLETE_TEXT
# ================================
def state_READER_WRITES_INCOMPLETE_TEXT(user, message_obj):
    game = user.get_current_game()
    hand_number = game.get_hand_number()
    players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = game.language
    if message_obj is None:
        if user == reader:
            if hand_number == 1:
                msg_all = ux.MSG_GAME_HAS_STARTED_WITH_PLAYERS[lang].format(', '.join(game.players_names))
                send_message(players, msg_all, remove_keyboard=True)
                send_message(players, ux.MSG_INSTRUCTIONS[game.game_type][lang])
            msg_intro_list = [ux.MSG_CURRENT_ROUND[lang].format(hand_number)]
            reader_name = ux.MSG_THE_TEACHER[lang] if game.game_control=='TEACHER' else reader.get_name()
            msg_intro = '\n'.join(msg_intro_list)
            send_message(players, msg_intro, remove_keyboard=True)
            msg_reader = ux.MSG_WRITE_INCOMPLETE[game.game_type][lang]
            msg_writers = ux.MSG_WAIT_READER_WRITE_INCOMPLETE[game.game_type][lang].format(reader_name)
            send_message(reader, msg_reader)
            send_message(writers, msg_writers)
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
                # elif game.game_type == 'SYNONYM' and utility.has_parenthesis_in_correct_format(text_input):
                #     send_message(user, ux.MSG_INPUT_NO_SYNONYM[lang], sleep=True)
                else:
                    incomplete_text = text_input.upper()
                    game.set_current_incomplete_text(incomplete_text)
                    redirect_to_state_multi(players, state_READER_WRITES_ANSWER)
            else:
                send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang])
        else:
            reader_name = ux.MSG_THE_TEACHER[lang] if game.game_control=='TEACHER' else reader.get_name()
            msg = ux.MSG_WRONG_INPUT_WAIT_FOR_READER[lang].format(reader_name)
            send_message(user, msg)

# ================================
# GAME_READER_WRITES_ANSWER
# ================================
def state_READER_WRITES_ANSWER(user, message_obj):
    game = user.get_current_game()
    players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = game.language
    reader_name = ux.MSG_THE_TEACHER[lang] if game.game_control=='TEACHER' else reader.get_name()
    if message_obj is None:
        if user == reader:
            msg_reader = ux.MSG_WRITE_CORRECT_ANSWER[game.game_type][lang]
            msg_writers = ux.MSG_WAIT_READER_WRITE_CORRECT_ANSWER[game.game_type][lang].format(reader_name)
            send_message(reader, msg_reader, remove_keyboard=True)
            send_message(writers, msg_writers, remove_keyboard=True)
    else:
        if user == reader:
            text_input = message_obj.text
            if text_input:
                if utility.contains_markdown(text_input):
                    send_message(user, ux.MSG_INPUT_NO_MARKDOWN[lang])
                elif ux.text_is_button_or_digit(text_input):
                    send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang])
                else:
                    answer = text_input.upper()
                    if game.game_type == 'CONTINUATION':
                        answer = utility.normalize_answer(answer)
                    elif game.game_type == 'SYNONYM':
                        inserted_sentence = game.get_current_incomplete_text()
                        freq = inserted_sentence.count(answer)
                        if freq==0:
                            send_message(user, ux.MSG_INPUT_SUBSTITUION_NOT_IN_SENTENCE[lang])
                            return
                        if freq>1:
                            send_message(user, ux.MSG_INPUT_SUBSTITUION_PRESENT_TWICE_OR_MORE_IN_SENTENCE[lang])
                            return
                    game.set_current_completion_text(answer)
                    redirect_to_state_multi(players, state_WRITERS_WRITE_ANSWERS)
            else:
                send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang])
        else:
            msg = ux.MSG_WRONG_INPUT_WAIT_FOR_READER[lang].format(reader_name)
            send_message(user, msg)

# ================================
# GAME_PLAYERS_WRITE_ANSWERS
# ================================
def state_WRITERS_WRITE_ANSWERS(user, message_obj):
    game = user.get_current_game()
    players, reader, writers = game.get_current_hand_players_reader_writers()
    current_completion = game.get_current_completion_text()
    lang = game.language
    if message_obj is None:
        if user == reader:
            msg_reader_list = [ux.MSG_WAIT_WRITERS_WRITE_ANSWERS[game.game_type][lang]]
            msg_writers = ux.MSG_WRITERS_WRITE_ANSWER[game.game_type][lang]
            if game.game_type in ['CONTINUATION','FILL']:
                if game.game_type == 'CONTINUATION':
                    incomplete_text = '*{}*'.format(game.get_current_incomplete_text())
                elif game.game_type == 'FILL':
                    pre_gap, post_gap = game.get_incomplete_text_pre_post_gap()
                    gap = '\\_\\_\\_\\_\\_\\_\\_\\_'
                    incomplete_text = '*{}*{}*{}*'.format(pre_gap, gap, post_gap)
                msg_incomplete_sentence = ux.MSG_PLAYERS_INCOMPLETE_SENTENCE[lang].format(incomplete_text)
            else:
                assert game.game_type == 'SYNONYM'
                incomplete_text = game.get_current_incomplete_text()
                incomplete_text = incomplete_text.replace(current_completion, '*{}*'.format(current_completion))
                msg_incomplete_sentence = ux.MSG_PLAYERS_SENTENCE_WITH_HIGHLITED_SYNONYM[lang].format(incomplete_text)
                msg_writers = msg_writers.format(current_completion)
            if game.translate_help:
                correct_completed_text = ux.render_complete_text(game, current_completion)
                translated_text = translate.get_google_translation(correct_completed_text).upper()
                msg_incomplete_sentence += '\n(*{}*)'.format(translated_text)
            send_message(players, msg_incomplete_sentence, remove_keyboard=True)
                            
            msg_reader_list.append(ux.MSG_STATUS_INSTRUCTIONS[lang])
            if game.game_control == 'TEACHER':
                msg_reader_list.append(ux.MSG_JUMP_TO_NEXT_PHASE[lang])            
            send_message(reader, '\n'.join(msg_reader_list), remove_keyboard=True)
            send_message(writers, msg_writers, remove_keyboard=True)
    else:
        text_input = message_obj.text
        if text_input == '/status':
            remaining_names = game.get_remaining_answers_names()
            remaining_names_str = ', '.join(remaining_names)
            msg_list = [ux.MSG_WAITING_FOR[lang].format(remaining_names_str)]
            if user == reader and game.game_control == 'TEACHER':
                msg_list.append(ux.MSG_JUMP_TO_NEXT_PHASE[lang])
            send_message(user, '\n'.join(msg_list))
            return
        if user == reader:
            if text_input=='/jump' and game.game_control == 'TEACHER':
                send_message(players, ux.MSG_TEACHER_HAS_JUMPED_TO_NEXT_PHASE[lang], remove_keyboard=True)
                redirect_to_state_multi(players, state_WRITERS_SELECT_BEST_ANSWER)
            else:
                send_message(user, ux.MSG_WRONG_INPUT_WAIT_FOR_PLAYERS_TO_ANSWER[lang])
            return        
        if game.has_player_already_written_answer(user):
            send_message(user, ux.MSG_ALREADY_SENT_ANSWER[lang])
            return
        if text_input:
            if ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang])
            else:
                answer = text_input.upper()
                if utility.contains_markdown(answer):
                    send_message(user, ux.MSG_INPUT_NO_MARKDOWN[lang])
                else:
                    if game.game_type == 'CONTINUATION':
                        answer = utility.normalize_answer(answer)
                    elif game.game_type == 'SYNONYM':
                        if answer == current_completion:
                            send_message(user, ux.MSG_INPUT_NO_VALID_SYNONYM[lang])
                            return
                    remaining_players_num = game.set_player_text_answer_and_get_remaining(user, answer)
                    tx_msg = ux.MSG_THANKS_YOU_ENTERED_X[lang].format(answer)
                    if remaining_players_num==0:                        
                        send_message(user, tx_msg, sleep=True)
                        send_message(players, ux.MSG_ALL_ANSWERS_RECEIVED[lang], remove_keyboard=True)
                        redirect_to_state_multi(players, state_WRITERS_SELECT_BEST_ANSWER)
                    else:
                        msg_list = [tx_msg, ux.MSG_WAIT_TILL_YOUR_TURN[lang], ux.MSG_STATUS_INSTRUCTIONS[lang]]
                        send_message(user, '\n'.join(msg_list))                        
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang])

# ================================
# GAME_PLAYERS_SELECT_BEST_ANSWERS
# ================================
def state_WRITERS_SELECT_BEST_ANSWER(user, message_obj):
    game = user.get_current_game()
    players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = game.language

    if message_obj is None:
        if user != reader:
            return
        game.prepare_voting() # setup variables
        correct_author_indexes = game.get_correct_answers_authors_indexes()
        correct_players = [players[i] for i in correct_author_indexes]
        correct_players_names = [p.get_name() for p in correct_players]
        all_answered_correctly = len(correct_author_indexes) == len(players) - 1
        shuffled_answers_info = game.get_shuffled_answers_info(include_no_vote=False)
        received_unique_answers_num = len(shuffled_answers_info)
        players_min_num_votes = received_unique_answers_num - 1 # subtricting her own answer (if no answer we would have more)
        
        if game.is_voting_no_or_multiple_answers_allowed():
            players_min_num_votes += 1
        
        if received_unique_answers_num == 0:
            msg = ux.MSG_NO_ANSWER_GOING_TO_NEXT_ROUND[lang]
            send_message(players, msg)
            game.prepare_hand_poins_and_get_points_feedbacks()
            redirect_to_state_multi(players, state_NEXT_HAND)
            return
        if len(correct_players)>0:
            exact_answers_names_str = ', '.join(correct_players_names)
            if len(correct_players)==1:
                msg = ux.MSG_X_PLAYER_SG_GUESSED_EXACT_ANSWERS[lang].format(exact_answers_names_str)
            else:
                msg = ux.MSG_X_PLAYERS_PL_GUESSED_EXACT_ANSWERS[lang].format(exact_answers_names_str)
            send_message(players, msg)
        if all_answered_correctly:
            msg = ux.MSG_NO_SELECTION_ALL_GUESSED_CORRECTLY[lang]
            send_message(players, msg)
            recap_votes(game)
            return
        if players_min_num_votes == 1:
            msg = ux.MSG_NO_SELECTION_ONLY_ONE_OPTION[lang]
            send_message(players, msg)
            if game.game_control == 'TEACHER':
                redirect_to_state_multi(players, state_TEACHER_VALIDATION)
            else:
                recap_votes(game)
            return
        number_answers = len(shuffled_answers_info)
        intro_msg = ux.MSG_INTRO_NUMBERED_TEXT[lang]
        send_message(players, intro_msg)
        all_num_completed_answers = []
        for num, answer_info in enumerate(shuffled_answers_info,1):
            answer = answer_info['answer']
            num_completed_answers = '{}: '.format(num) + \
                ux.render_complete_text(game, answer)
            all_num_completed_answers.append(num_completed_answers)
        all_num_completed_answers_str = '\n\n'.join(all_num_completed_answers)
        send_message(players, all_num_completed_answers_str)
        game.set_var('ALL_NUM_COMPLETED_ANSWERS', all_num_completed_answers_str)
        msg_reader_list = [
            ux.MSG_WAIT_FOR_PLAYERS_TO_SELECT_PL[lang], 
            ux.MSG_STATUS_INSTRUCTIONS[lang]
        ]
        if game.game_control == 'TEACHER':
            msg_reader_list.append(ux.MSG_JUMP_TO_NEXT_PHASE[lang])
        send_message(reader, '\n'.join(msg_reader_list))
        numbers_list = list(range(1,number_answers+1))

        for w in writers:
            p_index = players.index(w)
            player_answer_info = next((a for a in shuffled_answers_info if p_index in a['authors']), None)
            if game.game_control != 'TEACHER' and p_index in correct_author_indexes:
                w.set_var('NO_VOTE', True, save=False)                
                msg_list = [
                    ux.MSG_CORRECT_ANSWER_NO_SELECTION[lang], 
                    ux.MSG_WAIT_TILL_YOUR_TURN[lang], 
                    ux.MSG_STATUS_INSTRUCTIONS[lang]
                ]
                send_message(w, '\n'.join(msg_list), remove_keyboard=True)
            else:                                
                player_voting_optinos = [
                    str(i) for i in numbers_list
                    if player_answer_info and i != player_answer_info['shuffled_number']
                ]
                assert len(player_voting_optinos)>0
                w.set_var('NO_VOTE', False, save=False)
                kb = utility.distribute_elements(player_voting_optinos)
                if game.is_voting_no_or_multiple_answers_allowed():
                    kb.append([ux.BUTTON_NO_CORRECT_ANSWER[lang]])
                send_message(w, ux.MSG_SELECTION[game.game_type][lang], kb, sleep=True)
    else:
        # tx_msg = ux.MSG_THANKS_YOU_ENTERED_X[lang].format(text_input)        
        text_input = message_obj.text
        if text_input == '/status':
            remaining_names = game.get_names_remaining_voters()
            remaining_names_str = ', '.join(remaining_names)
            msg_list = [ux.MSG_WAITING_FOR[lang].format(remaining_names_str)]
            if user == reader and game.game_control == 'TEACHER':
                msg_list.append(ux.MSG_JUMP_TO_NEXT_PHASE[lang])
            send_message(user, '\n'.join(msg_list))
            return
        if user == reader:
            if text_input=='/jump' and game.game_control == 'TEACHER':
                send_message(players, ux.MSG_TEACHER_HAS_JUMPED_TO_NEXT_PHASE[lang])
                redirect_to_state_multi(players, state_TEACHER_VALIDATION)
            else:
                send_message(user, ux.MSG_WRONG_INPUT_WAIT_FOR_PLAYERS_TO_SELECT[lang])
            return        
        if user.get_var('NO_VOTE'):
            msg = ux.MSG_WRONG_INPUT_WAIT_FOR_PLAYERS_TO_SELECT[lang]
            send_message(user, msg)
            return
        if game.has_user_already_voted(user):
            send_message(user, ux.MSG_ALREADY_SELECTED_WAITING_FOR[lang].format(remaining_names_str))
            return
        kb = user.get_keyboard()
        if text_input in utility.flatten(kb):
            if text_input == ux.BUTTON_NO_CORRECT_ANSWER[lang]:
                assert game.is_voting_no_or_multiple_answers_allowed()
                voted_shuffled_number = -1
            else:
                voted_shuffled_number = int(text_input)
            remaining_players_num = game.set_voted_indexes_and_get_remaining(user, voted_shuffled_number)
            tx_msg = ux.MSG_THANKS_YOU_SELECTED_X[lang].format(text_input)
            if remaining_players_num==0:                        
                send_message(user, tx_msg, remove_keyboard=True, sleep=True)
                send_message(players, ux.MSG_ALL_ANSWERS_RECEIVED[lang])
                if game.game_control == 'TEACHER':
                    redirect_to_state_multi(players, state_TEACHER_VALIDATION)
                else:
                    recap_votes(game)
            else:
                msg_list = [tx_msg, ux.MSG_WAIT_TILL_YOUR_TURN[lang], ux.MSG_STATUS_INSTRUCTIONS[lang]]
                send_message(user, '\n'.join(msg_list))                       
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang], kb)

# ================================
# GAME_TEACHER_VALIDATION
# ================================
def state_TEACHER_VALIDATION(user, message_obj):
    game = user.get_current_game()
    _, reader, writers = game.get_current_hand_players_reader_writers()
    lang = game.language
    shuffled_answers_info = game.get_shuffled_answers_info(include_no_vote=False)
    number_answers = len(shuffled_answers_info)
    msg_or_none = ux.MSG_OR_NONE[lang] \
        if game.is_voting_no_or_multiple_answers_allowed() \
        else ''
    if message_obj is None:
        if user == reader:
            # teacher
            user.set_var('CORRECT_ANSWERS_NUMBERS', [])
            numbers_list = [str(i) for i in list(range(1,number_answers+1))]
            kb = utility.distribute_elements(numbers_list) # should exclude the original one
            if game.is_voting_no_or_multiple_answers_allowed():
                kb.append([ux.BUTTON_NO_CORRECT_ANSWER_NO_EMOJI[lang]])
            if game.game_type == 'SYNONYM':
                incomplete_text, original_completion = game.get_current_incomplete_text_and_original_completion()
                completed_text = incomplete_text.replace(original_completion, '*{}*'.format(original_completion))
                msg = ux.MSG_TEACHER_ORIGINAL_TEXT[lang].format(completed_text)
                send_message(user, msg, kb, sleep=True)
            msg_list = [
                ux.MSG_RECAP_STUDENTS_ANSWERS[lang], 
                game.get_var('ALL_NUM_COMPLETED_ANSWERS'),
                ux.MSG_TEACHER_SELECT[lang].format(msg_or_none)
            ]
            send_message(user, '\n'.join(msg_list), kb, sleep=True)
            send_message(writers, ux.MSG_WAIT_FOR_TEACHER_EVALUATION[lang], remove_keyboard=True)
    else:
        if user != reader:
            send_message(user, ux.MSG_WRONG_INPUT_WAIT_FOR_TEACHER_TO_SELECT[lang])
        else:
            text_input = message_obj.text
            if text_input == '/recap_answers':
                send_message(user, game.get_var('ALL_NUM_COMPLETED_ANSWERS'))
                return
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                CORRECT_ANSWERS_NUMBERS = user.get_var('CORRECT_ANSWERS_NUMBERS')
                if text_input == ux.BUTTON_SUBMIT[lang]:
                    game.set_correct_answers(CORRECT_ANSWERS_NUMBERS)
                    recap_votes(game)
                else:
                    if text_input.endswith(ux.BUTTON_NO_CORRECT_ANSWER_NO_EMOJI[lang]):
                        assert game.is_voting_no_or_multiple_answers_allowed()
                        if -1 in CORRECT_ANSWERS_NUMBERS:
                            CORRECT_ANSWERS_NUMBERS.pop()
                        else:
                            for _ in range(len(CORRECT_ANSWERS_NUMBERS)):
                                CORRECT_ANSWERS_NUMBERS.pop()
                            CORRECT_ANSWERS_NUMBERS.append(-1)
                    else:
                        if text_input.startswith('⭐'):
                            CORRECT_ANSWERS_NUMBERS.remove(int(text_input[1:]))
                        else:
                            CORRECT_ANSWERS_NUMBERS.append(int(text_input))
                            if -1 in CORRECT_ANSWERS_NUMBERS:
                                CORRECT_ANSWERS_NUMBERS.remove(-1)
                    numbers_list = list(range(1,number_answers+1))
                    starred_number_list = [
                        '⭐{}'.format(n) if n in CORRECT_ANSWERS_NUMBERS else '{}'.format(n)
                        for n in numbers_list
                    ]
                    kb = utility.distribute_elements(starred_number_list)
                    if CORRECT_ANSWERS_NUMBERS:
                        # if there are stars
                        if game.is_voting_no_or_multiple_answers_allowed():
                            NONE_BUTTON = ux.BUTTON_NO_CORRECT_ANSWER_NO_EMOJI[lang]
                            if -1 in CORRECT_ANSWERS_NUMBERS:
                                msg_or_none = ''
                                NONE_BUTTON = '⭐' + NONE_BUTTON
                            else:
                                pass
                            kb.append([NONE_BUTTON])
                        kb.append([ux.BUTTON_SUBMIT[lang]])                        
                        seleced = ', '.join([
                            str(x) if x!=-1 else ux.MSG_NO_ANSWER[lang]
                            for x in sorted(CORRECT_ANSWERS_NUMBERS)
                        ])
                        msg_selected = ux.MSG_TEACHER_YOU_SELECTED[lang].format(seleced)
                        msg_select_or_submit = ux.MSG_TEACHER_SELECT_OR_SUBMIT[lang].format(msg_or_none)
                        msg_list = [msg_selected, msg_select_or_submit, ux.MSG_RECAP_INSTRUCTION[lang]]
                    else:
                        msg_list = [
                            ux.MSG_TEACHER_SELECT[lang].format(msg_or_none), 
                            ux.MSG_RECAP_INSTRUCTION[lang]
                        ]
                        if game.is_voting_no_or_multiple_answers_allowed():
                            kb.append([ux.BUTTON_NO_CORRECT_ANSWER_NO_EMOJI[lang]])
                    send_message(user, '\n'.join(msg_list), kb)
            else:
                send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang], kb)

# ================================
# UTIL FUNCTION TO RECAP VOTES
# ================================
def recap_votes(game):
    lang = game.language
    players, _, writers = game.get_current_hand_players_reader_writers()
    include_no_vote = game.is_voting_no_or_multiple_answers_allowed()
    shuffled_answers_info = game.get_shuffled_answers_info(include_no_vote)
    msg_list = [
        ux.MSG_ANSWERS_RECAP_PL[lang]
        if game.is_voting_no_or_multiple_answers_allowed()
        else ux.MSG_ANSWERS_RECAP_SG[lang]
    ]
    for answer_info in shuffled_answers_info:
        answer = answer_info['answer']
        voters_names = [players[i].get_name() for i in answer_info['voted_by']]
        num_voters_and_names = str(len(voters_names))
        num = answer_info['shuffled_number']
        if voters_names:
            num_voters_and_names += ": {}".format(', '.join(voters_names))
        if answer == parameters.NO_ANSWER_KEY: # no vote
            answer_report = ("❌ ⭐️ → {}" if answer_info['correct'] \
                else "❌ → {}").format(ux.MSG_NO_ANSWER[lang])
        else:
            complete_text = ux.render_complete_text(game, answer)
            answer_report = ("{} ⭐️ → {}" if answer_info['correct'] \
                else "{} → {}").format(num, complete_text)
            authors_names = [players[i].get_name() for i in answer_info['authors']]
            if authors_names:
                authors_names_str = ', '.join(authors_names)
                answer_report += '\n' + ux.MSG_WRITTEN_BY[lang].format(authors_names_str)
        answer_report += '\n' + ux.MSG_SELECTED_BY[lang].format(num_voters_and_names)
        msg_list.append(answer_report)
    send_message(players, '\n\n'.join(msg_list), remove_keyboard=True)
    
    # send points feedback
    points_feedbacks = game.prepare_hand_poins_and_get_points_feedbacks()
    for w in writers:
        p_index = players.index(w)
        p_feedback = points_feedbacks[p_index]
        msg_points_correct_answer = ux.MSG_POINT_SG_PL(parameters.POINTS['CORRECT_ANSWER'])[lang]
        msg_points_incorrect_answer = ux.MSG_POINT_SG_PL(parameters.POINTS['INCORRECT_ANSWER'])[lang]
        msg_points_no_answer = ux.MSG_POINT_SG_PL(parameters.POINTS['NO_ANSWER'])[lang]
        msg_points_correct_selection = ux.MSG_POINT_SG_PL(parameters.POINTS['CORRECT_SELECTION'])[lang]
        msg_points_no_selection = ux.MSG_POINT_SG_PL(parameters.POINTS['NO_SELECTION'])[lang]
        
        msg_list = [ux.MSG_YOUR_POINTS[lang]]
        
        if p_feedback['ANSWERED_CORRECTLY']:
            msg_list.append(ux.MSG_CORRECT_ANSWER[lang].format(msg_points_correct_answer))
        elif p_feedback['NO_ANSWER']:
            msg_list.append(ux.MSG_NO_GIVEN_ANSWER[lang].format(msg_points_no_answer))
        else:
            msg_list.append(ux.MSG_WRONG_ANSWER[lang].format(msg_points_incorrect_answer))
        
        if p_feedback['SELECTED_CORRECTLY']:
            msg_list.append(ux.MSG_CORRECT_SELECTION[lang].format(msg_points_correct_selection))
        else:            
            if game.game_control == 'TEACHER':
                if p_feedback['NO_SELECTION']:                          
                    msg_points_no_selection = ux.MSG_POINT_SG_PL(parameters.POINTS['INCORRECT_SELECTION'])[lang]
                    msg_list.append(ux.MSG_NO_GIVEN_SELECTION[lang].format(msg_points_no_selection))
                elif not p_feedback['ANSWERED_CORRECTLY']:
                    msg_points_incorrect_selection = ux.MSG_POINT_SG_PL(parameters.POINTS['INCORRECT_SELECTION'])[lang]
                    msg_list.append(ux.MSG_WRONG_SELECTION_PENALTY[lang].format(msg_points_incorrect_selection))
            else:
                msg_list.append(ux.MSG_WRONG_SELECTION_NO_PENALTY[lang])
        #else no voting took place
            
        if game.game_control != 'TEACHER':
            received_votes = p_feedback['NUM_VOTES_RECEIVED']
            received_votes_total_points = received_votes * parameters.POINTS['RECEIVED_VOTE']
            msg_received_votes_total_points = ux.MSG_POINT_SG_PL(received_votes_total_points)[lang]
            msg_list.append(ux.MSG_RECEIVED_VOTES[lang].format(msg_received_votes_total_points))
        
        send_message(w, '\n'.join(msg_list))

    send_message(players, ux.MSG_POINT_ROUND_SUMMARY[lang])            
    game.send_hand_point_img_data(players)
    if game.is_last_hand():
        send_message(players, ux.MSG_POINT_GAME_SUMMARY[lang])
        game.send_game_point_img_data(players, save=True)
        winners_names = game.get_winner_names()
        winner_msg = ux.MSG_WINNER_SINGULAR[lang] if len(winners_names)==1 else ux.MSG_WINNER_PLURAL[lang]
        winner_msg = winner_msg.format(', '.join(winners_names))
        send_message(players, winner_msg)
        end_game(game, players)
    else:
        redirect_to_state_multi(players, state_NEXT_HAND)
        # send_message(players, ux.MSG_POINT_GAME_PARTIAL_SUMMARY[lang])
        # game.send_game_point_img_data(players)
        

# ================================
# SETUP NEXT ROUND
# ================================
def state_NEXT_HAND(user, message_obj):
    game = user.get_current_game()
    players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = game.language
    reader_name = ux.MSG_THE_TEACHER[lang] if game.game_control=='TEACHER' else reader.get_name()
    if message_obj is None:
        if user == reader:
            kb = [[ux.BUTTON_NEXT_ROUND[lang]]]
            send_message(user, ux.MSG_NEXT_ROUND[lang], kb)                        
            msg_writers = ux.MSG_WAIT_FOR_X_TO_START_NEXT_ROUND[lang].format(reader_name)
            send_message(writers, msg_writers)
    else:
        if user != reader:            
            send_message(user, ux.MSG_WRONG_INPUT_WAIT_FOR_X_TO_START_NEXT_ROUND[lang].format(reader_name))
        else:
            text_input = message_obj.text
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                assert text_input == ux.BUTTON_NEXT_ROUND[lang]
                game.setup_next_hand(user)
                if game.auto_exercise_mode():                            
                    redirect_to_state_multi(players, state_WRITERS_WRITE_ANSWERS)
                else:
                    redirect_to_state_multi(players, state_READER_WRITES_INCOMPLETE_TEXT)
            else:
                send_message(user, ux.MSG_WRONG_INPUT_USE_BUTTONS[lang], kb)


def end_game(game, players):
    for p in players:
        p.current_game_id = None
    game.set_state('ENDED')
    restart_multi(players)

def interrupt_game(game, user=None):
    game.set_state('INTERRUPTED')
    players = game.get_players()
    lang = game.language
    for p in players:
        p.current_game_id = None
    if len(players) > 0:
        if user:
            send_message(players, ux.MSG_EXIT_GAME[lang].format(user.get_name()), remove_keyboard=True)
        else:
            send_message(players, ux.MSG_EXIT_GAME_EXPIRED[lang], remove_keyboard=True)
    restart_multi(players)

def deal_with_universal_commands(user, text_input):
    #logging.debug('In universal command with input "{}". User is master: {}'.format(text_input, user.is_master()))
    lang = user.language
    if text_input == '/forcedstart':
        restart_user(user)
        return True
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
    if text_input == '/exit':
        game = user.get_current_game()
        if game:
            lang = game.language
            players = game.get_players()
            if parameters.ONLY_GAME_CREATOR_CAN_TERMINATE_GAME:
                if user == players[0]:
                    # only game creator can terminate it
                    interrupt_game(game, user)
                else:
                    send_message(user, ux.MSG_ONLY_CREATOR_CAN_TERMINATE_GAME[lang])
            elif user in players:
                interrupt_game(game, user)
            else:
                # game deleted
                user.current_game_id = None
                restart_user(user)
        else:
            send_message(user, ux.MSG_NO_GAME_TO_EXIT[lang])
        return True
    if text_input == ('/chat'):
        send_message(user, ux.MSG_ERROR_CHAT_INFO[lang])
        return True
    if text_input.startswith('/chat '):
        game = user.get_current_game()
        lang = game.language
        chat_msg = ' '.join(text_input.split()[1:])
        if game:
            if len(text_input)>500:
                send_message(user, ux.MSG_CHAT_MSG_TOO_LONG[lang])
            if utility.contains_markdown(text_input):
                send_message(user, ux.MSG_CHAT_MSG_NO_MARKDOWN[lang])
            else:
                players = game.get_players()
                send_message(players, "📩 *{}*: {}".format(user.get_name(), chat_msg))
        else:
            send_message(user, ux.MSG_NO_GAME_NO_CHAT[lang])
        return True
    if text_input.startswith('/game_'):
        if user.current_game_id:
            send_message(user, ux.MSG_CANT_JOIN_ALREADY_IN_GAME[lang])
            return True
        game_id = text_input.split('/game_')[1]
        game = Game.get(game_id)
        lang = game.language
        if game:
            if game.add_player(user):
                redirect_to_state(user, state_WAITING_FOR_START)
            else:
                send_message(user, ux.MSG_GAME_NOT_AVAILABLE[lang])
        else:
            send_message(user, ux.MSG_CANT_JOIN_GAME[lang])
        return True
    if text_input == '/refresh':
        repeat_state(user)
        return True
    if user.is_master():
        if text_input == '/debug':
            import json
            game = user.get_current_game()
            send_text_document(user, 'tmp_vars.json', json.dumps(game.variables))
            return True
        if text_input == '/image':
            from bot_telegram import send_photo_from_data
            import render_leaderboard
            img_data = render_leaderboard.test()
            send_photo_from_data(user, 'test.png', img_data, caption='test')
            return True
        if text_input.startswith('/translate '):
            import translate
            text_input = text_input.split(' ',1)[1]
            t = translate.get_google_translation(text_input)
            send_message(user, t)
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

