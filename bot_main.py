from flask import Flask, Response, request, jsonify
from flask_cors import CORS, cross_origin
import key

import logging
import google.cloud.logging
client = google.cloud.logging.Client()
client.setup_logging(log_level=logging.DEBUG) # INFO DEBUG WARNING


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
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
    user_id = request.form.get('id')
    user_name = request.form.get('name')
    logging.debug('ENDOPOINT: add_user id={} name={}'.format(user_id, user_name))
    if user_id and user_name:
        if user_id.startswith('web_') and len(user_id)>4:
            application, serial_id = user_id.split('_')
            if User.get_user(application, serial_id):
                return ('User exists',400)
            User.create_user(application, serial_id, user_name)            
            return ('ok',200)
        else:
            return ('`id` must conform to string pattern <web_serial>', 400)
    return ('Both `id` and `name` params need to be specified',400)