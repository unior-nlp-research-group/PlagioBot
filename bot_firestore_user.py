import key
from utility import escape_markdown

import json
import logging

from google.cloud import firestore

from dataclasses import dataclass, field
from typing import List, Dict, Any

# https://gitlab.com/futureprojects/firestore-model/blob/master/examples/main.py
import firestore_model
from firestore_model import Model

db = firestore.Client()
firestore_model.db = db
# transaction = db.transaction()


@dataclass
class User(Model):
    application: str
    serial_id: str
    name: str
    username: str
    language: str    
    bot: bool    
    state: str = field(default=None)
    keyboard: str = field(default=None)
    notifications: bool = field(default=True)    
    current_game_id: str = field(default=None)     
    variables: str = field(default='{}', repr=False, compare=False)
    # _max_attempts: int = 10 # for transactional

    @staticmethod
    def make_id(application, serial_id):
        return '{}_{}'.format(application, serial_id)

    @staticmethod
    def create_user(application, serial_id, name, username, language, bot=False):
        user = User.make(
            application = application,
            serial_id = str(serial_id),
            name = name,
            username = username,
            language = language if language in ['en','it'] else 'it',
            bot = bot
        )
        user.id = User.make_id(application, serial_id)
        user.save()
        return user

    @staticmethod
    def get_user(application, serial_id):
        id_str = User.make_id(application, serial_id)
        return User.get(id_str)

    def update_user(self, name, username):
        self.name = name
        self.username = username
        self.save()

    def get_name(self):
        return escape_markdown(self.name)

    def get_name_at_username(self, escape_markdown=False):
        if self.username:
            result = "{} @{}".format(self.name, self.username)
        else:
            result = self.name 
        if escape_markdown:
            return escape_markdown(result)
        return result

    def set_state(self, state, save=True):
        self.state = state
        if save: self.save()

    def switch_language(self, lang, save=True):
        self.language = 'it' if self.language == 'en' else 'en'
        if save: self.save()

    def switch_notifications(self):
        self.notifications = not self.notifications
        self.save()

    def set_current_game(self, game):
        self.current_game_id = game.id
        self.save()

    def get_current_game(self):
        from bot_firestore_game import Game
        if self.current_game_id is None:
            return None
        return Game.get(self.current_game_id)

    def set_keyboard(self, value, save=True):
        self.keyboard = json.dumps(value, ensure_ascii=False)
        if save: self.save()

    def set_empy_keyboard(self, save=True):
        self.keyboard = None
        if save: self.save()

    def get_keyboard(self):
        return json.loads(self.keyboard)

    def reset_variables(self, save=True):
        self.variables = '{}'
        if save: self.save()

    def set_variables_from_dict(self, value_dict, save=True):
        self.variables = json.dumps(value_dict, ensure_ascii=False)
        if save: self.save()

    def get_variables_as_dict(self):
        return json.loads(self.variables)

    def set_var(self, var_name, var_value, save=True):
        var_dict = json.loads(self.variables)
        var_dict[var_name] = var_value        
        self.set_variables_from_dict(var_dict, save)

    def get_var(self, var_name):
        var_dict = json.loads(self.variables)
        return var_dict.get(var_name,None)

    def is_master(self):
        return self.serial_id == key.TELEGRAM_BOT_MASTER_ID
    
    def is_tester(self):
        return self.serial_id in key.TELEGRAM_TESTERS_IDS

    @staticmethod
    def get_user_lang_state_notification_on(lang, state):
        users_generator = User.query([
            ('notifications', '==', True), 
            ('state', '==', state)
        ]).get()
        return list(users_generator)

if __name__ == "__main__":
    user = User.create_user('test','123','name','username','it')
    