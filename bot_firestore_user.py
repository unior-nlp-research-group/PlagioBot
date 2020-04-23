import key
from utility import escape_markdown

import json
import logging

from dataclasses import dataclass, field
from typing import List, Dict, Any

from firestore_model import Model


@dataclass
class User(Model):
    application: str
    serial_id: str
    name: str
    username: str
    language: str = None
    bot: bool = False
    state: str = None
    keyboard: List = None
    notifications: bool = True
    current_game_id: str = None
    variables: Dict = field(default_factory=dict)

    @staticmethod
    def make_id(application, serial_id):
        return '{}_{}'.format(application, serial_id)

    @staticmethod
    def create_user(application, serial_id, name, username, bot=False):
        user = User.make(
            id = User.make_id(application, serial_id),
            application = application,
            serial_id = str(serial_id),
            name = name,
            username = username,
            # language = language if language in ['en','it'] else 'en',
            bot = bot,
            save = True
        )
        return user

    @staticmethod
    def get_user(application, serial_id):
        id_str = User.make_id(application, serial_id)
        return User.get(id_str)

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def update_user(self, name, username):
        self.username = username
        self.save()

    def get_name(self, escape_md=True):
        if escape_md:
            return escape_markdown(self.name)
        return self.name

    def get_name_and_id(self, escape_md=True):
        result = "{} ({})".format(self.name, self.serial_id)
        if escape_markdown:
            return escape_markdown(result)
        return result

    def get_name_at_username(self, escape_markdown=False):
        if self.username:
            result = "{} @{}".format(self.name, self.username)
        else:
            result = self.name 
        if escape_markdown:
            return escape_markdown(result)
        return result

    def set_state(self, state, save=True):
        if self.state != state:
            self.state = state
            if save: self.save()
            return True
        return False

    def switch_language(self, save=True):
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
        new_keyboard = {str(i):v for i,v in enumerate(value)}
        if self.keyboard == new_keyboard:
            return
        self.keyboard = new_keyboard
        if save: self.save()

    def set_empy_keyboard(self, save=True):
        self.set_keyboard({},save=save)

    def get_keyboard(self):
        return [self.keyboard[str(i)] for i in range(len(self.keyboard))] 

    def reset_variables(self, save=True):
        self.variables = {}
        if save: self.save()

    def set_var(self, var_name, var_value, save=True):
        if self.variables.get(var_name,None) == var_value:
            return
        self.variables[var_name] = var_value
        if save: self.save()

    def get_var(self, var_name, init_value=None):
        if var_name in self.variables:
            return self.variables[var_name]
        self.variables[var_name] = init_value
        return init_value

    def is_master(self):
        return self.serial_id == key.TELEGRAM_BOT_MASTER_ID
    
    def is_tester(self):
        return self.serial_id in key.TELEGRAM_TESTERS_IDS

    @staticmethod
    def get_user_lang_state_notification_on(lang, state):
        users_generator = User.query([
            ('language', '==', lang),
            ('notifications', '==', True), 
            ('state', '==', state)
        ]).get()
        return list(users_generator)

def get_fede():
    return User.get_user('telegram', key.TELEGRAM_BOT_MASTER_ID)

if __name__ == "__main__":
    user = User.create_user('test','123','name','username')
    