# -*- coding: utf-8 -*-
import parameters
import utility

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
# SYMBOLS
# ================================
LANGUAGES = ['it','en']

# ================================
# BUTTONS
# ================================

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
BUTTON_NEW_GAME = {
    'en': '🆕🎯 NEW GAME',
    'it': '🆕🎯 NUOVO GIOCO'
}
BUTTON_JOIN_GAME = {
    'en': '🏹🎯 JOIN GAME',
    'it': '🏹🎯 ENTRA IN UN GIOCO'
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
    'en': "🔕 → 🔔",
    'it': "🔕 → 🔔"
}
BUTTON_ANNOUNCE_GAME_PUBLICLY = {
    'en': "🔔 Announce Game",
    'it': "🔔 Annuncia Gioco"
}
BUTTON_STOP_WAITING_START_GAME= {
    'en': "🏁 Start",
    'it': "🏁 Inizia"
}
BUTTON_DISABLE_NOTIFICATIONS = {
    'en': "🔔 → 🔕",
    'it': "🔔 → 🔕"
}
BUTTON_CHANGE_LANGUAGE = {
    'en': '🇬🇧 → 🇮🇹',
    'it': '🇮🇹 → 🇬🇧'
}
BUTTON_MODE_DEFAULT = {
    'en': "⚛️ DEFAULT",
    'it': "⚛️ TRADIZIONALE"
}
BUTTON_MODE_TEACHER = {
    'en': "👩‍🏫 TEACHER",
    'it': "👩‍🏫 INSEGNANTE"
}
BUTTON_MODE_DEMO = {
    'en': "🤖 DEMO",
    'it': "🤖 DEMO"
}
BUTTON_TYPE_COMPLETION = {
    'en': "👣 COMPLETION",
    'it': "👣 CONTINUA"
}
BUTTON_TYPE_FILL = {
    'en': "🕳 FILL",
    'it': "🕳 RIEMPI"
}
BUTTON_REWARD_MODE_CREATIVITY = {
    'en': "🎭 CREATIVITY",
    'it': "🎭 CREATIVITÀ"
}
BUTTON_REWARD_MODE_EXACTNESS = {
    'en': "🎯 EXACTNESS",
    'it': "🎯 ESATTEZZA"
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
    'en': "{}".format(parameters.INSTRUCTION_URL_EN),
    'it': "{}".format(parameters.INSTRUCTION_URL_IT)
}
MSG_WORK_IN_PROGRESS = {
    'en': "🏗 System under maintanance, please try later.",
    'it': "🏗 Sistema in manutenzione, riprova più tardi."
}
MSG_FEATURE_NOT_YET_IMPLEMENTED = {
    'en': "🏗 This feature has not yet been implemented.",
    'it': "🏗 Questa opzione non è ancora stata implementata."
}
MSG_CHANGE_LANGUAGE = {
    'en': "🇬🇧 ⇆ 🇮🇹 Change Language",
    'it': "🇬🇧 ⇆ 🇮🇹 Cambia Lingua"
}
MSG_LANGUAGE_INFO = {
    'en': "🇬🇧 Language set for English",
    'it': "🇮🇹 Lingua impostata per l'italiano"
}
MSG_CHOOSE_EXITING_GAME_NAME = {
    'en': "✍️ Choose the name of an existing game.",
    'it': "✍️ Scegli il nome di un gioco esistente."
}
MSG_CHOOSE_NEW_GAME_NAME = {
    'en': "✍️ Choose a new game name.",
    'it': "✍️ Scegli il nome di un nuovo gioco."
}

# MSG_WRITE_GAME_SPECIAL_RULES = {
#     'en': "✍️ If you want you can write down any special rule you want to set for the game (e.g., rymes, length of sentences, etc...), or press {}".format(BUTTON_SKIP['en']),
#     'it': "✍️ Inserisci se vuoi delle regole particolari da adottare nel gioco (ad esempio rime, lunghezza frasi, ecc...), o premi {}".format(BUTTON_SKIP['it']),
# }
MSG_SELECT_GAME_MODE = {
    'en': "✔️ Please select the game mode:\n  • {}: every players choose a sentence to be completed\n  • {}: you will choose all the sentences".format(BUTTON_MODE_DEFAULT['en'],BUTTON_MODE_TEACHER['en']),
    'it': "✔️ Seleziona la modalità di gioco:\n  • {}: ogni giocatore sceglie una frase da completare\n  • {}: tu sceglierai tutte le frasi".format(BUTTON_MODE_DEFAULT['it'],BUTTON_MODE_TEACHER['it'])
}
MSG_SELECT_GAME_TYPE = {
    'en': "✔️ Please select the game type:\n  • {}: continue the sentece\n  • {}: fill the gap".format(BUTTON_TYPE_COMPLETION['en'],BUTTON_TYPE_FILL['en']),
    'it': "✔️ Seleziona il tipo di gioco:\n  • {}: continua la frase\n  • {}: inserisci la parola mancante".format(BUTTON_TYPE_COMPLETION['it'],BUTTON_TYPE_FILL['it'])
}
MSG_SELECT_GAME_REWARD_MODE = {
    'en': "✔️ Please select the game reward mode:\n  • {}: solutions different from the original are possible\n  • {}: only one solution is possible".format(BUTTON_REWARD_MODE_CREATIVITY['en'],BUTTON_REWARD_MODE_EXACTNESS['en']),
    'it': "✔️ Seleziona il tipo di gioco:\n  • {}: soluzioni diversi dall'originale sono possibili d\n  • {}: solo una soluzione è possibile".format(BUTTON_REWARD_MODE_CREATIVITY['it'],BUTTON_REWARD_MODE_EXACTNESS['it'])
}
MSG_INSER_NUMBER_OF_HANDS = {
    'en': "🔢 Please insert the number of hands to play.",
    'it': "🔢 Seleziona il numero di mani da giocare."
}
MSG_TELL_SPECIAL_RULES = {
    'en': "🧭 {} has chosen the following rules for the game: {}",
    'it': "🧭 {} ha scelto le seguenti regole del gioco: {}"
}
MSG_GAME_NOT_YET_READY = {
    'en': '🤷‍♀️ The game *{}* has been just created, but still needs to be set up. Please try again in a bit.',
    'it': '🤷‍♀️ Il gioco *{}* è appena stato creato, ma deve essere ancora impostato. Riprova tra qualche istante.'
}
MSG_GAME_ALREADY_ACTIVE = {
    'en': '🤷‍♀️ A game with this name is already active. Choose another name.',
    'it': '🤷‍♀️ Un gioco con questo nome è già in corso. Scegli un altro nome.'
}
MSG_GAME_ALREADY_STARTED = {
    'en': '🤷‍♀️ No more seats availbel on this game.',
    'it': '🤷‍♀️ Non ci sono posti disponibili in questo gioco.'
}
MSG_NAME_NO_LONGER_AVAILBLE = {
    'en': "🤷‍♀️ The game *{}* is no longer available.",
    'it': "🤷‍♀️ Il gioco *{}* non è più disponibile."
}
MSG_NAME_DOES_NOT_EXIST = {
    'en': "🤷‍♀️ The game *{}* does not exist.",
    'it': "🤷‍♀️ Il gioco *{}* non esiste."
}
MSG_GAME_NAME_ALREADY_STARTED = {
    'en': "🤷‍♀️ The game *{}* has already started.",
    'it': "🤷‍♀️ Il gioco *{}* è già iniziato."
}
MSG_NEW_GAME_CONFIRM = {
    'en': '🆕 No game *{}* exists. Do you want to create it?',
    'it': '🆕 Il gioco *{}* non esiste. Vuoi crearne uno?'
}
MSG_WRONG_INPUT_NUMBER_OF_PLAYERS = {
    'en': '⛔️ You must enter a name between 3 and 100',
    'it': '⛔️ Devi inserire un numero da 3 a 100'
}
MSG_WRONG_COMMAND = {
    'en': '⛔️ Wrong command',
    'it': '⛔️ Comando non riconosciuto'
}
MSG_CANT_JOIN_ALREADY_IN_GAME = {
    'en': '⛔️ You can open a new game when you are already in a game. You have to exit first.',
    'it': "⛔️ Non puoi unirti ad un gioco quando sei già all'interno di un gioco. Devi prima uscire."
}
MSG_NUMBER_OF_PLAYERS = {
    'en': "🔢 Please enter the maximum number of players for this game.",
    'it': "🔢 Inserisci il numero massimo dei giocatori per questo gioco."
}
MSG_ENTERING_GAME_X = {
    'en': "🏁 You entered game *{}*.",
    'it': "🏁 Sei entrato/a nel gioco *{}*."
}
MSG_GAME_HAS_STARTED_WITH_PLAYERS = {
    'en': "🏁Game has started with players: {}",
    'it': "🏁Il gioco è iniziato con i giocoatori: {}"
}
MSG_NOT_ENOUGH_PLAYERS = {
    'en': "📮 There needs to be at least {} players in the game to start. Please invite other players to the game or press the button below {} to announce it publicly.".format(parameters.MIN_NUM_OF_PLAYERS, BUTTON_ANNOUNCE_GAME_PUBLICLY['en']),
    'it': "📮 Occorrono almeno {} giocatori/ici per iniziare il gioco. Invita altri partecipanti al gioco o premi il pulsante {} per annunciarlo pubblicamente.".format(parameters.MIN_NUM_OF_PLAYERS, BUTTON_ANNOUNCE_GAME_PUBLICLY['en']),
}
MSG_INVITE_PEOPLE_ANNOUNCE_OR_START = {
    'en': "📮 Please invite other players to the game *{3}* or press the button {0} to announce it publicly. If there are at least {1} players in the game you can start with {2}.".format(BUTTON_ANNOUNCE_GAME_PUBLICLY['en'],parameters.MIN_NUM_OF_PLAYERS, BUTTON_STOP_WAITING_START_GAME['en'],"{}"),
    'it': "📮 Invita altri/e giocatori/trici ad unirsi al gioco *{3}* o premere il pulsante {0} per annunciarlo pubblicamente. Se ci sono almento {1} giocatori nel gioco puoi iniziare comunque premendo {2}.".format(BUTTON_ANNOUNCE_GAME_PUBLICLY['en'],parameters.MIN_NUM_OF_PLAYERS, BUTTON_STOP_WAITING_START_GAME['en'],"{}"),
}
MSG_ANNOUNCE_GAME_PUBLICLY = {
    'en': "📮 New game created by {} with {} people and {} seats remaining. Join th egame clicking on {}.",
    'it': "📮 Nuovo gioco creato da {} con {} persone e {} posti rimanenti. Unisciti premendo su {}."
}
MSG_SENT_ANNOUNCEMENT = {
    'en': "📮 Announcement sent! Let's wait for new players to join.",
    'it': "📮 Annuncio inviato! Aspettiamo che altri/e giocatori/trici si uniscano."
}
MSG_PLAYER_X_JOINED_GAME = {
    'en': "👤 Player *{}* joined the game.",
    'it': "👤 Il/a giocatore/ice *{}* si è unito/a al gioco."
}
MSG_WAITING_FOR_X_PLAYERS_PL = {
    'en': "😴 Waiting for {} more players...\n📮 Please invite other players to the game *{}*.",
    'it': "😴 Stiamo aspettando {} altri/e giocatori/trici...\n📮 Invita altri/e giocatori/trici ad unirsi al gioco *{}*."
}
MSG_WAITING_FOR_X_PLAYERS_SG = {
    'en': "😴 Waiting for {} more player...\n📮 Please invite another player to the game *{}*.",
    'it': "😴 Stiamo aspettando {} altro/a giocatore/ice...\n📮 Invita un altro/a giocatore/ice ad unirsi al gioco *{}*."
}
MSG_READY_TO_START = {
    'en': "👟 All seats have been occupied, let's start the game!",
    'it': "👟 Tutti i posti sono stati occupati, iniziamo il gioco!"
}
MSG_HAND_INFO = {
    'en': '🖐 Current Hand: {}\n📖 Reader: {} ⭐️',
    'it': '🖐 Mano: {}\n📖 Lettore: {} ⭐️'
}
MSG_READER_WRITES_BEGINNING = {
    'en': '✍️ Please write down the beginning of a sentence or a paragraph from a book.',
    'it': "✍️ Scrivi l'inizio di una frase o di un paragrafo di un libro."
}
MSG_READER_WRITES_SENTENCE_WITH_GAP = {
    'en': '✍️ Please write down a sentence with the missing gap indicated with 3 question marks (\'???\' with no spaces).',
    'it': "✍️ Scrivi una frase con una parte da completare indicata da 3 punti di domanda (\'???\' senza spazi)."
}
MSG_READER_WRITES_TEXT_INFO = {
    'en': '✍️ If you want, you can write down the info about the text or press {}.'.format(BUTTON_SKIP['en']),
    'it': "✍️ Se vuoi puoi scrivere alcune informazioni sul testo o premi {}.".format(BUTTON_SKIP['it']),
}
MSG_WRITERS_WAIT_READER_BEGINNING = {
    'en': "😴 Let's wait for {} ⭐️ to write down the beginning of a paragraph from a book.",
    'it': "😴 Aspettiamo che {} ⭐️ scriva l'inizio di una frase o di un paragrafo di un libro."
}
MSG_WRITERS_WAIT_READER_SENTENCE_WITH_GAP = {
    'en': "😴 Let's wait for {} ⭐️ to write down the sentence with a missing gap.",
    'it': "😴 Aspettiamo che {} ⭐️ scriva una frase con una parte mancante da completare."
}
MSG_WRITERS_WAIT_READER_TEXT_INFO = {
    'en': "😴 Let's wait for {} ⭐️ to write down additional info about the inserted text.",
    'it': "😴 Aspettiamo che {} ⭐️ scriva alcune informazioni sul testo inserito."
}
MSG_WRITERS_TEXT_INFO = {
    'en': "💡 extra information: *{}*.",
    'it': "💡 informazioni aggiuntive: *{}*."
}
MSG_PLAYERS_BEGINNING_INTRO = {
    'en': "📖 This is the chosen beginning by {}",
    'it': "📖 Questo è l'inizio scelto da {}"
}
MSG_PLAYERS_SENTENCE_WITH_GAP_INTRO = {
    'en': "📖 This is the sentence with a missing gap inserted by {}:",
    'it': "📖 Questo è la frase con la parte mancante inserita da {}:"
}
MSG_READER_WRITE_CORRECT_CONTINUATION = {
    'en': "✍️ Please, write down the correct continuation of the sentence.",
    'it': "✍️ Scrivi la corretta continuazione del testo inserito."
}
MSG_WRITERS_WRITE_CONTINUATION = {
    'en': "✍️ Please, write down a possible continuation of the sentence.",
    'it': "✍️ Scrivi una possibile continuazione del testo."
}
MSG_READER_WRITE_CORRECT_MISSING_PART = {
    'en': "✍️ Please, write down the correct completion for the missing part of the sentence.",
    'it': "✍️ Scrivi la corretta parte mancante della frase."
}
MSG_WRITERS_WRITE_MISSING_PART = {
    'en': "✍️ Please, write down a possible completion for the missing part of the sentence.",
    'it': "✍️ Scrivi una possibile completamento della parte mancante della frase."
}
MSG_ALREADY_SENT_CONTINUATION = {
    'en': "🤐 You have already sent a continuation!\n😴 Let's wait for the other players to write the continuations.",
    'it': "🤐 Hai già inserito la continuazione!\n😴 Aspetta che gli altri/e giocatori/trici inseriscano la loro coninuazione."
}
MSG_X_GAVE_CONTINUATION_WAITING_FOR_PLAYERS_NAME_CONTINUATION = {
    'en': "📝 Received continuation of *{}*. Let's wait for: {} 😴",
    'it': "📝 Ricevuta la continuazione di *{}*. Rimaniamo in attesa di: {} 😴"
}
MSG_INTRO_NUMBERED_TEXT = {
    'en': "📝 These are all the complete texts in random order:",
    'it': "📝 Queste sono tutti i testi completi in ordine casuale:"
}
MSG_WAIT_FOR_PLAYERS_TO_VOTE_PL = {
    'en': "😴 Let's wait for the other players to guess.",
    'it': "😴 Rimaniamo in attesa della scelta degli altri/e giocatori/trici."
}
MSG_VOTE = {
    'en': "🗳️ Please select the number of the continuation you think it's the correct one.",
    'it': "🗳️ Seleziona il numero del testo che ritieni essere quella corretta."
}
MSG_GUESSED_NO_VOTE = {
    'en': "😀 Wow, you entered a continuation which is identical to the oriiginal one! no need to vote!",
    'it': "😀 Wow, hai inserito la continuazione che è identica all'originale!\nNon hai bisogno di votare!",
}
MSG_X_PLAYER_SG_GUESSED_EXACT_CONTINUATIONS = {
    'en': "🤠 {} has inserted the original continuation and doesn't need to vote!",
    'it': "🤠 {} ha inserito la continuazione originale e non deve votare!",
}
MSG_X_PLAYERS_PL_GUESSED_EXACT_CONTINUATIONS = {
    'en': "🤠 {} have inserted the original continuation and don't need to vote!",
    'it': "🤠 {} hanno inserito la continuazione originale e non devono votare!",
}
MSG_THANKS = {
    'en': "😀 Thanks!",
    'it': "😀 Grazie!"
}
MSG_ALREADY_VOTED_WAITING_FOR = {
    'en': "🤐 You already voted!\n😴 Let's wait for: {}",
    'it': "🤐 Hai già votato!\n😴 Rimani in attesa di: {}"
}
MSG_X_VOTED = {
    'en': "✔️ *{}* has chosen.",
    'it': "✔️ *{}* ha fatto la sua scelta."
}
MSG_WAIT_FOR = {
    'en': "😴 Let's wait for: {}",
    'it': "😴 Rimaniamo in attesa di: {}"
}
MSG_VOTE_RECAP = {
    'en': "🗳️ These are the completion being made:",
    'it': "🗳️ Questi sono i completamenti effettuati:"
}
MSG_VOTED_BY = {
    'en': "Voted by: {}",
    'it': "Votato da: {}"
}
MSG_GUESSED_BY_AND_VOTED_BY = {
    'en': "Guessed by: {}. Voted by: {}.",
    'it': "Indovinato da: {}. Votato da: {}."
}
MSG_POINT_HAND_SUMMARY = {
    'en': "🖐 LAST HAND POINTS",
    'it': "🖐 PUNTI ULTIMA MANO"
}
MSG_POINT_GAME_SUMMARY = {
    'en': "🎲 GAME POINTS",
    'it': "🎲 PUNTI GIOCO"
}
MSG_POINT_GAME_PARTIAL_SUMMARY = {
    'en': "🎲 GAME POINTS (PARTIAL)",
    'it': "🎲 PUNTI GIOCO (PARZIALI)"
}
MSG_EXIT_GAME = {
    'en': "🚪 Game has terminated because {} exited.",
    'it': "🚪 Gioco terminato perché {} è uscito/a."
}
MSG_NO_GAME_TO_EXIT = {
    'en': "⛔️ You are not in a game",
    'it': "⛔️ Non sei in un gioco"
}
MSG_ONLY_CREATOR_CAN_TERMINATE_GAME = {
    'en': "⛔️ Only the person who has created the game can terminate it.",
    'it': "⛔️ Solo la persona che ha creato il gioco può terminarlo."
}
MSG_NO_GAME_NO_CHAT = {
    'en': "⛔️ You are not in a game. You can send a chat message only inside a game.",
    'it': "⛔️ Non sei in un gioco. Puoi mandare messaggi di testo solo in un gioco."
}
MSG_CHAT_MSG_TOO_LONG = {
    'en': "⛔️ Message too long (max 200 characters).",
    'it': "⛔️ Messagio troppo lungo (max 200 caratteri).",
}
MSG_CHAT_NO_PLAYERS_IN_ROOM = {
    'en': "⛔️ No players in game to send the message to.",
    'it': "⛔️ Non c'è alcun  giocatore/ice a cui mandare il messaggio.",
}
MSG_CHAT_SENT = {
    'en': "📩 Message sent.",
    'it': "📩 Messaggio inviato."
}
MSG_WINNER_SINGULAR = {
    'en': "🏆 The winner of the game is *{}*",
    'it': "🏆 Il/a vincitore/trice del gioco è *{}*"
}
MSG_WINNER_PLURAL = {
    'en': "🏆 The winners of the game are *{}*",
    'it': "🏆 I/le vincitori/trici del gioco sono *{}*"
}

MSG_WRONG_INPUT_ONLY_TEXT_ACCEPTED = {
    'en': "⛔️ Wrong input, only text is accepted here.",
    'it': "⛔️ Input non valido, devi inserire solo del testo."
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
MSG_WRONG_INPUT_INSRT_NUMBER = {
    'en': '⛔️ Wrong input, please insert a number 🔢',
    'it': '⛔️ Input non valido, per favore inserisci un numero 🔢'
}
MSG_WRONG_INPUT_USE_BUTTONS = {
    'en': '⛔️ Wrong input, please use buttons below 🎛',
    'it': '⛔️ Input non valido, per favore usa i pulsanti 🎛'
}
MSG_WRONG_BUTTON_INPUT = {
    'en': '⛔️ Wrong input, you probably pressed a button twice.',
    'it': '⛔️ Input non valido, probabilmente hai premuto un tasto due volte.'
}
MSG_INPUT_TOO_SHORT = {
    'en': '⛔️ Input too short.',
    'it': '⛔️ Input troppo corto.'
}
MSG_INPUT_NO_MARKDOWN = {
    'en': '⛔️ Input cannot contains the following characters: {}'.format(utility.escape_markdown(utility.MARKDOWN_CHARS)),
    'it': '⛔️ Il testo non può contenere i caratteri: {}'.format(utility.escape_markdown(utility.MARKDOWN_CHARS))
}
MSG_INPUT_NO_GAP = {
    'en': '⛔️ The text you have inserted does not contain the sequence of 3 question marks (\'???\') to indicate the missing part to be completed.',
    'it': '⛔️ Il testo inserito non contiene la sequenza di 3 punti di domanda (\'???\') per indicare la parte mancante da completare.'
}
MSG_COMMAND_NOT_RECOGNIZED = {
    'en': '⛔️ The command has not been recognised.',
    'it': '⛔️ Comando non riconosciuto.'
}

ALL_BUTTONS_TEXT_LIST = [v[l] for l in LANGUAGES for k,v in globals().items() if k.startswith('BUTTON_')]

def text_is_button_or_digit(text):
    import utility
    return text in ALL_BUTTONS_TEXT_LIST or utility.represents_int(text)