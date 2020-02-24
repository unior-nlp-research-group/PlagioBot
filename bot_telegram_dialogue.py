import logging
from bot_telegram import BOT, send_message, send_typing_action, send_text_document, send_message_multi, exception_reporter, report_master
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
    # logging.debug("players[0]: {}".format(players[0]))
    lang = game.language    
    if message_obj is None:
        msg = ux.MSG_ENTERING_GAME_X[lang].format(game.get_name())
        send_message(user, msg, remove_keyboard=True)        
        # logging.debug("user: {}".format(user))
        # logging.debug("user == players[0]: {}".format(user == players[0]))
        if user == players[0]:
            kb = [                
                [ux.BUTTON_START_GAME[lang]],
                [ux.BUTTON_GAME_SETTINGS[lang]]
            ]
            players_names = [p.get_name() for p in players]
            msg = (ux.MSG_CURRENT_PLAYERS if len(players)>1 else ux.MSG_CURRENT_PLAYERS)[lang].format(
                len(players),', '.join(players_names)) + '\n\n'
            if not game.announced:
                kb.append([ux.BUTTON_ANNOUNCE_GAME_PUBLICLY[lang]])
                msg += ux.MSG_INVITE_PEOPLE_ANNOUNCE_OR_START[lang].format(game.get_name())
            else:
                msg += ux.MSG_INVITE_PEOPLE_START[lang].format(game.get_name())
            send_message(user, msg, kb)
        else:
            msg_other_players = ux.MSG_PLAYER_X_JOINED_GAME[lang].format(user.get_name())
            other_players = [p for p in players if p != user]
            send_message_multi(other_players, msg_other_players)
            msg_waiting = ux.MSG_WAITING_FOR_START_GAME[lang].format(game.get_name())
            send_message_multi(players, msg_waiting)
    else:
        if user == players[0]:
            text_input = message_obj.text
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_ANNOUNCE_GAME_PUBLICLY[lang]:
                    game.set_announced(True)
                    kb = [[ux.BUTTON_START_GAME[lang]]]
                    send_message(user, ux.MSG_SENT_ANNOUNCEMENT[lang], kb)
                    command = utility.escape_markdown('/game_{}'.format(game.id))
                    announce_msg = ux.MSG_ANNOUNCE_GAME_PUBLICLY[lang].format(user.get_name(), command)
                    users = User.get_user_lang_state_notification_on(lang, 'state_INITIAL')
                    send_message_multi(users, announce_msg)
                    repeat_state(user)
                elif text_input == ux.BUTTON_GAME_SETTINGS[lang]:
                    redirect_to_state(user, state_GAME_SETTINGS)                    
                elif text_input == ux.BUTTON_START_GAME[lang]:
                    if len(players) >= parameters.MIN_NUM_OF_PLAYERS:
                        if game.setup(user):
                            redirect_to_state_multi(players, state_GAME_READER_WRITES_BEGINNING)
                        else:
                            send_message(user, ux.MSG_GAME_NOT_AVAILABLE[lang])
                    else:
                        send_message(user, ux.MSG_NOT_ENOUGH_PLAYERS[lang])                        
                else:
                    assert(False)
            else:
                msg = ux.MSG_WAITING_FOR_START_GAME[lang].format(game.get_name())
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
        ux.BUTTON_GAME_DEMO_MODE[lang]: {
            'row': 1, 'col': 0,
            'info': game.demo_mode,
            'action': 'redirect_to_state(user, state_SETTINGS_DEMO_MODE)' ,
            'show_button': True,
            'show_description': True,
        },
        ux.BUTTON_GAME_TRANSLATE_HELP[lang]: {
            'row': 2, 'col': 0,
            'info': game.translate_help,
            'action': 'redirect_to_state(user, state_SETTINGS_GAME_TRANSLATE_HELP)' ,
            'show_button': True,
            'show_description': True,
        },
        ux.BUTTON_GAME_CONTROL[lang]: {
            'row': 3, 'col': 0,
            'info': game.game_control,
            'action': 'redirect_to_state(user, state_SETTINGS_GAME_CONTROL)',
            'show_button': True,
            'show_description': True,
        },
        ux.BUTTON_REWARD_MODE[lang]: {
            'row': 4, 'col': 0,
            'info': game.game_reward_mode,
            'action': 'redirect_to_state(user, state_SETTINGS_GAME_REWARD_MODE)',
            'show_button': True,
            'show_description': True,
        },
        ux.BUTTON_SPECIAL_RULES[lang]: {
            'row': 5, 'col': 0,
            'info': game.special_rules if game.special_rules else ux.BUTTON_NO[lang],
            'action': 'redirect_to_state(user, state_SETTINGS_SPECIAL_RULES)',
            'show_button': True,
            'show_description': True,
        },
        ux.BUTTON_HANDS_NUMBER[lang]: {
            'row': 6, 'col': 0,
            'info': ux.MSG_NUM_PLAYERS[lang] if game.game_control=='DEFAULT' else game.num_hands,
            'action': 'redirect_to_state(user, state_SETTINGS_NUMBER_OF_HANDS)',
            'show_button': game.game_control!='DEFAULT',
            'show_description': True,
        },
        ux.BUTTON_ASK_EXTRA_INFO[lang]: {
            'row': 7, 'col': 0,
            'info': game.ask_text_info,
            'action': 'redirect_to_state(user, state_SETTINGS_ASK_TEXT_INFO)',
            'show_button': True,
            'show_description': True,
        },
        ux.BUTTON_BACK[lang]: {
            'row': 8, 'col': 0,
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
    lang = user.language
    game = user.get_current_game()
    game_type = game.game_type
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
        ux.BUTTON_GAME_TYPE_SUBSTITUTION[lang]: {
            'order': 3,
            'value': 'SUBSTITUTION',
            'description': ux.MSG_GAME_TYPE_SUBSTITUTION_DESCR[lang]            
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
                    redirect_to_state(user, state_GAME_SETTINGS)
            elif ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)                
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang], kb)

# ================================
# SETTINGS DEMO MODE
# ================================
def state_SETTINGS_DEMO_MODE(user, message_obj):
    lang = user.language
    game = user.get_current_game()
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
        msg = ux.MSG_GAME_DEMO_MODE[lang]
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
                    new_demo_mode = next(
                        v['value'] for b,v in buttons_value_description.items() 
                        if text_input.startswith(b)
                    )
                    game.set_demo_mode(new_demo_mode)                        
                    redirect_to_state(user, state_GAME_SETTINGS)
            elif ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)                
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang], kb)

# ================================
# SETTINGS TRANSLATE HELP
# ================================
def state_SETTINGS_GAME_TRANSLATE_HELP(user, message_obj):
    lang = user.language
    game = user.get_current_game()
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
    lang = user.language    
    game = user.get_current_game()
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
        # todo: insert demo mode
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
# SETTINGS GAME REWARD MODE (only for fill the gap)
# ================================
def state_SETTINGS_GAME_REWARD_MODE(user, message_obj):
    lang = user.language
    game = user.get_current_game()
    game_reward_mode = game.game_reward_mode
    buttons_value_description = {
        ux.BUTTON_REWARD_MODE_CREATIVITY[lang]: {
            'order': 1,
            'value': 'CREATIVITY',
            'description': ux.MSG_GAME_REWARD_MODE_CREATIVITY_DESCR[lang]
        },
        ux.BUTTON_REWARD_MODE_EXACTNESS[lang]: {
            'order': 2,
            'value': 'EXACTNESS',
            'description': ux.MSG_GAME_REWARD_MODE_EXACTNESS_DESCR[lang]            
        }
    }
    kb = [
        ux.check_multi_button(buttons_value_description, game_reward_mode, multi_line=False),
        [ux.BUTTON_BACK[lang]]
    ]
    if message_obj is None:
        msg = '\n'.join([
            ux.MSG_SELECT_GAME_REWARD_MODE[lang],
            ux.check_multi_description(buttons_value_description, game_reward_mode)
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
                    new_game_reward_mode = next(
                        v['value'] for b,v in buttons_value_description.items() 
                        if text_input.startswith(b)
                    )
                    game.set_game_reward_mode(new_game_reward_mode)
                    redirect_to_state(user, state_GAME_SETTINGS)
            elif ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)                
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang], kb)

# ================================
# SETTINGS NUMBER OF HANDS (only in tacher mode and demo)
# ================================
def state_SETTINGS_NUMBER_OF_HANDS(user, message_obj):
    lang = user.language
    game = user.get_current_game()
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
        msg = ux.MSG_INSERT_NUMBER_OF_HANDS[lang].format(num_hands)
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
# SETTINGS GAME REWARD MODE (only for fill the gap)
# ================================
def state_SETTINGS_ASK_TEXT_INFO(user, message_obj):
    lang = user.language
    game = user.get_current_game()
    ask_text_info = game.ask_text_info
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
    kb = [
        ux.check_multi_button(buttons_value_description, ask_text_info, multi_line=False),
        [ux.BUTTON_BACK[lang]]
    ]
    if message_obj is None:
        msg = ux.MSG_ENABLE_TEXT_INFO[lang]
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
                    new_ask_text_info = next(
                        v['value'] for b,v in buttons_value_description.items() 
                        if text_input.startswith(b)
                    )
                    game.set_ask_text_info(new_ask_text_info)
                    redirect_to_state(user, state_GAME_SETTINGS)
            elif ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)                
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang], kb)            

# ================================
# SETTINGS SPECIAL RULES
# ================================
def state_SETTINGS_SPECIAL_RULES(user, message_obj):
    lang = user.language
    game = user.get_current_game()
    special_rules = game.special_rules
    if message_obj is None:
        kb = [
            [ux.BUTTON_BACK[lang]]
        ]    
        msg = ux.MSG_WRITE_GAME_SPECIAL_RULES[lang]
        if special_rules:
            kb.insert(0, [ux.BUTTON_REMOVE[lang]])            
            msg += '\n\n' + ux.MSG_CURRENT_GAME_SPECIAL_RULES[lang].format(special_rules)
        send_message(user, msg, kb)
    else:
        game = user.get_current_game()
        text_input = message_obj.text
        kb = user.get_keyboard()            
        if text_input:            
            if text_input in utility.flatten(kb):
                if text_input == ux.BUTTON_BACK[lang]:
                    redirect_to_state(user, state_GAME_SETTINGS)
                elif text_input == ux.BUTTON_REMOVE[lang]:
                    game.set_special_rules('')
                    redirect_to_state(user, state_GAME_SETTINGS)
                else:
                    assert(False)
            elif ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang], kb)
            else:
                game.set_special_rules(text_input)
                redirect_to_state(user, state_GAME_SETTINGS)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang], kb)

# ================================
# GAME_READER_WRITES_BEGINNING
# ================================
def state_GAME_READER_WRITES_BEGINNING(user, message_obj):
    game = user.get_current_game()
    hand = game.get_hand_number()
    players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = game.language
    if message_obj is None:        
        if user == players[0]:
            if hand == 1:
                msg_all = ux.MSG_GAME_HAS_STARTED_WITH_PLAYERS[lang].format(', '.join(game.players_names))
                send_message_multi(players, msg_all, remove_keyboard=True)
                special_rules = game.special_rules
                if special_rules:
                    creator_name = players[0].get_name()
                    special_rules_msg = ux.MSG_TELL_SPECIAL_RULES[lang].format(creator_name, special_rules)
                    send_message_multi(players, special_rules_msg)
            msg_intro = ux.MSG_HAND_INFO[lang].format(hand, reader.get_name())
            send_message_multi(players, msg_intro)
            if game.game_type == 'CONTINUATION':
                msg_reader = ux.MSG_READER_WRITES_BEGINNING[lang]
                msg_writers = ux.MSG_WRITERS_WAIT_READER_BEGINNING[lang].format(reader.get_name())
            elif game.game_type == 'FILL':
                msg_reader = ux.MSG_READER_WRITES_SENTENCE_WITH_GAP[lang]
                msg_writers = ux.MSG_WRITERS_WAIT_READER_SENTENCE_WITH_GAP[lang].format(reader.get_name())
            else:
                assert game.game_type == 'SUBSTITUTION'
                msg_reader = ux.MSG_READER_WRITES_SENTENCE_WITH_SUBSTITUTION[lang]
                msg_writers = ux.MSG_WRITERS_WAIT_READER_SENTENCE_WITH_SUBSTITUTION[lang].format(reader.get_name())
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
                # elif game.game_type == 'SUBSTITUTION' and utility.has_parenthesis_in_correct_format(text_input):
                #     send_message(user, ux.MSG_INPUT_NO_SUBSTITUTION[lang], sleep=True)
                else:
                    incomplete_text = text_input
                    game.set_current_incomplete_text(incomplete_text)
                    if game.ask_text_info:                        
                        redirect_to_state_multi(players, state_GAME_READER_WRITES_TEXT_INFO)
                    else:
                        redirect_to_state_multi(players, state_GAME_READER_WRITES_ANSWER)                        
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
    lang = game.language
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
                        redirect_to_state_multi(players, state_GAME_READER_WRITES_ANSWER)
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
                    redirect_to_state_multi(players, state_GAME_READER_WRITES_ANSWER)
            else:
                send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang])
        else:
            msg = ux.MSG_WRONG_INPUT_WAIT_FOR_READER[lang].format(reader.get_name())
            send_message(user, msg)


# ================================
# GAME_READER_WRITES_ANSWER
# ================================
def state_GAME_READER_WRITES_ANSWER(user, message_obj):
    game = user.get_current_game()
    players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = game.language
    if message_obj is None:
        if user == players[0]:
            if game.game_type in ['CONTINUATION', 'FILL']:
                msg_reader = ux.MSG_READER_WRITE_CORRECT_ANSWER[lang]
                send_message(reader, msg_reader, remove_keyboard=True)    
                msg_writers = ux.MSG_WRITERS_WAIT_READER_WRITE_CORRECT_ANSWER[lang].format(reader.get_name())
                send_message_multi(writers, msg_writers)            
            elif game.game_type == 'SUBSTITUTION':
                msg_reader = ux.MSG_READER_WRITE_SUBSTITUTION_PART[lang]
                send_message(reader, msg_reader, remove_keyboard=True)    
                msg_writers = ux.MSG_WRITERS_WAIT_READER_WRITE_SUBSTITUTION_PART[lang].format(reader.get_name())
                send_message_multi(writers, msg_writers)            
    else:
        if user == reader:
            text_input = message_obj.text
            if text_input:                
                if utility.contains_markdown(text_input):
                    send_message(user, ux.MSG_INPUT_NO_MARKDOWN[lang])
                elif ux.text_is_button_or_digit(text_input):
                    send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang])
                else:
                    answer = text_input
                    if game.game_type == 'CONTINUATION':
                        answer = utility.normalize_answer(answer)                
                    elif game.game_type == 'SUBSTITUTION':
                        inserted_sentence = game.get_current_incomplete_text()
                        if not utility.validate_substring_presence(inserted_sentence, text_input):                            
                            send_message(user, ux.MSG_INPUT_SUBSTITUION_NOT_IN_SENTENCE[lang])
                            return
                    game.set_player_text_answer_and_get_remaining(user, answer)
                    redirect_to_state_multi(players, state_GAME_PLAYERS_WRITE_ANSWERS)                    
            else:
                send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang])
        else:
            msg = ux.MSG_WRONG_INPUT_WAIT_FOR_READER[lang].format(reader.get_name())
            send_message(user, msg)

# ================================
# GAME_PLAYERS_WRITE_ANSWERS
# ================================
def state_GAME_PLAYERS_WRITE_ANSWERS(user, message_obj):
    game = user.get_current_game()
    players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = game.language
    if message_obj is None:
        if user == players[0]:
            if game.game_type in ['CONTINUATION','FILL']:
                if game.game_type == 'CONTINUATION':
                    incomplete_text = '*{}*'.format(game.get_current_incomplete_text())
                elif game.game_type == 'FILL':                
                    pre_gap, post_gap = game.get_incomplete_text_pre_post_gap()
                    gap = '\\_\\_\\_\\_\\_\\_\\_\\_'
                    incomplete_text = '*{}*{}*{}*'.format(pre_gap, gap, post_gap)
                msg_incomplete_sentence = ux.MSG_PLAYERS_INCOMPLETE_SENTENCE[lang].format(incomplete_text.upper())
            else:
                assert game.game_type == 'SUBSTITUTION'
                incomplete_text = game.get_current_incomplete_text()
                substitution = game.get_correct_answers()[0]
                incomplete_text = incomplete_text.replace(substitution, '*{}*'.format(substitution))
                msg_incomplete_sentence = ux.MSG_PLAYERS_SENTENCE_WITH_HIGHLITED_SUBSTITUTION[lang].format(incomplete_text.upper())
            if game.translate_help:
                correct_completed_text = ux.render_complete_text(game, 
                    game.get_current_incomplete_text(), game.get_correct_answers()[0],
                    markdown=False, uppercase=False)
                translated_text = translate.get_google_translation(correct_completed_text).upper()
                msg_incomplete_sentence += '\n(*{}*)'.format(translated_text)
            send_message_multi(players, msg_incomplete_sentence, remove_keyboard=True)
            text_info = game.get_incomplete_text_info()            
            if text_info:                
                msg_players = ux.MSG_WRITERS_TEXT_INFO[lang].format(text_info)
                send_message_multi(players, msg_players, remove_keyboard=True)
            if game.game_type in ['CONTINUATION','FILL']:
                msg_reader = ux.MSG_READER_WAIT_WRITERS_WRITE_ANSWER[lang]
                msg_writers = ux.MSG_WRITERS_WRITE_ANSWER[lang]
            else:
                assert game.game_type == 'SUBSTITUTION'
                msg_reader = ux.MSG_READER_WAIT_WRITERS_WRITE_SUBSTITUTION[lang]
                msg_writers = ux.MSG_WRITERS_WRITE_SUBSTITUTION[lang]
            send_message(reader, msg_reader, remove_keyboard=True)
            send_message_multi(writers, msg_writers, remove_keyboard=True)
    else:
        text_input = message_obj.text
        if game.has_player_already_written_answer(user):
            send_message(user, ux.MSG_ALREADY_SENT_ANSWER[lang])
            return
        if text_input:
            if ux.text_is_button_or_digit(text_input):
                send_message(user, ux.MSG_WRONG_BUTTON_INPUT[lang])            
            else:
                answer = text_input                
                if utility.contains_markdown(answer):
                    send_message(user, ux.MSG_INPUT_NO_MARKDOWN[lang])
                else:
                    if game.game_type == 'CONTINUATION':
                        answer = utility.normalize_answer(answer) 
                    elif game.game_type == 'SUBSTITUTION':
                        correct_answer = game.get_correct_answers()[0]
                        if text_input == correct_answer:
                            send_message(user, ux.MSG_INPUT_NO_VALID_SUBSTITUTION[lang])
                            return
                    remaining_names = game.set_player_text_answer_and_get_remaining(user, answer)
                    if len(remaining_names)>0:
                        all_but_users = [p for p in players if p!=user]
                        remaining_names_str = ', '.join(remaining_names)
                        send_message(user, ux.MSG_THANKS[lang], remove_keyboard=True)
                        send_message(user, ux.MSG_WAIT_FOR[lang].format(remaining_names_str), remove_keyboard=True)
                        logging.debug("Remainig names ({}): {}".format(len(remaining_names), remaining_names_str))
                        send_message_multi(all_but_users, ux.MSG_X_GAVE_ANSWER_WAITING_FOR_PLAYERS_NAMES[lang].format(user.get_name(), remaining_names_str))                
                    else:
                        game.prepare_voting()
                        redirect_to_state_multi(players, state_GAME_VOTE_ANSWER)
        else:
            send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT[lang])

# ================================
# GAME_PLAYERS_VOTE_ANSWERS 
# ================================
def state_GAME_VOTE_ANSWER(user, message_obj):
    game = user.get_current_game()
    players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = game.language
    exact_answers_indexes = game.get_exact_answers_indexes()
    exact_answers_players = [players[i] for i in exact_answers_indexes]
    exact_answers_names = [p.get_name() for p in exact_answers_players]
    all_guessed_correctly = len(exact_answers_indexes) == len(players) - 1
    all_but_one_guessed_correctly = len(exact_answers_indexes) == len(players) - 2
    shuffled_answers = game.get_shuffled_answers()

    remaining_names = game.get_names_remaining_voters()
    remaining_names_str = ', '.join(remaining_names)

    if message_obj is None:
        if user == players[0]:
            if len(exact_answers_players)>0:                
                exact_answers_names_str = ', '.join(exact_answers_names)
                if len(exact_answers_players)==1:
                    msg = ux.MSG_X_PLAYER_SG_GUESSED_EXACT_ANSWERS[lang].format(exact_answers_names_str)
                else:
                    msg = ux.MSG_X_PLAYERS_PL_GUESSED_EXACT_ANSWERS[lang].format(exact_answers_names_str)
                send_message_multi(players, msg)
            if all_guessed_correctly:
                msg = ux.MSG_NO_VOTE_ALL_GUESSED_CORRECTLY[lang]
                send_message_multi(players, msg)
                recap_votes(user, game)
                return     
            elif all_but_one_guessed_correctly:  
                msg = ux.MSG_NO_VOTE_ALL_BUT_ONE_GUESSED_CORRECTLY[lang]
                send_message_multi(players, msg)
                recap_votes(user, game)
                return     
            number_answers = len(shuffled_answers)
            intro_msg = ux.MSG_INTRO_NUMBERED_TEXT[lang]
            send_message_multi(players, intro_msg)
            incomplete_text = game.get_current_incomplete_text()
            all_num_completed_answers = []
            for num, answer in enumerate(shuffled_answers,1):
                # if game.game_type == 'SUBSTITUTION' and num==r_shuffled_number:
                #     continue
                num_completed_answers = '{}: '.format(num) + ux.render_complete_text(game, incomplete_text, answer)                
                all_num_completed_answers.append(num_completed_answers)
            all_num_completed_answers_str = '\n\n'.join(all_num_completed_answers)
            send_message_multi(players, all_num_completed_answers_str)
            game.set_var('ALL_NUM_COMPLETED_ANSWERS', all_num_completed_answers_str)            
            send_message(reader, ux.MSG_WAIT_FOR_PLAYERS_TO_VOTE_PL[lang])
            numbers_list = list(range(1,number_answers+1))            
            
            for w in writers:
                w_index = players.index(w)

                w_shuffled_number = game.get_answer_shuffled_index(w_index) + 1
                if game.game_control != 'TEACHER' and w_index in exact_answers_indexes:    
                    send_message(w, ux.MSG_GUESSED_NO_VOTE[lang], remove_keyboard=True)
                    send_message(w, ux.MSG_WAIT_FOR[lang].format(remaining_names_str), remove_keyboard=True)
                else:
                    kb = [[str(i) for i in numbers_list if i != w_shuffled_number]]
                    if game.game_type == 'SUBSTITUTION':
                        kb.append([ux.BUTTON_NO_CORRECT_ANSWER[lang]])
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
                if text_input == ux.BUTTON_NO_CORRECT_ANSWER[lang]:
                    assert game.game_type == 'SUBSTITUTION'
                    voted_shuffled_index = -1
                else:
                    voted_shuffled_index = int(text_input) - 1
                remaining_names = game.set_voted_indexes_and_points_and_get_remaining(user, voted_shuffled_index)
                remaining_names_str = ', '.join(remaining_names)
                all_but_users = [p for p in players if p!=user]
                send_message_multi(all_but_users, ux.MSG_X_VOTED[lang].format(user.get_name()))
                if len(remaining_names)>0:
                    send_message(user, ux.MSG_THANKS[lang], remove_keyboard=True)
                    send_message(user, ux.MSG_WAIT_FOR[lang].format(remaining_names_str), remove_keyboard=True)
                    send_message_multi(all_but_users, ux.MSG_WAIT_FOR[lang].format(remaining_names_str))
                else:
                    #only once
                    if game.game_control == 'TEACHER':
                        redirect_to_state_multi(players, state_GAME_TEACHER_VALIDATION)                  
            else:
                send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang], kb)

# ================================
# GAME_TEACHER_VALIDATION 
# ================================
def state_GAME_TEACHER_VALIDATION(user, message_obj):
    game = user.get_current_game()
    players, reader, writers = game.get_current_hand_players_reader_writers()
    lang = game.language
    shuffled_answers = game.get_shuffled_answers()
    number_answers = len(shuffled_answers)

    if message_obj is None:
        if user == reader:
            # teacher            
            numbers_list = list(range(1,number_answers+1))
            kb = [[str(i) for i in numbers_list]] #should exclude the original one
            if game.game_type == 'SUBSTITUTION':
                kb.append([ux.BUTTON_NO_CORRECT_ANSWER_NO_EMOJI[lang]])
            send_message(user, ux.MSG_TEACHER_VOTE[lang], kb, sleep=True)
            send_message_multi(writers, ux.MSG_WAIT_FOR_TEACHER_EVALUATION[lang], remove_keyboard=True)            
    else:
        if user != reader:
            send_message(user, ux.MSG_WRONG_INPUT_WAIT_FOR_TEACHER_TO_VOTE[lang])
        else:
            text_input = message_obj.text
            if text_input == '/recap_answers':
                send_message(user, game.get_var('ALL_NUM_COMPLETED_ANSWERS'))
                return
            kb = user.get_keyboard()
            if text_input in utility.flatten(kb):
                TEACHER_CORRECT_ANSWERS = user.get_var('TEACHER_CORRECT_ANSWERS',[])
                if text_input == ux.BUTTON_SUBMIT[lang]:
                    game.set_correct_answers(TEACHER_CORRECT_ANSWERS)
                    recap_votes(user, game)   
                else:                       
                    if text_input.endswith(ux.BUTTON_NO_CORRECT_ANSWER_NO_EMOJI[lang]):
                        assert game.game_type == 'SUBSTITUTION'
                        if -1 in TEACHER_CORRECT_ANSWERS:
                            TEACHER_CORRECT_ANSWERS.pop()
                        else:
                            for _ in range(len(TEACHER_CORRECT_ANSWERS)):
                                TEACHER_CORRECT_ANSWERS.pop()
                            TEACHER_CORRECT_ANSWERS.append(-1)                        
                    else:                        
                        if text_input.startswith('⭐'):
                            TEACHER_CORRECT_ANSWERS.remove(int(text_input[1:]))                        
                        else:
                            TEACHER_CORRECT_ANSWERS.append(int(text_input))
                            if -1 in TEACHER_CORRECT_ANSWERS:
                                TEACHER_CORRECT_ANSWERS.remove(-1)                            
                    numbers_list = list(range(1,number_answers+1))
                    starred_number_list = [
                        '⭐{}'.format(n) if n in TEACHER_CORRECT_ANSWERS else '{}'.format(n) 
                        for n in numbers_list
                    ]
                    kb = [starred_number_list]
                    if TEACHER_CORRECT_ANSWERS:
                        # if there are stars  
                        NONE_BUTTON = ux.BUTTON_NO_CORRECT_ANSWER_NO_EMOJI[lang]
                        if -1 in TEACHER_CORRECT_ANSWERS:
                            NONE_BUTTON = '⭐' + NONE_BUTTON
                        kb.append([NONE_BUTTON])
                        kb.append([ux.BUTTON_SUBMIT[lang]])
                        msg = ux.MSG_TEACHER_VOTE_AND_SUBMIT[lang]
                    else:
                        msg = ux.MSG_TEACHER_VOTE[lang]
                        if game.game_type == 'SUBSTITUTION':
                            kb.append([ux.BUTTON_NO_CORRECT_ANSWER_NO_EMOJI[lang]])                    
                    send_message(user, msg, kb)
            else:
                send_message(user, ux.MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS[lang], kb)

# ================================
# UTIL FUNCTION TO RECAP VOTES
# ================================
def recap_votes(user, game):
    lang = game.language
    players, reader, _ = game.get_current_hand_players_reader_writers()
    shuffled_answers = game.get_shuffled_answers()
    shuffled_answer_voters_names = game.get_shuffled_answers_voters()
    exact_answers_indexes = game.get_exact_answers_indexes()             
    exact_answers_players = [players[i] for i in exact_answers_indexes]
    exact_answers_names = [p.get_name() for p in exact_answers_players]
    msg_summary_list = []
    for i, answer in enumerate(shuffled_answers):       
        num = i+1     
        answer_complete_text = ux.render_complete_text(game, answer)
        authors_indexes = game.get_answers_authors_indexes(answer)
        authors = [players[i] for i in authors_indexes]            
        voters_names = shuffled_answer_voters_names[i]
        num_voters = str(len(voters_names))
        if voters_names:
            num_voters += " ({})".format(', '.join(voters_names))
        if reader in authors:
            guessers_summary = str(len(exact_answers_names))
            if exact_answers_names:
                guessers_summary += " ({})".format(', '.join(exact_answers_names))
            answer_report = "{} *{}* ⭐️ → {}\n{}".format(
                num, reader.get_name(), answer_complete_text, \
                ux.MSG_GUESSED_BY_AND_CORRECTLY_VOTED_BY[lang].format(guessers_summary, num_voters))
        else:
            author_names = ', '.join(p.get_name() for p in authors)
            answer_report = "{} *{}* → {}\n{}".format(
                num, author_names, answer_complete_text, ux.MSG_VOTED_BY[lang].format(num_voters))
        msg_summary_list.append(answer_report)
    msg_summary = '\n\n'.join(msg_summary_list)
    send_message_multi(players, ux.MSG_VOTE_RECAP[lang], remove_keyboard=True)    
    send_message_multi(players, msg_summary)
    if game.game_type == 'SUBSTITUTION':
        # write count for NO VALID ANSWERS
        pass
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
        # send_message_multi(players, ux.MSG_POINT_GAME_PARTIAL_SUMMARY[lang])
        # game.prepare_and_send_game_point_img_data(players)
        game.setup_next_hand(user)
        redirect_to_state_multi(players, state_GAME_READER_WRITES_BEGINNING)

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
            send_message_multi(players, ux.MSG_EXIT_GAME[lang].format(user.get_name()))
        else:
            send_message_multi(players, ux.MSG_EXIT_GAME_EXPIRED[lang])
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
        lang = game.language
        if game:
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
            send_message(user, ux.MSG_NO_GAME_TO_EXIT[lang])
        return True
    if text_input == ('/chat'):
        send_message(user, ux.MSG_CHAT_INFO[lang])
        return True
    if text_input.startswith('/chat '):
        game = user.get_current_game()
        lang = game.language
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

