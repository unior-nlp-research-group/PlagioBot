MIN_NUM_OF_PLAYERS = 3

MIN_BEGINNING_LENGTH = 10
MIN_TEXT_INFO_LENGTH = 10

MAX_NAME_LENGTH = 20

MAX_NUM_HANDS = 100

POINTS = {
    'CONTINUATION': {
        'CORRECT_ANSWER': 1,
        'INCORRECT_ANSWER': 0,
        'NO_ANSWER': -1,
        'CORRECT_SELECTION': 1,
        'INCORRECT_SELECTION': 0, 
        'NO_SELECTION': -1,
        'RECEIVED_VOTE': 1,
    },
    'FILL': {
        'CORRECT_ANSWER': 1,
        'INCORRECT_ANSWER': 0,
        'NO_ANSWER': -1,
        'CORRECT_SELECTION': 1,
        'INCORRECT_SELECTION': 0,
        'NO_SELECTION': -1,
        'RECEIVED_VOTE': 1,
    },
    'REPLACEMENT': {
        'CORRECT_ANSWER': 2,
        'INCORRECT_ANSWER': 0,
        'NO_ANSWER': -1,
        'CORRECT_SELECTION': 1,
        'INCORRECT_SELECTION': -1, # applicable only in teacher mode
        'NO_SELECTION': -1, # applicable only in teacher mode
        'RECEIVED_VOTE': 1, # not applicable in teacher mode    
    }
}


INSTRUCTION_URL_IT = 'https://telegra.ph/Plagio---Regole-del-gioco-01-06'
INSTRUCTION_URL_EN = 'https://telegra.ph/Plagio---Game-Rules-01-06'

NO_ANSWER_KEY = "___"

EXPIRATION_DELTA_HOURS = 240
EXPIRATION_DELTA_MILLISECONDS = EXPIRATION_DELTA_HOURS * 3600 * 1000
ONLY_GAME_CREATOR_CAN_TERMINATE_GAME = False
NUM_HANDS_IN_TEACHER_MODE = 5