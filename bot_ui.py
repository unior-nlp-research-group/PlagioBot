import parameters
import utility

# ================================
# SYMBOLS
# ================================
# 🤗📝✏️
CHECK_SYMBOL = '✅'
CANCEL_SYMBOL = '❌'
BLACK_CHECK_SYMBOL = '✔️'
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
BUTTON_REMOVE = {
    'en': "🗑️ DELETE",
    'it': "🗑️ CANCELLA",
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
BUTTON_GAME_SETTINGS= {
    'en': "⚙️ Game Settings",
    'it': "⚙️ Impostazioni di Gioco"
}
BUTTON_START_GAME= {
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
BUTTON_GAME_TYPE = {
    'en': "👣🕳🐡 EXERCISE TYPE",
    'it': "👣🕳🐡 TIPO ESERCIZIO"
}
BUTTON_GAME_TYPE_CONTINUATION = {
    'en': "👣 CONTINUATION",
    'it': "👣 CONTINUAZIONE"
}
BUTTON_GAME_TYPE_FILL = {
    'en': "🕳 FILL",
    'it': "🕳 RIEMPI"
}
BUTTON_GAME_TYPE_SUBSTITUTION = {
    'en': "🐡 SUBSTITUTION",
    'it': "🐡 SOSTITUZIONE"
}
BUTTON_GAME_DEMO_MODE = {
    'en': "🎮 DEMO MODE",
    'it': "🎮 MODALITÀ DEMO"
}
BUTTON_GAME_TRANSLATE_HELP = {
    'en': "👁️‍🗨️ AUTOMATIC TRANSLATE",
    'it': "👁️‍🗨️ TRADUZIONE AUTOMATICA"
}
BUTTON_GAME_CONTROL = {
    'en': "⚛️🧑‍🏫 CONTROL",
    'it': "⚛️🧑‍🏫 CONTROLLO"
}
BUTTON_GAME_CONTROL_DEFAULT = {
    'en': "⚛️ DEFAULT",
    'it': "⚛️ TRADIZIONALE"
}
BUTTON_GAME_CONTROL_TEACHER = {
    'en': "🧑‍🏫 TEACHER",
    'it': "🧑‍🏫 INSEGNANTE"
}
BUTTON_GAME_CONTROL_DEMO = {
    'en': "🤖 DEMO",
    'it': "🤖 DEMO"
}
BUTTON_REWARD_MODE = {
    'en': "🎭🎯 REWARD MODE",
    'it': "🎭🎯 RICOMPENSA"
}
BUTTON_REWARD_MODE_CREATIVITY = {
    'en': "🎭 CREATIVITY",
    'it': "🎭 CREATIVITÀ"
}
BUTTON_REWARD_MODE_EXACTNESS = {
    'en': "🎯 EXACTNESS",
    'it': "🎯 ESATTEZZA"
}
BUTTON_SPECIAL_RULES = {
    'en': "✍️ SPECIAL RULES",
    'it': "✍️ REGOLE PARTICOLARI"
}
BUTTON_HANDS_NUMBER = {
    'en': "🔢🖐️ HANDS NUMBER",
    'it': "🔢🖐️ NUMERO MANI"
}
BUTTON_ASK_EXTRA_INFO = {
    'en': "ℹ️ ASK EXTRA INFO",
    'it': "ℹ️ CHIEDI INFO AGGIUNTIVE"
}
BUTTON_NO_CORRECT_ANSWER = {
    'en': "❌ NONE",
    'it': "❌ NESSUNA"
}
BUTTON_NO_CORRECT_ANSWER_NO_EMOJI = {
    'en': "NONE",
    'it': "NESSUNA"
}
BUTTON_SUBMIT = {
    'en': "✅ SUBMIT",
    'it': "✅ INVIA"
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
    'en': "⛔ No /start command availale during the game. Type /exit if you want to abandon the game.",
    'it': "⛔ Il comando /start non è disponibile durante il gioco. Scrivi /exit se vuoi terminare il gioco."
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
MSG_SETTINGS_RECAP = {
    'en': "⚙️ Settings:",
    'it': "⚙️ Impostazioni:"
}
MSG_NUM_PLAYERS = {
    'en': "👤 One hand per player",
    'it': "👤 Una mano per giocatore"
}
MSG_WRITE_GAME_SPECIAL_RULES = {
    'en': "✍️ If you want you can write down any special rule you want to set for the game (e.g., rymes, length of sentences, etc...).",
    'it': "✍️ Inserisci se vuoi delle regole particolari da adottare nel gioco (ad esempio rime, lunghezza frasi, ecc...).",
}
MSG_CURRENT_GAME_SPECIAL_RULES = {
    'en': "*Current special rules*: {}",
    'it': "*Regole particolari attuali*: {}"
}
MSG_SELECT_GAME_TYPE = {
    'en': "Please select the game type:",
    'it': "Seleziona il tipo di gioco:"
}
MSG_GAME_TYPE_CONTINUATION_DESCR = {
    'en': "continue the sentece",
    'it': "continuare la frase"
}
MSG_GAME_TYPE_FILL_DESCR = {
    'en': "fill the gap",
    'it': "inserire la parola mancante"
}
MSG_GAME_TYPE_SUBSTITUTION_DESCR = {
    'en': "replace a word (sequence) in a sentence",
    'it': "sostituire una o più parole in una frase"
}
MSG_GAME_DEMO_MODE = {
    'en': "Please select if you want sentences to be generated automatically.",
    'it': "Indica se vuoi generare le frasi automaticamente."
}
MSG_GAME_TRANSLATE = {
    'en': "Please select if you want to provide the *automatic translation* of the sentence to be completed.",
    'it': "Indica se vuoi fornire la *traduzione automatica* della frase da completare."
}
MSG_SELECT_GAME_CONTROL = {
    'en': "Please select the game mode:",
    'it': "Seleziona la modalità di gioco:"
}
MSG_GAME_CONTROL_DEFAULT_DESCR = {
    'en': "every players choose a sentence to be completed",
    'it': "ogni giocatore sceglie una frase da completare"
}
MSG_GAME_CONTROL_TEACHER_DESCR = {
    'en': "you (the teacher) will choose all the sentences",
    'it': "tu (l'insegnante) sceglierai tutte le frasi"
}
MSG_SELECT_GAME_REWARD_MODE = {
    'en': "Please select the game reward mode:",
    'it': "Seleziona il tipo di ricompensa:"
}
MSG_GAME_REWARD_MODE_CREATIVITY_DESCR = {
    'en': "encourage solutions different from the original",
    'it': "incoraggia soluzioni diversi dall'originale"
}
MSG_GAME_REWARD_MODE_EXACTNESS_DESCR = {
    'en': "only one solution is possible",
    'it': "solo una soluzione è possibile"
}
MSG_INSERT_NUMBER_OF_HANDS = {
    'en': "🔢🖐️ Please insert the number of hands to play.\n\n*Current hands*: {}",
    'it': "🔢🖐️ Seleziona il numero di mani da giocare.\n\n*Mani attuali*: {}"
}
MSG_TELL_SPECIAL_RULES = {
    'en': "🧭 {} has chosen the following rules for the game: {}",
    'it': "🧭 {} ha scelto le seguenti regole del gioco: {}"
}
MSG_ENABLE_TEXT_INFO = {
    'en': "ℹ️ Specify whether the reader can specify additional infor in each hand.",
    'it': "ℹ️ Indica se il lettore può inserire info aggiuntive in ogni mano."
}
MSG_GAME_ALREADY_ACTIVE = {
    'en': '🤷‍♀️ A game with this name is already active. Choose another name.',
    'it': '🤷‍♀️ Un gioco con questo nome è già in corso. Scegli un altro nome.'
}
MSG_GAME_NOT_AVAILABLE = {
    'en': '🤷‍♀️ The game is no longer available.',
    'it': '🤷‍♀️ Sessione di gioco non più disponibile.'
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
MSG_CANT_JOIN_GAME = {
    'en': '⛔️ The game you want to join has already started.',
    'it': "⛔️ Il gioco a cui vuoi unirti è già iniziato."
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
MSG_CURRENT_PLAYERS = {
    'en': '👥 {} players: {}',
    'it': '👥 {} giocatori: {}'
}
MSG_CURRENT_PLAYER = {
    'en': '👤 {} player: {}',
    'it': '👤 {} giocatore: {}'
}
MSG_INVITE_PEOPLE_ANNOUNCE_OR_START = {
    'en': "📮 Please invite other players to the game *{3}* or press the button {0} to announce it publicly. If there are at least {1} players in the game you can start with {2}.".format(BUTTON_ANNOUNCE_GAME_PUBLICLY['en'],parameters.MIN_NUM_OF_PLAYERS, BUTTON_START_GAME['en'],"{}"),
    'it': "📮 Invita altri/e giocatori/trici ad unirsi al gioco *{3}* o premere il pulsante {0} per annunciarlo pubblicamente. Se ci sono almento {1} giocatori nel gioco puoi iniziare comunque premendo {2}.".format(BUTTON_ANNOUNCE_GAME_PUBLICLY['it'],parameters.MIN_NUM_OF_PLAYERS, BUTTON_START_GAME['it'],"{}"),
}
MSG_INVITE_PEOPLE_START = {
    'en': "📮 Please invite other players to the game *{2}*. If there are at least {0} players in the game you can start with {1}.".format(parameters.MIN_NUM_OF_PLAYERS, BUTTON_START_GAME['en'],"{}"),
    'it': "📮 Invita altri/e giocatori/trici ad unirsi al gioco *{2}*. Se ci sono almento {0} giocatori nel gioco puoi iniziare comunque premendo {1}.".format(parameters.MIN_NUM_OF_PLAYERS, BUTTON_START_GAME['en'],"{}"),
}
MSG_ANNOUNCE_GAME_PUBLICLY = {
    'en': "📮 New game created by {}. Join the game by clicking on {}.",
    'it': "📮 Nuovo gioco creato da {}. Unisciti premendo su {}."
}
MSG_SENT_ANNOUNCEMENT = {
    'en': "📮 Announcement sent! Let's wait for new players to join.",
    'it': "📮 Annuncio inviato! Aspettiamo che altri/e giocatori/trici si uniscano."
}
MSG_PLAYER_X_JOINED_GAME = {
    'en': "👤 Player *{}* joined the game.",
    'it': "👤 Il/a giocatore/ice *{}* si è unito/a al gioco."
}
MSG_WAITING_FOR_START_GAME = {
    'en': "😴 Waiting to start the game *{}*.\n📮 You can still invite other players to the game.",
    'it': "😴 Stiamo aspettando che inizi il gioco *{}*.\n📮 Puoi ancora invitare altri/e giocatori/trici ad unirsi."
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
MSG_READER_WRITES_SENTENCE_WITH_SUBSTITUTION = {
    'en': '✍️ Please write down a sentence with the part to substitute.',
    'it': "✍️ Scrivi una frase con una parte da sostituire."
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
MSG_WRITERS_WAIT_READER_SENTENCE_WITH_SUBSTITUTION = {
    'en': "😴 Let's wait for {} ⭐️ to write down the sentence with a part to be replaced.",
    'it': "😴 Aspettiamo che {} ⭐️ scriva una frase con una parte da sostituire."
}
MSG_WRITERS_WAIT_READER_TEXT_INFO = {
    'en': "😴 Let's wait for {} ⭐️ to write down additional info about the inserted text.",
    'it': "😴 Aspettiamo che {} ⭐️ scriva alcune informazioni sul testo inserito."
}
MSG_WRITERS_WAIT_READER_WRITE_CORRECT_ANSWER = {
    'en': "😴 Let's wait for {} ⭐️ to write down the correct answer.",
    'it': "😴 Aspettiamo che {} ⭐️ scriva la risposta corretta."
}
MSG_WRITERS_WAIT_READER_WRITE_SUBSTITUTION_PART = {
    'en': "😴 Let's wait for {} ⭐️ to write the part of the sentence to be substituted.",
    'it': "😴 Aspettiamo che {} ⭐️ scriva la parte della frase che deve essere sostituita."
}
MSG_READER_WAIT_WRITERS_WRITE_SUBSTITUTION = {
    'en': "😴 Please wait that the other players write down their substituion proposal.",
    'it': "😴 Aspettiamo che gli altri giocatori scrivano la loro proposta di sostituzione."
}
MSG_READER_WAIT_WRITERS_WRITE_ANSWER = {
    'en': "😴 Please wait that the other players write down the correct answer.",
    'it': "😴 Aspettiamo che gli altri giocatori scrivano il loro completamento del testo."
}
MSG_WRITERS_TEXT_INFO = {
    'en': "💡 extra information: *{}*.",
    'it': "💡 informazioni aggiuntive: *{}*."
}
MSG_PLAYERS_INCOMPLETE_SENTENCE = {
    'en': "📖 This is the sentence that needs to be completed:\n{}",
    'it': "📖 Questa è la frase che deve essere completata:\n{}"
}
MSG_PLAYERS_SENTENCE_WITH_HIGHLITED_SUBSTITUTION = {
    'en': "📖 This is the sentence with the highlited part to be substituted:\n{}",
    'it': "📖 Questa è la frase con la parte evidenziata da sostituire:\n{}"
}
MSG_READER_WRITE_CORRECT_ANSWER = {
    'en': "✍️ Please, write down the correct answer of the sentence.",
    'it': "✍️ Scrivi il corretto completamento del testo inserito."
}
MSG_READER_WRITE_SUBSTITUTION_PART = {
    'en': "✍️ Please, write down the part of the sentence to substitute.",
    'it': "✍️ Scrivi la parte della frase da sostituire."
}
MSG_WRITERS_WRITE_ANSWER = {
    'en': "✍️ Please, write down a possible answer of the sentence.",
    'it': "✍️ Scrivi un possibile completamento del testo."
}
MSG_WRITERS_WRITE_SUBSTITUTION = {
    'en': "✍️ Please, write down a possible substitution of the highlited part.",
    'it': "✍️ Scrivi un possibile sostituzione della parte evidenziata."
}
MSG_ALREADY_SENT_ANSWER = {
    'en': "🤐 You have already sent your answer!\n😴 Let's wait for the other players.",
    'it': "🤐 Hai già mandato una risposta!\n😴 Aspettamo che gli altri/e giocatori/trici rispondano."
}
MSG_X_GAVE_ANSWER_WAITING_FOR_PLAYERS_NAMES = {
    'en': "📝 Received answer by *{}*. Let's wait for: {} 😴",
    'it': "📝 Ricevuta risposta da *{}*. Rimaniamo in attesa di: {} 😴"
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
    'en': "🗳️ Please select the number of the answer you think is the correct one.",
    'it': "🗳️ Seleziona il numero del completamento che ritieni essere quello corretto."
}
MSG_TEACHER_VOTE = {
    'en': "🧑‍🏫 Please *select the correct response(s)* (none, one, or more).",
    'it': "🧑‍🏫 Seleziona *la/e risposta/e corretta/e* (nessuna, una, o più di una)."
}
MSG_TEACHER_VOTE = {
    'en': "🧑‍🏫 Please *select the correct response(s)* (none, one, or more). Press on /recap\\_answers if you want to see the students' answers again.",
    'it': "🧑‍🏫 Seleziona *la/e risposta/e corretta/e* (nessuna, una, o più di una). Premi /recap\\_answers se vuoi vedere nuovamente le risposte degli studenti."
}
MSG_TEACHER_VOTE_AND_SUBMIT = {
    'en': "🧑‍🏫 Please select the correct responses (none, one, or more) and press SUBMIT to confirm. Press on /recap\\_answers if you want to see the students' answers again.",
    'it': "🧑‍🏫 Seleziona le risposste corrette (nessuna, una, o più di una) e premi INVIA per confermare. Premi /recap\\_answers se vuoi vedere nuovamente le risposte degli studenti."
}
MSG_NO_VOTE_ALL_BUT_ONE_GUESSED_CORRECTLY = {
    'en': "❌🗳️ No voting: only one player would have to vote for one possibility.",
    'it': "❌🗳️ Votazione assente: solo un giocatore dovrebbe votare per una sola possibilità."
}
MSG_NO_VOTE_ALL_GUESSED_CORRECTLY = {
    'en': "❌🗳️ No voting: all player inserted the correct answer.",
    'it': "❌🗳️ Votazione assente: tutti i giocatori hanno inserito la soluzione corretta."
}
MSG_GUESSED_NO_VOTE = {
    'en': "😀 Wow, you entered the correct answer!",
    'it': "😀 Wow, hai inserito la risposta coretta!",
}
MSG_X_PLAYER_SG_GUESSED_EXACT_ANSWERS = {
    'en': "🤠 {} has inserted the correct answer.",
    'it': "🤠 {} ha inserito la risposta corretta.",
}
MSG_X_PLAYERS_PL_GUESSED_EXACT_ANSWERS = {
    'en': "🤠 {} have inserted the correct answer.",
    'it': "🤠 {} hanno inserito la risopsta corretta.",
}
MSG_THANKS = {
    'en': "😀 Thanks!",
    'it': "😀 Grazie!"
}
MSG_WAIT_FOR_TEACHER_EVALUATION = {
    'en': "🧑‍🏫 Let's wait for the teacher's evaluation!",
    'it': "🧑‍🏫 Aspettiamo la valutazione dell'insegnante!"
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
    'en': "🗳️ Voting summary:",
    'it': "🗳 Risultato votazione:"
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
MSG_EXIT_GAME_EXPIRED = {
    'en': "🚪 Game has terminated because none made a move for long time.",
    'it': "🚪 Gioco terminato perché nessuno ha giocato per troppo tempo."
}
MSG_NO_GAME_TO_EXIT = {
    'en': "⛔️ You are not in a game",
    'it': "⛔️ Non sei in un gioco"
}
MSG_ONLY_CREATOR_CAN_TERMINATE_GAME = {
    'en': "⛔️ Only the person who has created the game can terminate it.",
    'it': "⛔️ Solo la persona che ha creato il gioco può terminarlo."
}
MSG_CHAT_INFO = {
    'en': "⛔️ To send a message to the other players, please type /chat followed by the message.",
    'it': "⛔️ Per mandare un messaggio agli altri giocatore, scrivi /chat seguito dal messaggio."
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
MSG_WRONG_INPUT_WAIT_FOR_TEACHER_TO_VOTE = {
    'en': "⛔️ Let's wait for the teacher's evaluation.",
    'it': "⛔️ Attendiamo la valutazione dell'insegnante."
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
    'en': '⛔️🔢 Wrong input, please insert a number.',
    'it': '⛔️🔢 Input non valido, per favore inserisci un numero.'
}
MSG_WRONG_INPUT_INSRT_NUMBER_BETWEEN = {
    'en': '⛔️🔢 Wrong input, please insert a number between {} and {}.',
    'it': '⛔️🔢 Input non valido, per favore inserisci un numero da {} a {}.'
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
MSG_INPUT_CONTAINS_SPACE_OR_MARKDOWN = {
    'en': '⛔️ Input cannot contain spaces or following characters: "{}".'.format(utility.escape_markdown(utility.MARKDOWN_CHARS)),
    'it': '⛔️ Input non può conotenere spazi o i caratteri: "{}".'.format(utility.escape_markdown(utility.MARKDOWN_CHARS))
}
MSG_INPUT_NO_MARKDOWN = {
    'en': '⛔️ Input cannot contains the following characters: {}'.format(utility.escape_markdown(utility.MARKDOWN_CHARS)),
    'it': '⛔️ Il testo non può contenere i caratteri: {}'.format(utility.escape_markdown(utility.MARKDOWN_CHARS))
}
MSG_INPUT_NO_GAP = {
    'en': '⛔️ The text you have inserted does not contain the sequence of 3 question marks (\'???\') to indicate the missing part to be completed.',
    'it': '⛔️ Il testo inserito non contiene la sequenza di 3 punti di domanda (\'???\') per indicare la parte mancante da completare.'
}
MSG_INPUT_NO_SUBSTITUTION = {
    'en': '⛔️ The text you have inserted does not contain parenthesis or they are not in the correct format.',
    'it': '⛔️ Il testo inserito non contiene le parentsi in formato corretto.'
}
MSG_INPUT_SUBSTITUION_NOT_IN_SENTENCE = {
    'en': '⛔️ The string you have inserted is not present in the original sentence, try again.',
    'it': '⛔️ Il testo inserito non è presente nella frase inserita precedentemente, prova di nuovo.'
}
MSG_INPUT_NO_VALID_SUBSTITUTION = {
    'en': '⛔️ The text you have inserted is identical to the one highlighted, try again.',
    'it': '⛔️ Il testo inserito è identico a quello evidenziato, riprova di nuovo.'
}
MSG_COMMAND_NOT_RECOGNIZED = {
    'en': '⛔️ The command has not been recognised.',
    'it': '⛔️ Comando non riconosciuto.'
}

ALL_BUTTONS_TEXT_LIST = [v[l] for l in LANGUAGES for k,v in globals().items() if k.startswith('BUTTON_')]

GAME_SETTINGS_BUTTON_VALUE_UX_MAPPING = lambda lang: {
    BUTTON_GAME_TYPE[lang]: {
        'CONTINUATION': BUTTON_GAME_TYPE_CONTINUATION[lang],
        'FILL': BUTTON_GAME_TYPE_FILL[lang],
        'SUBSTITUTION': BUTTON_GAME_TYPE_SUBSTITUTION[lang],
    },
    BUTTON_GAME_CONTROL[lang]: {
        'DEFAULT': BUTTON_GAME_CONTROL_DEFAULT[lang],
        'TEACHER': BUTTON_GAME_CONTROL_TEACHER[lang]
    },
    BUTTON_REWARD_MODE[lang]: {
        'CREATIVITY': BUTTON_REWARD_MODE_CREATIVITY[lang],
        'EXACTNESS': BUTTON_REWARD_MODE_EXACTNESS[lang]
    },
    BUTTON_ASK_EXTRA_INFO[lang]: {
        True: BUTTON_YES[lang],
        False: BUTTON_NO[lang]
    },
    BUTTON_GAME_DEMO_MODE[lang]: {
        True: BUTTON_YES[lang],
        False: BUTTON_NO[lang]
    },
    BUTTON_GAME_TRANSLATE_HELP[lang]: {
        True: BUTTON_YES[lang],
        False: BUTTON_NO[lang]
    }
}

def render_complete_text(game, incomplete_text, answer, markdown=True, uppercase=True):
    if uppercase:
            answer = answer.upper()
            incomplete_text = incomplete_text.upper()
    if game.game_type == 'CONTINUATION':        
        completed_text = "{} *{}*".format(incomplete_text, answer)
    elif game.game_type == 'FILL':        
        pre_gap, post_gap = game.get_incomplete_text_pre_post_gap()
        if uppercase:
            pre_gap, post_gap = pre_gap.upper(), post_gap.upper()
        completed_text = '{}*{}*{}'.format(pre_gap, answer, post_gap)
    else:
        assert game.game_type == 'SUBSTITUTION'
        original_answer = game.get_reader_answer().upper()
        completed_text = incomplete_text.replace(original_answer, '*{}*'.format(answer))


    if not markdown:
        completed_text = utility.remove_markdown(completed_text)
    return completed_text

def text_is_button_or_digit(text):
    import utility
    return text in ALL_BUTTONS_TEXT_LIST or utility.represents_int(text)

def check_multi_button(buttons_value_description, selected_value, multi_line=False):
    buttons = [
        '{}{}'.format(
            b,
            ' ' + CHECK_SYMBOL if v['value']==selected_value else ''            
        ) 
        for b,v in sorted(buttons_value_description.items(), key=lambda i: i[1]['order'])
    ]
    if multi_line:
        buttons = [[b] for b in buttons]
    return buttons

def check_multi_description(buttons_value_description, selected_value):
    return '\n'.join([
        '{} {}: {}'.format(
            CHECK_SYMBOL if v['value']==selected_value else BLACK_CHECK_SYMBOL, 
            b,
            v['description']
        ) 
        for b,v in sorted(buttons_value_description.items(), key=lambda i: i[1]['order'])
    ])

def make_keyboard_from_keyboard_action(kb_action):
    kb_action = {k:v for k,v in kb_action.items() if v['show_button']}
    rows_indexes = [v['row'] for k,v in kb_action.items()]
    num_rows = len(set(rows_indexes))
    if max(rows_indexes)!=num_rows-1:
        # recompute indexes
        for i,r in enumerate(rows_indexes):
            if i!=r:
                for v in kb_action.values():
                    if v['row']==r:
                        v['row'] = i
    kb_action_items = sorted(kb_action.items(), key=lambda kv:(kv[1]['row'],kv[1]['col']))
    kb = [[] for r in range(num_rows)]
    for k,v in kb_action_items:
        kb[v['row']].append(k)
    return kb