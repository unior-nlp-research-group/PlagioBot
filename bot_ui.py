# -*- coding: utf-8 -*-

# ================================
# SYMBOLS
# ================================
# 🤗📝✏️
CHECK_SYMBOL = '✅'
BULLET_SYMBOL = '∙'
RIGHT_ARROW_SYMBOL = '→'
IT_FLAG_SYMBOL = '🇮🇹'
EN_FLAG_SYMBOL = '🇬🇧'

# ================================
# BUTTONS
# ================================

START_BUTTON = {
    'en': "🚩 START",
    'it': "🚩 INIZIO"
}
HELP_BUTTON = {
    'en': "🆘 HELP",
    'it': "🆘 AIUTO"
}

BUTTON_YES = {
    'en': '✅ YES',
    'it': '✅ SI'
}
BUTTON_NO = {
    'en': '❌ NO',
    'it': '❌ NO'
}
BUTTON_BACK = {
    'en': "🔙 BACK",
    'it': "🔙 INDIETRO"
}
BUTTON_HOME = {
    'en': "🏠 HOME",
    'it': "🏠 INIZIO"
}
BUTTON_INFO = {
    'en': "ℹ INFO",
    'it': "ℹ INFO"
}
BUTTON_ABORT = {
    'en': "❌ ABORT",
    'it': "❌ ANNULLA"
}
BUTTON_SKIP = {
    'en': "➡️ SKIP",
    'it': "➡️ SALTA"
}
BUTTON_START_GAME = {
    'en': '🎯 START GAME',
    'it': '🎯 INIZIO GIOCO'
}
BUTTON_CONTACT_US = {
    'en': "📩 CONTACT US",
    'it': "📩 CONTATTACI"
}
BUTTON_ADMIN = {
    'en': "🔑 Admin",
    'it': "🔑 Admin"
}
BUTTON_ENABLE_NOTIFICATIONS = {
    'en': "🔔 Enable Notifications",
    'it': "🔔 Attiva Notifiche"
}
BUTTON_ANNOUNCE_GAME_PUBLICLY = {
    'en': "🔔 Announce Game",
    'it': "🔔 Annuncia Gioco"
}
BUTTON_DISABLE_NOTIFICATIONS = {
    'en': "🔕 Disable Notifications",
    'it': "🔕 Disabilita Notifiche"
}
BUTTON_CHANGE_LANGUAGE = {
    'en': '🇬🇧 ⇆ 🇮🇹',
    'it': '🇬🇧 ⇆ 🇮🇹'
}

####################
# CONVERSATIONS
####################

MSG_WELCOME = {
    'en': "🤗 Welcome to PlagioBot!",
    'it': "🤗 Benvenuto a PlagioBot!"
}
MSG_HOME = {
    'en': "🏠 Home Screen",
    'it': "🏠 Schermata Iniziale"
}
MSG_NOTIFICATIONS_ON = {
    'en': "🔔 You have the notifications enabled.",
    'it': "🔔 Hai le notifiche abilitate."
}
MSG_NOTIFICATIONS_OFF = {
    'en': "🔕 You have the notifications disabled.",
    'it': "🔕 Hai le notifiche disabilitate."
}
MSG_NO_START_COMMAND_AVAILABLE_DURING_GAME = {
    'en': "⛔ No /start command availale during the game. Type /exit\\_game if you want to abandon the game.",
    'it': "⛔ Il comando /start non è disponibile durante il gioco. Scrivi /exit\\_game se vuoi terminare il gioco."
}
MSG_INFO = {
    'en': "🏗 Plagio bot the game of creative writers!",
    'it': "🏗 Plagio bot il gioco degli scrittori creativi!"
}
MSG_WORK_IN_PROGRESS = {
    'en': "🏗 System under maintanance, please try later.",
    'it': "🏗 Sistema in manutenzione, riprova più tardi."
}
MSG_CHANGE_LANGUAGE = {
    'en': "🇬🇧 ⇆ 🇮🇹 Change Language",
    'it': "🇬🇧 ⇆ 🇮🇹 Cambia Lingua"
}
MSG_LANGUAGE_CHANGED = {
    'en': "🇬🇧 Language set for English",
    'it': "🇮🇹 Lingua impostata per l'italiano"
}
MSG_CHOOSE_GAME_NAME = {
    'en': "✍️ Choose the name of an existing game or a create a new one.",
    'it': "✍️ Scegli il nome di un gioco esistente o creane uno nuovo."
}
MSG_WRITE_GAME_SPECIAL_RULES = {
    'en': "✍️ If you want you can write down any special rule you want to set for the game (e.g., rymes, length of sentences, etc...), or press {}".format(BUTTON_SKIP['en']),
    'it': "✍️ Inserisci se vuoi delle regole particolari da adottare nel gioco (ad esempio rime, lunghezza frasi, ecc...), o premi {}".format(BUTTON_SKIP['it']),
}
MSG_TELL_SPECIAL_RULES = {
    'en': "🧭 {} has chosen the following rules for the game: {}",
    'it': "🧭 {} ha scelto le seguenti regole del gioco: {}"
}
MSG_GAME_ALREADY_STARTED = {
    'en': '🤷‍♀️ No more seats availbel on this game.',
    'it': '🤷‍♀️ Non ci sono posti disponibili in questo gioco.'
}
MSG_NAME_NO_LONGER_AVAILBLE = {
    'en': "🤷‍♀️ The name *{}* is no longer available.",
    'it': "🤷‍♀️ Il nome *{}* non è più disponibile."
}
MSG_NEW_GAME_CONFIRM = {
    'en': '🆕 No game "{}" exists. Do you want to create it?',
    'it': '🆕 Nessun gioco con il nome "{}" esiste. Vuoi crearne uno?'
}
MSG_WRONG_INPUT_NUMBER_OF_PLAYERS = {
    'en': '⛔️ You must enter a name between 3 and 100',
    'it': '⛔️ Devi inserire un numero da 3 a 100'
}
MSG_NUMBER_OF_PLAYERS = {
    'en': "🔢 Please enter the number of players.",
    'it': "🔢 Inserisci il numero dei giocatori."
}
MSG_ENTERING_GAME_X = {
    'en': "🏁 You entered game *{}*.",
    'it': "🏁 Sei entrato nel gioco *{}*."
}
MSG_INVITE_PEOPLE = {
    'en': "📮 You can invite other players to the game *{}* or press the button below 🔔 to announce it publicly.",
    'it': "📮 Puoi invitare altri giocatori ad unirsi al gioco *{}* o premere il pulsante 🔔 per annunciarlo pubblicamente."
}
MSG_ANNOUNCE_GAME_PUBLICLY = {
    'en': "📮 New game created by {} with {} people and {} seats remaining. Join th egame clicking on {}.",
    'it': "📮 Nuovo gioco creato da {} con {} persone e {} posti rimanenti. Unisciti premendo su {}."
}
MSG_SENT_ANNOUNCEMENT = {
    'en': "📮 Announcement sent! Let's wait for new players to join.",
    'it': "📮 Annuncio inviato! Aspettiamo che altri giocatori si uniscano."
}
MSG_PLAYER_X_JOINED_GAME = {
    'en': "👤 Player *{}* joined the game.",
    'it': "👤 Il giocatore *{}* si è unito al gioco."
}
MSG_WAITING_FOR_X_PLAYERS = {
    'en': "😴 Waiting for {} other players...",
    'it': "😴 Stiamo aspettando {} altri giocatori..."
}
MSG_READY_TO_START = {
    'en': "👟 All seats have been occupied, let's start the game!",
    'it': "👟 Tutti i posti sono stati occupati, iniziamo il gioco!"
}
MSG_HAND_INFO = {
    'en': '🖐 Current Hand: {}\n📖 Reader: {}',
    'it': '🖐 Mano: {}\n📖 Lettore: {}'
}
MSG_READER_WRITES_BEGINNING = {
    'en': '✍️ Please write down the beginning of a sentence or paragraph from a book.',
    'it': "✍️ Scrivi l'inizio di una frase o un paragrafo di un libro."
}
MSG_WRITERS_WAIT_READER = {
    'en': "😴 Let's wait for {} to write down the beginning of a paragraph from a book",
    'it': "😴 Aspettiamo {} che scriva l'inizio di una frase o di un paragrafo di un libro."
}
MSG_PLAYERS_BEGINNING_INFO = {
    'en': "📝 This is the chosen beginning by {}",
    'it': "📝 Questo è l'inizio scelto da {}"
}
MSG_READER_WRITE_CONTINUATION = {
    'en': "✍️ Please, write down the correct continuation of the sentence.",
    'it': "✍️ Scrivi la corretta continuazione del testo inserito."
}
MSG_WRITERS_WRITE_CONTINUATION = {
    'en': "✍️ Please, write down a possible continuation of the sentence.",
    'it': "✍️ Scrivi una possibile continuazione del testo."
}
MSG_THANKS_FOR_CONTINUATION = {
    'en': "😀 Thanks! Let's wait for the other players to write the continuations. 😴",
    'it': "😀 Grazie! Aspettiamo che gli altri giocatori inseriscano la loro coninuazione. 😴"
}
MSG_X_GAVE_CONTINUATION_WAITING_FOR_PLAYERS_NAME_CONTINUATION = {
    'en': "📝 Received continuation of *{}*. Let's wait for: {} 😴",
    'it': "📝 Ricevuta la continuazione di *{}*. Rimaniamo in attesa di: {} 😴"
}
MSG_INTRO_NUMBERED_TEXT = {
    'en': "📝 These are all the complete texts in random order:",
    'it': "📝 Queste sono tutte i testi completi in ordine casuale:"
}
MSG_WAIT_FOR_PLAYERS_TO_VOTE = {
    'en': "😴 Let's wait for the other players to guess.",
    'it': "😴 Rimaniamo in attesa della scelta degli altri giocatori."
}
MSG_VOTE = {
    'en': "🗳️ Please select the number of the continuation you think it's the orginal one.",
    'it': "🗳️ Seleziona il numero del testo che ritieni essere l'originale."
}
MSG_THANKS_WAITING_FOR_OTHER_PLAYERS_VOTE = {
    'en': "😀 Thanks, let's wait for the other players to guess. 😴",
    'it': "😀 Grazie, rimaniamo in attesa della scelta degli altri giocatori. 😴"
}
MSG_X_VOTED_WAITING_FOR_PLAYERS_VOTE = {
    'en': "✔️ *{}* has chosen. Let's wait for: {} 😴",
    'it': "✔️ *{}* ha fatto la sua scelta. Let's wait for: {} 😴"
}
MSG_VOTE_RECAP = {
    'en': "🗳️ These are the choices being made:",
    'it': "🗳️ Queste sono le scelte effettuate:"
}
MSG_VOTED_BY = {
    'en': "Voted by:",
    'it': "Votato da:"
}
MSG_POINT_HAND_SUMMARY = {
    'en': "🖐 HAND POINTS:\n{}",
    'it': "🖐 PUNTI MANO:\n{}"
}
MSG_POINT_GAME_SUMMARY = {
    'en': "🎲 GAME POINTS:\n{}",
    'it': "🎲 PUNTI GIOCO:\n{}"
}
MSG_EXIT_GAME = {
    'en': "🚪 Game has terminated because {} exited.",
    'it': "🚪 Gioco terminato perché {} è uscito/a."
}
MSG_NO_GAME_TO_EXIT = {
    'en': "⛔️ You are not in a game",
    'it': "⛔️ Non sei in un gioco"
}
MSG_WINNER_SINGULAR = {
    'en': "🏆 The winner of the game is *{}*",
    'it': "🏆 Il vincitore del gioco è *{}*"
}
MSG_WINNER_PLURAL = {
    'en': "🏆 The winners of the game are *{}*",
    'it': "🏆 I vincitori del gioco sono *{}*"
}

MSG_WRONG_INPUT_WAIT_FOR_PLAYERS_TO_VOTE = {
    'en': "⛔️ Let's wait for the other players to vote.",
    'it': "⛔️ Attendiamo che le altre persone completino il voto."
}
MSG_WRONG_INPUT_WAIT_FOR_READER = {
    'en': '⛔️ Please wait for {} to insert the text.',
    'it': '⛔️ Attendiamo che {} inserisca il testo.'
}
MSG_WRONG_INPUT_USE_TEXT = {
    'en': '⛔ Wrong input, please insert text.',
    'it': '⛔ Input non valido, per favore inserisci del testo.'
}
MSG_WRONG_INPUT_USE_TEXT_OR_BUTTONS = {
    'en': '⛔️ Wrong input, please use text or buttons below 🎛',
    'it': '⛔️ Input non valido, per favore inserisci del testo o usa i pulsanti 🎛'
}
MSG_WRONG_INPUT_USE_BUTTONS = {
    'en': '⛔️ Wrong input, please use buttons below 🎛',
    'it': '⛔️ Input non valido, per favore usa i pulsanti 🎛'
}
MSG_COMMAND_NOT_RECOGNIZED = {
    'en': '⛔️ The command has not been recognised.',
    'it': '⛔️ Comando non riconosciuto.'
}

