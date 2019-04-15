import key

from utility import escape_markdown
from bot_firestore_game import Game

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
from google.cloud import firestore

from dataclasses import dataclass, field

# https://gitlab.com/futureprojects/firestore-model/blob/master/examples/main.py
import firestore_model
from firestore_model import Model

# Use the application default credentials
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred, {
#   'projectId': key.APP_NAME,
# })

# firestore_model.db = firestore.client()
firestore_model.db = firestore.Client()

@dataclass
class User(Model):
    application: str
    serial_number: str
    name:str
    username:str
    language:str    
    bot:bool
    notifications:bool = field(default=True, init=False)
    state:str = field(default=None, init=False)
    current_game_id:str = field(default=None, init=False) 
    variables:dict = field(default_factory={}, init=False, repr=False, compare=False)

    @staticmethod
    def make_id(application, serial_number):
        return '{}_{}'.format(application, serial_number)

    @staticmethod
    def create_user(application, serial_number, name, username, language, bot=False):
        user = User.make(
            application = application,
            serial_number = serial_number,
            name = name,
            username = username,
            language = language if language in ['en','it'] else 'it',
            bot = bot            
        )
        user.id = User.make_id(application, serial_number)
        user.save()
        return user

    @staticmethod
    def get_user(application, serial_number):
        id_str = User.make_id(application, serial_number)
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

    def switch_notifications(self):
        self.notifications = not self.notifications
        self.save()

    def set_current_game(self, game):
        self.current_game_id = game.id
        self.save()

    def get_current_game(self):
        if self.current_game_id is None:
            return None
        return Game.get(self.current_game_id)

    def reset_vars(self):
        self.variables = {}
        self.save()

    def set_keyboard(self, value, save=True):
        self.variables['keyboard'] = value
        if save: self.save()

    def set_empy_keyboard(self, save=True):
        self.variables['keyboard'] = []
        if save: self.save()

    def get_keyboard(self):
        return self.variables['keyboard']

    def set_var(self, var_name, var_value, save=True):
        self.variables[var_name] = var_value
        if save: self.save()

    def get_var(self, var_name):
        return self.variables[var_name]

    def is_master(self):
        return self.serial_number == key.TELEGRAM_BOT_MASTER_ID
    
    def is_tester(self):
        return self.serial_number in key.TELEGRAM_TESTERS_IDS

    @staticmethod
    def get_user_lang_state_notification_on(lang, state):
        users = User.query([
            ('notifications', '=', True), 
            ('state', '=', state)
        ]).get()
        return users