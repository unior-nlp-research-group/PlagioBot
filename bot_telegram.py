import telegram
import telegram.error
from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError
import key
import logging
import traceback
import bot_ui
import time
from bot_firestore_user import User


BOT = telegram.Bot(token=key.TELEGRAM_API_TOKEN)

# see https://github.com/python-telegram-bot/python-telegram-bot/wiki/Exception-Handling
# def error_callback(bot, update, error):
#     try:
#         raise error
#     except Unauthorized:
#         # remove update.message.chat_id from conversation list
#     except BadRequest:
#         # handle malformed requests - read more below!
#     except TimedOut:
#         # handle slow connection problems
#     except NetworkError:
#         # handle other connection problems
#     except ChatMigrated as e:
#         # the chat_id of a group has changed, use e.new_chat_id instead
#     except TelegramError:
#         # handle all other telegram related errors

def exception_reporter(func):
    def exception_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TimedOut, NetworkError):
            rety_on_network_error(func)
        except Exception: #(Unauthorized, BadRequest, ChatMigrated, TelegramError)
            report_string = '❗️ Exception {}'.format(traceback.format_exc()) #.splitlines()
            logging.error(report_string)
            try:
                report_master(report_string)
            except Exception:
                report_string = '❗️ Exception {}'.format(traceback.format_exc())
                logging.error(report_string)        
    return exception_wrapper


def rety_on_network_error(func):
    def retry_on_network_error_wrapper(*args, **kwargs):
        for retry_num in range(1, 5):
            try:
                return func(*args, **kwargs)
            except telegram.error.NetworkError:
                sleep_secs = pow(2,retry_num)
                report_string = '⚠️️ Caught network error, on {} attemp. Retrying after {} secs...'.format(retry_num,sleep_secs)
                logging.warning(report_string)                 
                report_master(report_string)
                time.sleep(sleep_secs)
        report_string = '❗️ Exception: persistent network error'
        logging.error(report_string)            
        report_master(report_string)            
    return retry_on_network_error_wrapper

def set_webhook():
    print("Attempting to set webhook to\n{}".format(key.WEBHOOK_TELEGRAM_BASE))
    s = BOT.setWebhook(key.WEBHOOK_TELEGRAM_BASE, allowed_updates=['message'])
    if s:
        print("webhook setup ok!")
    else:
        print("webhook setup failed")

def delete_webhook():
    BOT.deleteWebhook()

def get_webhook_info():
    print(BOT.get_webhook_info())

# def send_message_query(query, text, kb=None, markdown=True, remove_keyboard=False, **kwargs):
#     def get_next_page_of_users(cursor):
#         query_iter = query.fetch(start_cursor=cursor, limit=100)
#         page = next(query_iter.pages)
#         entries = list(page)
#         next_cursor = query_iter.next_page_token
#         return entries, next_cursor
#     cursor = None
#     while(True):
#         entries, cursor = get_next_page_of_users(cursor)
#         users = [User(entry=e) for e in entries]
#         send_message(users, text, kb, markdown, remove_keyboard, **kwargs)
#         #logging.debug("sending invitation to {}".format(', '.join(u.get_name() for u in users)))
#         if cursor == None:
#             break

'''
If kb==None keep last keyboard
'''
@exception_reporter
def send_message(user, text, kb=None, markdown=True, remove_keyboard=False, sleep=False, **kwargs):
    if type(user) is list:
        for u in user:
            send_message(u, text, kb=kb, markdown=markdown, 
            remove_keyboard=remove_keyboard, sleep=True, **kwargs)
        return
    
    is_user = type(user) is User
    if is_user and user.application != 'telegram':
        return
    chat_id = user.serial_id if is_user else user

    if kb!=None or remove_keyboard:
        if kb==[] or remove_keyboard:
            if is_user:
                user.set_empy_keyboard()            
            reply_markup = telegram.ReplyKeyboardRemove()
        else:
            if is_user:
                user.set_keyboard(kb)
            reply_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
    else:
        reply_markup = None        
    
    try:
        BOT.sendMessage(
            chat_id,
            text = text,
            parse_mode = telegram.ParseMode.MARKDOWN if markdown else None,
            reply_markup = reply_markup,
            disable_web_page_preview=True,
            **kwargs
        )
    except Unauthorized:
        logging.debug('User has blocked Bot: {}'.format(user))
        user.switch_notifications()
    if sleep:
        time.sleep(0.1)

def send_typing_action(user, sleep_secs=None):    
    BOT.sendChatAction(
        chat_id = user.serial_id,
        action = telegram.ChatAction.TYPING
    )
    if sleep_secs:
        time.sleep(sleep_secs)

def send_text_document(user, file_name, file_content):
    import requests
    files = [('document', (file_name, file_content, 'text/plain'))]
    data = {'chat_id': user.serial_id}
    resp = requests.post(key.TELEGRAM_API_URL + 'sendDocument', data=data, files=files)
    logging.debug("Sent documnet. Response status code: {}".format(resp.status_code))

def send_photo_from_data_multi(users, file_name, file_data, caption=None, sleep=False):
    for u in users:
        send_photo_from_data(u, file_name, file_data, caption)        


def send_photo_from_data(user, file_name, file_data, caption=None, sleep=False):
    import requests
    files = [('photo', (file_name, file_data, 'image/png'))]
    data = {'chat_id': user.serial_id}
    if caption:
        data['caption'] = caption
    resp = requests.post(key.TELEGRAM_API_URL + 'sendPhoto', data=data, files=files)
    logging.info('Sent photo. Response status code: {}'.format(resp.status_code))
    if sleep:
        time.sleep(0.1)


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

def report_master(message):
    max_length = 2000
    if len(message)>max_length:
        chunks = (message[0+i:max_length+i] for i in range(0, len(message), max_length))
        for m in chunks:
            send_message(key.TELEGRAM_BOT_MASTER_ID, m, markdown=False)    
    else:
        send_message(key.TELEGRAM_BOT_MASTER_ID, message, markdown=False)

if __name__ == "__main__":
    pass