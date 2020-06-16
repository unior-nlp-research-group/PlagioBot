from flask import Flask, Response, request, jsonify
from flask_cors import CORS, cross_origin
import key

import logging
import google.cloud.logging
client = google.cloud.logging.Client()
client.setup_logging(log_level=logging.DEBUG) # INFO DEBUG WARNING


# If entrypoint is not defined in app.yaml, App Engine will look for an app
# called app in main.py.
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def root():
    logging.debug("in root function")
    """Return a friendly HTTP greeting."""
    return ("Plagio Game.", 200)

@app.route('/tasks/interrupt_expired_games')
def interrupt_expired_games():
    if key.TEST:
        return
    from bot_firestore_game import Game
    from bot_telegram_dialogue import interrupt_game
    expired_games = Game.get_expired_games()
    for g in expired_games:
        interrupt_game(g)
    return ("", 200)

@app.errorhandler(404)
def page_not_found(e):
    logging.debug("page_not_found")
    # note that we set the 404 status explicitly
    return ("url not found", 404)

@app.errorhandler(500)
def internal_error(error):
    return ("500 error: {}".format(error), 500)

@app.route(key.WEBHOOK_TELEGRAM_ROUTING, methods=['POST'])
def telegram_webhook_handler():
    import threading
    from bot_telegram_dialogue import deal_with_request
    import json
    request_json = request.get_json(force=True)

    logging.debug("TELEGRAM POST REQUEST: {}".format(json.dumps(request_json)))

    # deal_with_request(request_json)
    threading.Thread(target=deal_with_request, args=[request_json]).start()

    return ('',200)

@app.route('/add_user', methods=['POST'])
@cross_origin()
def add_user():
    from bot_firestore_user import User
    from bot_telegram import report_master
    user_id = request.form.get('id')
    user_name = request.form.get('name')
    logging.debug('ENDOPOINT: add_user id={} name={}'.format(user_id, user_name))
    if user_id and user_name:
        if user_id.startswith('web_') and len(user_id)>4:
            application, serial_id = user_id.split('_')
            if User.get_user(application, serial_id):
                return jsonify({'success': False, 'error': 'User exists'}), 400
            u = User.create_user(application, serial_id, user_name)
            u.set_state('state_INITIAL')
            report_master('New user: {}'.format(user_id))
            return jsonify({'success': True, 'error': None}), 200
        else:
            error_msg = 'id must conform to string pattern <web_serial>'
            return jsonify({'success': False, 'error': error_msg}), 400
    error_msg = 'Both id and name params need to be specified'
    return jsonify({'success': False, 'error': error_msg}), 400


@app.route('/join_game', methods=['POST'])
@cross_origin()
def join_game():
    from bot_firestore_user import User
    from bot_firestore_game import Game
    user_id = request.form.get('id')
    game_name = request.form.get('game_name')
    logging.debug('ENDOPOINT: join_game id={} game_name={}'.format(user_id, game_name))
    if user_id and game_name:
        if user_id.startswith('web_') and len(user_id)>4:
            application, serial_id = user_id.split('_')
            u = User.get_user(application, serial_id)
            if u is None:
                error_msg = 'user does not exist'
                return jsonify({'success': False, 'error': error_msg}), 400
            if u.state != 'state_INITIAL':
                error_msg = 'user not in state_INITIAL'
                return jsonify({'success': False, 'error': error_msg}), 400
            room_name = game_name.upper()
            game = Game.get_game_in_initial_state(room_name)
            if game:
                if Game.add_player(game, u):
                    u.set_state('state_WAITING_FOR_START')
                    return jsonify({'success': True, 'error': None}), 200
                else:
                    error_msg = 'Game no longer available'
                    return jsonify({'success': False, 'error': error_msg}), 400
            else:
                error_msg = 'Game does not exist'
                return jsonify({'success': False, 'error': error_msg}), 400
        else:
            error_msg = 'id must conform to string pattern <web_serial>'
            return jsonify({'success': False, 'error': error_msg}), 400
    else:
        error_msg = 'Both id and game_name params need to be specified'
        return jsonify({'success': False, 'error': error_msg}), 400

@app.route('/create_game', methods=['POST'])
@cross_origin()
def create_game():
    from bot_firestore_user import User
    from bot_firestore_game import Game
    user_id = request.form.get('id')
    game_name = request.form.get('game_name')
    logging.debug('ENDOPOINT: create_game id={} game_name={}'.format(user_id, game_name))
    if user_id and game_name:
        if user_id.startswith('web_') and len(user_id)>4:
            application, serial_id = user_id.split('_')
            u = User.get_user(application, serial_id)
            if u is None:
                error_msg = 'user does not exist'
                return jsonify({'success': False, 'error': error_msg}), 400
            if u.state != 'state_INITIAL':
                error_msg = 'user not in state_INITIAL'
                return jsonify({'success': False, 'error': error_msg}), 400
            room_name = game_name.upper()
            game = Game.get_game_in_initial_state(room_name)
            if game:
                error_msg = 'There is already an active game with the same name'
                return jsonify({'success': False, 'error': error_msg}), 400
            game = Game.create_game(room_name, u)
            u.set_current_game(game, save=False)
            u.set_state('state_WAITING_FOR_START')
            return jsonify({'success': True, 'error': None}), 200
        else:
            error_msg = 'id must conform to string pattern <web_serial>'
            return jsonify({'success': False, 'error': error_msg}), 400
    else:
        error_msg = 'Both id and game_name params need to be specified'
        return jsonify({'success': False, 'error': error_msg}), 400


@app.route('/user_reply', methods=['POST'])
@cross_origin()
def user_reply():
    from bot_firestore_user import User
    from bot_telegram_dialogue import repeat_state
    import telegram
    user_id = request.form.get('id')
    user_reply = request.form.get('reply')
    logging.debug('ENDOPOINT: user_reply id={} reply={}'.format(user_id, user_reply))
    if user_id and user_reply:
        if user_id.startswith('web_') and len(user_id)>4:
            application, serial_id = user_id.split('_')
            u = User.get_user(application, serial_id)
            if u is None:
                error_msg = 'user does not exist'
                return jsonify({'success': False, 'error': error_msg}), 400
            message_obj = telegram.Message(message_id=-1, from_user=None, date=None, chat=None, text=user_reply)
            repeat_state(u, message_obj=message_obj)
            return jsonify({'success': True, 'error': None}), 200
        else:
            error_msg = 'id must conform to string pattern <web_serial>'
            return jsonify({'success': False, 'error': error_msg}), 400
    else:
        error_msg = 'Both id and reply params need to be specified'
        return jsonify({'success': False, 'error': error_msg}), 400
