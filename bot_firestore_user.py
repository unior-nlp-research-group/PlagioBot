import key
from utility import escape_markdown

import json
import logging

# https://firebase.google.com/docs/firestore/manage-data/add-data
from google.cloud import firestore

from dataclasses import dataclass, field
from typing import List, Dict, Any

# https://gitlab.com/futureprojects/firestore-model/blob/master/examples/main.py
import firestore_model
from firestore_model import Model

db = firestore.Client()
firestore_model.db = db


@dataclass
class User(Model):
    application: str
    serial_id: str
    name: str #= field(compare=False)
    username: str #= field(compare=False)
    language: str #= field(compare=False)
    bot: bool = False #field(default=False, compare=False)
    state: str = None #field(default=None, compare=False)
    keyboard: List = None #field(default=None, compare=False)
    notifications: bool = True #field(default=True, compare=False)    
    current_game_id: str = None #field(default=None, compare=False)     
    variables: Dict = field(default_factory=dict)

    @staticmethod
    def make_id(application, serial_id):
        return '{}_{}'.format(application, serial_id)

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

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

    def switch_language(self, save=True):
        self.language = 'it' if self.language == 'en' else 'en'
        if save: self.save()

    def switch_notifications(self):
        if key.TEST:
            # if we are in the test bot do not switch notification mode 
            # (both test and production share the same db)
            return
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
        self.keyboard = {str(i):v for i,v in enumerate(value)}
        if save: self.save()

    def set_empy_keyboard(self, save=True):
        self.keyboard = {}
        if save: self.save()

    def get_keyboard(self):
        return [self.keyboard[str(i)] for i in range(len(self.keyboard))] 

    def reset_variables(self, save=True):
        self.variables = {}
        if save: self.save()

    def set_var(self, var_name, var_value, save=True):
        self.variables[var_name] = var_value
        if save: self.save()

    def get_var(self, var_name):
        return self.variables.get(var_name,None)

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

def get_fede():
    return User.get_user('telegram', key.TELEGRAM_BOT_MASTER_ID)

if __name__ == "__main__":
    user = User.create_user('test','123','name','username','it')
    