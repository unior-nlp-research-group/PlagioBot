# -*- coding: utf-8 -*-

import telegram
import key
import logging
import traceback
import bot_ui
import time
from bot_ndb_user import NDB_User


BOT = telegram.Bot(token=key.TELEGRAM_API_TOKEN)

def exception_reporter(func):    
    def exception_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            report_string = '❗️ Exception {}'.format(traceback.format_exc()) #.splitlines()
            logging.error(report_string)          
            try:  
                report_master(report_string)
            except Exception:
                report_string = '❗️ Exception {}'.format(traceback.format_exc())
                logging.error(report_string)          
    return exception_wrapper

def set_webhook():
    s = BOT.setWebhook(key.WEBHOOK_TELEGRAM_BASE)
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

def delete_webhook():
    BOT.deleteWebhook()

def get_webhook_info():
    print(BOT.get_webhook_info())

def send_message_query(query, text, kb=None, markdown=True, remove_keyboard=False, **kwargs):
    def get_next_page_of_users(cursor):
        query_iter = query.fetch(start_cursor=cursor, limit=100)
        page = next(query_iter.pages)
        users = list(page)
        next_cursor = query_iter.next_page_token
        return users, next_cursor
    cursor = None
    while(True):    
        users, cursor = get_next_page_of_users(cursor)
        send_message_multi(users, text, kb, markdown, remove_keyboard, **kwargs)
        if cursor == None:
            break

def send_message_multi(users, text, kb=None, markdown=True, remove_keyboard=False, **kwargs):
    for u in users:
        send_message(u, text, kb=kb, markdown=markdown, remove_keyboard=remove_keyboard, sleep=True, **kwargs)        

'''
If kb==None keep last keyboard
'''
def send_message(user, text, kb=None, markdown=True, remove_keyboard=False, sleep=False, **kwargs):
    #sendMessage(chat_id, text, parse_mode=None, disable_web_page_preview=None, disable_notification=False, 
    # reply_to_message_id=None, reply_markup=None, timeout=None, **kwargs)
    if kb or remove_keyboard:
        reply_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True) if kb else telegram.ReplyKeyboardRemove()
        BOT.sendMessage(        
            chat_id = user.serial_number, 
            text = text,
            parse_mode = telegram.ParseMode.MARKDOWN if markdown else None,
            reply_markup = reply_markup,
            **kwargs
        )
    else:
        BOT.sendMessage(        
            chat_id = user.serial_number, 
            text = text,
            parse_mode = telegram.ParseMode.MARKDOWN if markdown else None,
            **kwargs
        )
    if sleep:
        time.sleep(0.1)   
    

def send_text_document(user, file_name, file_content):
    import requests
    files = [('document', (file_name, file_content, 'text/plain'))]
    data = {'chat_id': user.serial_number,}
    resp = requests.post(key.TELEGRAM_API_URL + 'sendDocument', data=data, files=files)
    logging.debug("Sent documnet. Response status code: {}".format(resp.status_code))

def get_url_from_file_id(file_id):    
    import requests
    logging.debug("TELEGRAM: Requested file_id: {}".format(file_id))
    r = requests.post(key.TELEGRAM_API_URL + 'getFile', data={'file_id': file_id})
    r_json = r.json()
    if 'result' not in r_json or 'file_path' not in r_json['result']:
        logging.warning('No result found when requesting file_id: {}'.format(file_id))
        return None
    file_url = r_json['result']['file_path']
    return file_url

def get_text_from_file(file_id):
    import requests
    file_url_suffix = get_url_from_file_id(file_id)
    file_url = key.TELEGRAM_API_URL_FILE + file_url_suffix
    r = requests.get(file_url)
    return r.text

bot_telegram_MASTER = None

def report_master(message):
    global bot_telegram_MASTER
    if bot_telegram_MASTER is None:
        bot_telegram_MASTER = NDB_User('telegram', key.TELEGRAM_BOT_MASTER_ID, update=False)
    send_message(bot_telegram_MASTER, message, markdown=False)    
