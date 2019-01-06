# -*- coding: utf-8 -*-

import logging
from google.cloud import datastore
from bot_ndb_base import NDB_Base
import key
import json
from utility import escape_markdown

CLIENT = datastore.Client()
KIND = 'User'

class NDB_User(NDB_Base):

    def __init__(self, application=None, serial_number=None,
                 name=None, username=None, language='en',
                 bot=False, update=True, entry=None):
        if entry:
            self.entry = entry
            return
        id_str = "{}:{}".format(application, serial_number)
        key = CLIENT.key(KIND, id_str)
        self.entry = CLIENT.get(key)
        if not self.entry:
            self.entry = datastore.Entity(key=key, exclude_from_indexes=['variables'])
            self.entry.update(
                application=application,
                serial_number=str(serial_number),
                language = language,
                current_game_key = None,
                bot = bot,
                notifications = True,
                variables = json.dumps({})
            )
            if not update:
                self.put()
        if update:
            self.update_info(name, username)

    def get_name(self):
        return escape_markdown(self.name)

    def update_info(self, name, username):
        self.entry.update(
            name=name,
            username=username,
        )
        self.put()

    def switch_notifications(self):
        self.notifications = not self.notifications
        self.put()

    def set_current_game(self, game):
        self.current_game_key = game.key
        self.put()

    def get_current_game(self):
        if self.current_game_key is None:
            return None
        from bot_ndb_game import NDB_Game
        return NDB_Game(entry=CLIENT.get(self.current_game_key))

    def is_bot(self):
        return self.bot

    def reset_vars(self):
        self.variables = json.dumps({})
        self.put()

    def set_keyboard(self, value, put=True):
        self.set_var('KEYBOARD', value, put)

    def get_keyboard(self):
        return self.get_var('KEYBOARD')

    def set_var(self, var_name, var_value, put=True):
        var_dict = json.loads(self.variables)
        # previous_value = var_dict.get(var_name,None)
        var_dict[var_name] = var_value
        self.variables = json.dumps(var_dict)
        if put:
            # logging.debug("setting var {} from {} to {} for user {}".format(var_name, previous_value, var_value, self.name))
            self.put()

    def get_var(self, var_name):
        var_dict = json.loads(self.variables)
        return var_dict.get(var_name,None)

    def is_master(self):
        return self.serial_number == key.TELEGRAM_BOT_MASTER_ID

def get_query_lang_state_notification_on(lang, state):
    query = CLIENT.query(kind=KIND)
    query.add_filter('language', '=', lang)
    query.add_filter('state', '=', state)
    query.add_filter('notifications', '=', True)
    return query

if __name__ == '__main__':
    '''
    from bot_ndb_game import NDB_Game
    user = (application='test', serial_number='000', name='nome')
    game = NDB_Game(name='game', creator=user, number_players=3)
    print(game.entry.key)
    print(game.key)
    #user.current_game_key = game.key
    #user.put()
    '''
    from google.cloud import datastore
    CLIENT = datastore.Client()
    from bot_ndb_game import NDB_Game
    from bot_ndb_user import NDB_User
    fede_user_entry = CLIENT.get(CLIENT.key('User','telegram:130870321'))
    katja_user_entry = CLIENT.get(CLIENT.key('User','telegram:113725192'))
    fede_user = NDB_User(entry=fede_user_entry)
    test_game_entry = CLIENT.get(CLIENT.key('Game',5077110938927104))
    game = NDB_Game(entry=test_game_entry)
    fede_user.set_current_game(game)

    entity = datastore.Entity(CLIENT.key('Game'))
    entity.update(
        name='new_test',
        creator=fede_user_entry,
        players_keys = [fede_user_entry, katja_user_entry],
        number_players=4
    )
    CLIENT.put(entity)
    print(fede_user.name)
    print(fede_user.serial_number)


    '''
    client = datastore.Client(key.APP_NAME)
    key = client.key('User')
    entity = datastore.Entity(key, exclude_from_indexes=['foo'])
    #entity['foo'] = 'foo'
    #entity['bar'] = 'bar'
    entity.update(foo='foo',bar='bar')
    client.put(entity)
    print('entity.exclude_from_indexes: {}'.format(entity.exclude_from_indexes))
    '''

