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
BUTTON_GAME_TYPE_SYNONYM = {
    'en': "🐡 SYNONYM",
    'it': "🐡 SINONIMO"
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
MSG_THE_TEACHER = {
    'en': "the *teacher*",
    'it': "l'*insegnante*"
}
BUTTON_ROUNDS_NUMBER = {
    'en': "🔢⭕️ ROUNDS NUMBER",
    'it': "🔢🖐️ NUMERO MANI"
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
BUTTON_NEXT_ROUND = {
    'en': "⭕️ NEXT ROUND",
    'it': "🖐 PROSSIMA MANO"
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
    'en': "✍️ Insert the name of an existing game.",
    'it': "✍️ Inserisci il nome di un gioco esistente."
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
    'en': "👤 One round per player",
    'it': "👤 Una mano per giocatore"
}
MSG_X_CHANGED_GAME_TYPE_TO_Y = {
    'en': "🕹️ {} changed the game type to {}.",
    'it': "🕹️ {} ha impostato la modalità di gioco su {}."
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
MSG_GAME_TYPE_SYNONYM_DESCR = {
    'en': "replace a word (sequence) in a sentence",
    'it': "sostituire una o più parole in una frase"
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
MSG_INSERT_NUMBER_OF_ROUNDS = {
    'en': "🔢⭕️ Please insert the number of rouds to play.\n\n*Current rounds*: {}",
    'it': "🔢🖐️ Seleziona il numero di mani da giocare.\n\n*Mani attuali*: {}"
}
MSG_INSTRUCTIONS = {
    'CONTINUATION': {
        'en': "ℹ️ *Instructions*: The game is set to *CONTINUATION* mode. Participants will be presented with an incomplete sentence (previously written by the reader), and need to provide a plausible continuation. Next, all completion (including the original) are collected and displayed in random order. Participants will then have to try guess which one is the original continuation. Each player will gain a point if she correctly guess the original completion, otherwise she will give the point to the player who wrote that completion.",
        'it': "ℹ️ *Instructions*: Il gioco è impostato in modalità *COMPLETAMENTO*. I partecipanti riceveranno una frase incompleta (scritta dal lettore in precedenza), e gli verrà chiesto di scrivere di completare la frase in maniera plausibile. Successivamente, verranno mostrate tutte le frase complete in ordine casuale (inclusa quella originale). I partecipanti dovranno quindi cercare di indovinare quale frase è quella originale. Ogni giocatore riceverà un punto se indovinerà correttamente, altrimenti darà il punto al giocatore che ha scritto la frase selezionata."
    },
    'FILL': {
        'en': "ℹ️ *Instructions*: The game is set to *FILL* mode.",
        'it': "ℹ️ *Instructions*: Il gioco è impostato in modalità *RIEMPIMENTO*."
    },
    'SYNONYM': {
        'en': "ℹ️ *Instructions*: The game is set to *SYNONYM* mode. In this game, you are presented with a sentence containing a part (one or more words) *highlighted in boldface*. Firstly you have to come up with a synonym of the highleted part. It can be a *single word* or *multiple words* that will retain the meaning of the sentence, once substituted to the boldfaced part. In the next phase, all answers are listed in random order; you will be asked to choose for one answer (from another player) that you think is also correct. If no other answer is correct, you can select *NONE*. Finally, the *teacher will validate all answers*: you will get 2 points if you answered correctly, 1 point if you chose correctly and -1 point if you chose incorrectly.",
        'it': "ℹ️ *Instructions*: Il gioco è impostato in modalità *SINONIMI*."
    }
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
MSG_GAME_HAS_STARTED_WITH_PLAYERS = {
    'en': "🏁Game has started with players: {}",
    'it': "🏁Il gioco è iniziato con i giocoatori: {}"
}
MSG_GAME_NAME = {
    'en': '🕹️ Game name: *{}*',
    'it': '🕹️ Nome gioco: *{}*'
}
MSG_GAME_SETTINGS_INFO = {
    'en': '⚙️ Mode: *{}* Control: *{}*',
    'it': '⚙️ Modalità: *{}* Controllo: *{}*'
}
MSG_CURRENT_PLAYERS = {
    'en': '👥 *{} players*: {}',
    'it': '👥 *{} giocatori*: {}'
}
MSG_CURRENT_PLAYER = {
    'en': '👤 *{} player*: {}',
    'it': '👤 *{} giocatore*: {}'
}
MSG_WAIT_FOR_MORE_PEOPLE_TO_START = {
    'en': "⌛ There needs to be at least {} players in the game to start it.".format(parameters.MIN_NUM_OF_PLAYERS),
    'it': "⌛ Ci devono essere almeno {} giocatori per iniziare.".format(parameters.MIN_NUM_OF_PLAYERS)
}
MSG_WAIT_FOR_X_TO_START_NEXT_ROUND = {
    'en': "⌛ Let's wait for {} to proceed to next round.",
    'it': "⌛ Attendiamo che {} avvii la prossima mano."
}
MSG_ANNOUNCE_GAME_PUBLICLY = {
    'en': "📮 New game created by {}. Join the game by clicking here: {}",
    'it': "📮 Nuovo gioco creato da {}. Unisciti premendo qua: {}"
}
MSG_SENT_ANNOUNCEMENT = {
    'en': "📮 Announcement sent! Let's wait for new players to join.",
    'it': "📮 Annuncio inviato! Aspettiamo che altri/e giocatori/trici si uniscano."
}
MSG_PLAYER_X_JOINED_GAME = {
    'en': "👤 Player {} joined the game.",
    'it': "👤 Il/a giocatore/ice {} si è unito/a al gioco."
}
MSG_YOU_CAN_START_GAME = {
    'en': "🏁 You can start the game by pressing the button *{}*.".format(BUTTON_START_GAME['en']),
    'it': "🏁 Puoi iniziare il gioco premendo il pulsante *{}*.".format(BUTTON_START_GAME['it'])
}
MSG_WAITING_FOR_START_GAME = {
    'en': "😴 Waiting for {} to start the game *{}*.",
    'it': "😴 Stiamo aspettando che {} faccia partire il gioco *{}*."
}
MSG_INVITE_OTHER_PLAYERS_ANNOUNCE = {
    'en': "📮 You can invite other players to the game. If you want you can press the button *{}* to announce it publicly to all users.".format(BUTTON_ANNOUNCE_GAME_PUBLICLY['en']),
    'it': "📮 Puoi invitare altri/e giocatori/trici ad unirsi. Se vuoi puoi mandare un invito a tutti gli utenti premendo il pulsante *{}*".format(BUTTON_ANNOUNCE_GAME_PUBLICLY['it'])
}
MSG_CHAT_INFO = {
    'en': "💬 To chat with other players, please type /chat followed by the message.",
    'it': "💬 Per chattare con gli altri giocatori, scrivi /chat seguito dal messaggio."
}
MSG_CURRENT_ROUND = {
    'en': '⭕️ Current round: {}',
    'it': '🖐 Mano: {}'
}
MSG_READER_NAME = {
    'en': '📖 Reader: {}',
    'it': '📖 Lettore: {}'
}
MSG_WRITE_INCOMPLETE = {
    'CONTINUATION': {
        'en': '✍️ Please write down the beginning of a sentence.',
        'it': "✍️ Scrivi l'inizio di una frase."
    },
    'FILL': {
        'en': '✍️ Please write down a sentence with the missing gap indicated with 3 question marks (\'???\' with no spaces).',
        'it': "✍️ Scrivi una frase con una parte da completare indicata da 3 punti di domanda (\'???\' senza spazi)."
    },
    'SYNONYM': {
        'en': '✍️ Please write down a sentence containing a part to substitute.',
        'it': "✍️ Scrivi una frase con una parte da sostituire."
    }
}
MSG_WAIT_READER_WRITE_INCOMPLETE = {
    'CONTINUATION': {
        'en': "😴 Let's wait for {} to write down the beginning of a sentence.",
        'it': "😴 Aspettiamo che {} scriva l'inizio di una frase."
    },
    'FILL': {
        'en': "😴 Let's wait for {} to write down the sentence with a missing gap.",
        'it': "😴 Aspettiamo che {} scriva una frase con una parte mancante da completare."
    },
    'SYNONYM': {
        'en': "😴 Let's wait for {} to write down the sentence with a part to be substituted.",
        'it': "😴 Aspettiamo che {} scriva una frase con una parte da sostituire."
    }
}
MSG_WRITE_CORRECT_ANSWER = {
    'CONTINUATION': {
        'en': "✍️ Please, write down the original continuation of the sentence.",
        'it': "✍️ Scrivi la continuazione originale della frase."
    },
    'FILL': {
        'en': "✍️ Please, write down the original text in the gap.",
        'it': "✍️ Scrivi la parte mancante della frase."
    },
    'SYNONYM': {
        'en': "✍️ Please, write down the part of the sentence to substitute.",
        'it': "✍️ Scrivi la parte della frase da sostituire."
    }
}
MSG_WAIT_READER_WRITE_CORRECT_ANSWER = {
    'CONTINUATION': {
        'en': "😴 Let's wait for {} to write down the original continuation.",
        'it': "😴 Aspettiamo che {} scriva la continuazione corretta."
    },
    'FILL': {
        'en': "😴 Let's wait for {} to write down the original text in the gap.",
        'it': "😴 Aspettiamo che {} scriva la parte mancante della frase."
    },
    'SYNONYM': {
        'en': "😴 Let's wait for {} to write down the part of the sentence to substitute.",
        'it': "😴 Aspettiamo che {} scriva la parte della frase da sostituire."
    }
}
MSG_WAIT_WRITERS_WRITE_ANSWERS = {
    'CONTINUATION': {
        'en': "😴 Please wait for the other players to complete the sentence.",
        'it': "😴 Aspettiamo che gli altri giocatori completino la frase."
    },
    'FILL': {
        'en': "😴 Please wait for the other players to complete the sentence.",
        'it': "😴 Aspettiamo che gli altri giocatori completino la frase."
    },
    'SYNONYM': {
        'en': "😴 Please wait for the other players to write down their substitution proposals.",
        'it': "😴 Aspettiamo che gli altri giocatori scrivano le loro proposte di sostituzione."
    }    
}
MSG_WRITERS_WRITE_ANSWER = {
    'CONTINUATION': {
        'en': "✍️ Please, write down a plausible completion of the sentence.",
        'it': "✍️ Scrivi una possibile continuazione della frase."
    },
    'FILL': {
        'en': "✍️ Please, write down some text that fits the gap.",
        'it': "✍️ Scrivi una possibile riempimento dello spazio della frase."
    },
    'SYNONYM': {
        'en': "✍️ Please, write down a synonym of the boldfaced part of the sentence (*{}*). It can be one or more words. Please do not type the whole sentence but only the part to substitute!",
        'it': "✍️ Scrivi un sinonimo della parte del testo in grassetto (*{}*). Può essere una o più parole. Non inserire la frase intera ma solo la parte da sostituire."
    }
}

MSG_ROUND_NUM = {
    'en': "⭕️ Round {}",
    'it': "🖐 Mano {}"
}
MSG_JUMP_TO_NEXT_PHASE = {
    'en': "🦘 You can decide to jump to the next phase with the command /jump",
    'it': "🦘 Puoi saltare alla fase successiva con il comando /jump"
}
MSG_TEACHER_HAS_JUMPED_TO_NEXT_PHASE = {
    'en': "🦘 The teacher has decided to jump to the next phase without waiting for all the answers.",
    'it': "🦘 L'insegnante ha deciso di saltare alla fase successiva senza aspettare tutte le risposte."
}
MSG_PLAYERS_INCOMPLETE_SENTENCE = {
    'en': "📖 This is the sentence that needs to be completed:\n\n{}",
    'it': "📖 Questa è la frase che deve essere completata:\n\n{}"
}
MSG_PLAYERS_SENTENCE_WITH_HIGHLITED_SYNONYM = {
    'en': "📖 This is the sentence with the boldfaced part to be substituted by a synonym:\n\n{}",
    'it': "📖 Questa è la frase con la parte in grassetto da sostituire con un sinonimo:\n\n{}"
}
MSG_ALREADY_SENT_ANSWER = {
    'en': "🤐 You have already sent your answer!\n😴 Let's wait for the other players.\n👀Use /status to know who is missing.",
    'it': "🤐 Hai già mandato una risposta!\n😴 Aspettamo che gli altri/e giocatori/trici rispondano.\n👀Usa /status per sapere chi manca."
}
RECEIVED_ANSWER_BY = {
    'en': "📝 Received answer by {}.",
    'it': "📝 Ricevuta risposta da {}."
}
MSG_WAITING_FOR = {
    'en': "😴 We are waiting for: {}",
    'it': "😴 Siamo in attesa di: {}"
}
MSG_ALL_ANSWERS_RECEIVED = {
    'en': "📚 All answers have been received.",
    'it': "📚 Ricevute tutte le risposte."
}
MSG_INTRO_NUMBERED_TEXT = {
    'en': "📝 These are all the possibile answers in random order:",
    'it': "📝 Queste sono tutte le risposte in ordine casuale:"
}
MSG_WAIT_FOR_PLAYERS_TO_SELECT_PL = {
    'en': "😴 Let's wait for the other players to make their choice.",
    'it': "😴 Rimaniamo in attesa che gli altri/e giocatori/trici facciano la loro scelta."
}
MSG_SELECTION = {
    'CONTINUATION': {
        'en': "🔢 Select the number of the continuation you think is the original one.",
        'it': "🔢 Seleziona il numero associato alla continuazione che ritieni essere quella originale."
    },
    'FILL': {
        'en': "🔢 Select the number of the completion you think is the original one.",
        'it': "🔢 Seleziona il numero associato al completamento che ritieni essere quello originale."
    },
    'SYNONYM': {
        'en': "🔢 *Choice selection*: please select the number associated to one of the other answers you think is correct, or select NONE if there is no correct answer. You cannot vote for your own answer.",
        'it': "🔢 *Selezione*: seleziona il numero associato a una delle altre risposte che ritieni essere corretta, o scegli NESSUNA se non ce n'è nessuna di corretta. Non puoi votare per la tua risposta."
    }    
}

MSG_NEXT_ROUND = {
    'en': "⭕️🚦 Please press the button below when you are ready for the next round.",
    'it': "⭕️🚦 Premi il pulsante qua sotto quando sei pronto/a alla prossima mano."
}
MSG_TEACHER_ORIGINAL_TEXT = {
    'en': "🧑‍🏫 This is the original sentence:\n{}",
    'it': "🧑‍🏫 Queta è la frase originale:\n{}"
}
MSG_OR_NONE = {
    'en': ' (or NONE)',
    'it': ' (o NESSUNA)'
}
MSG_TEACHER_SELECT = {
    'en': "🧑‍🏫 Please *select a correct response*{}.",
    'it': "🧑‍🏫 Seleziona una risposta corretta*{}."
}
MSG_RECAP_STUDENTS_ANSWERS = {
    'en': "🧑‍🏫 These are the student's answers:",
    'it': "🧑‍🏫 Queste sono le risposte degli studenti:"
}
MSG_TEACHER_YOU_SELECTED = {
    'en': "⭐ You have selected {}.",
    'it': "⭐ Hai selezionato {}."
}
MSG_TEACHER_SELECT_OR_SUBMIT = {
    'en': "🧑‍🏫 Please select another correct response{} or press *{}* to confirm.".format('{}',BUTTON_SUBMIT['en']),
    'it': "🧑‍🏫 Seleziona un'altra risposta corretta{} o premi *{}* per confermare.".format('{}',BUTTON_SUBMIT['it'])
}
MSG_RECAP_INSTRUCTION = {
    'en': "📜 Use the command /recap\\_answers if you want to see the students' answers again.",
    'it': "📜 Usa il comando /recap\\_answers se vuoi vedere nuovamente le risposte degli studenti."
}
MSG_POINT_SG_PL = lambda x: \
    {
        'en': "{} point".format(x),
        'it': '{} punto'.format(x),        
    } \
    if abs(x) == 1 else \
    {
        'en': "{} points".format(x),
        'it': '{} punti'.format(x),        
    }

MSG_CORRECT_ANSWER= {
    'en': '🌟✍ You have answered correctly! ({})',
    'it': '🌟✍ Hai risposto correttamente! ({})'
}
MSG_NO_GIVEN_ANSWER= {
    'en': "🤷‍♀️✍ You didn't provide an answer ({}).",
    'it': '🤷‍♀️✍ Non hai dato una risposta ({}).',
}
MSG_WRONG_ANSWER= {
    'en': "❌✍ You didn't give the correct answer ({}).",
    'it': '❌✍ Non hai dato la risposta corretta ({}).',
}
MSG_CORRECT_SELECTION= {
    'en': '🌟📌 You have chosen correctly! ({})',
    'it': '🌟📌 Hai scelto correttamete! ({})'
}
MSG_WRONG_SELECTION_NO_PENALTY= {
    'en': "❌📌 You didn't choose correctly.",
    'it': '❌📌 Non hai scelto correttamente.'
}
MSG_NO_GIVEN_SELECTION= {
    'en': "🤷‍♀️📌 You didn't make a selection. ({})",
    'it': '🤷‍♀️📌 Non hai fatto una scelta. ({})'
}
MSG_WRONG_SELECTION_PENALTY= {
    'en': "❌📌 You didn't choose correctly ({}).",
    'it': '❌📌 Non hai scelto correttamente ({}).'
}
MSG_RECEIVED_VOTES = {
    'en': "🔘 {} players chosen your answer ({}).",
    'it': "🔘 {} giocatori hanno scelto la tua risposta ({})."
}

MSG_NO_SELECTION_ONLY_ONE_OPTION = {
    'en': "❌🔘 No selection: some player would only have one option to choose from.",
    'it': "❌🔘 Nessuna selezione: alcuni giocatori avrebbero solo una sola opzione da scegliere."
}
MSG_NO_SELECTION_ALL_GUESSED_CORRECTLY = {
    'en': "❌🔘 No selection: all player inserted the correct answer.",
    'it': "❌🔘 Nessuna selezione: tutti i giocatori hanno inserito la soluzione corretta."
}
MSG_NO_ANSWER_GOING_TO_NEXT_ROUND = {
    'en': "🦘 No answer received, we go to next round.",
    'it': "🦘 Nessuna risposta ricevuta, si passa alla prossima mano."
}
MSG_CORRECT_ANSWER_NO_SELECTION = {
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
MSG_THANKS_YOU_ENTERED_X = {
    'en': "😀 Thanks, you entered *{}*.",
    'it': "😀 Grazie, hai inserito *{}*."
}
MSG_THANKS_YOU_SELECTED_X = {
    'en': "😀 Thanks, you selected *{}*.",
    'it': "😀 Grazie, hai selezionato *{}*."
}
MSG_WAIT_TILL_YOUR_TURN = {
    'en': "💤 We will get back as soon as it is your turn again.",
    'it': "💤 Verrai informato quando sarà nuovamente il tuo turno."
}
MSG_STATUS_INSTRUCTIONS = {
    'en': "👀 If you want to see who we are still waiting for use the command /status",
    'it': "👀 Se vuoi sapre chi stiamo aspettando, usa il comando /status!"
}
MSG_WAIT_FOR_TEACHER_EVALUATION = {
    'en': "🧑‍🏫 Let's wait for the teacher's evaluation!",
    'it': "🧑‍🏫 Aspettiamo la valutazione dell'insegnante!"
}
MSG_ALREADY_SELECTED_WAITING_FOR = {
    'en': "🤐 You already made your choice!\n😴 Let's wait for: {}",
    'it': "🤐 Hai già fatto la tua scelta!\n😴 Rimani in attesa di: {}"
}
MSG_X_SELECTED = {
    'en': "✔️ {} has chosen.",
    'it': "✔️ {} ha fatto la sua scelta."
}
MSG_WAIT_FOR = {
    'en': "😴 Let's wait for: {}",
    'it': "😴 Rimaniamo in attesa di: {}"
}
MSG_ANSWERS_RECAP_SG = {
    'en': "📜 Answers recap: correct answer is marked with a ⭐️",
    'it': "📜 Sintesi risposte: la risposta corretta è segnata con una ⭐️"
}
MSG_ANSWERS_RECAP_PL = {
    'en': "📜 Answers recap: correct answers are marked with a ⭐️",
    'it': "📜 Sintesi risposte: le risposte corrette sono segnate con una ⭐️"
}
MSG_YOUR_POINTS = {
    'en': "💰 Your points:",
    'it': "💰 I tuoi punti:"
}
MSG_SELECTED_BY = {
    'en': "Chosen by {}",
    'it': "Scelto da {}"
}
MSG_NO_ANSWER = {
    'en': "NONE",
    'it': "NESSUNA"
}
MSG_WRITTEN_BY = {
    'en': "Written by: {}",
    'it': "Scritto da: {}"
}
MSG_POINT_ROUND_SUMMARY = {
    'en': "⭕️ ROUND {} POINTS",
    'it': "🖐 PUNTI MANO {}"
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
    'en': "🚪 Game has terminated because {} has quit the game.",
    'it': "🚪 Gioco terminato perché {} ha interrotto il gioco."
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
MSG_ERROR_CHAT_INFO = {
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
    'en': "🏆 The winner of the game is {}",
    'it': "🏆 Il/a vincitore/trice del gioco è {}"
}
MSG_WINNER_PLURAL = {
    'en': "🏆 The winners of the game are {}",
    'it': "🏆 I/le vincitori/trici del gioco sono {}"
}

MSG_WRONG_INPUT_ONLY_TEXT_ACCEPTED = {
    'en': "⛔️ Wrong input, only text is accepted here.",
    'it': "⛔️ Input non valido, devi inserire solo del testo."
}
MSG_WRONG_INPUT_WAIT_FOR_PLAYERS_TO_ANSWER = {
    'en': "⛔️ Let's wait for the other players to provide their answers.",
    'it': "⛔️ Attendiamo che le altre persone scrivano la loro risposta."
}
MSG_WRONG_INPUT_WAIT_FOR_PLAYERS_TO_SELECT = {
    'en': "⛔️ Let's wait for the other players to make their choice.",
    'it': "⛔️ Attendiamo che le altre persone facciano la loro scelta."
}
MSG_WRONG_INPUT_WAIT_FOR_X_TO_START_NEXT_ROUND = {
    'en': "⛔️ Let's wait for {} to proceed to next round.",
    'it': "⛔️ Attendiamo che {} avvii la prossima mano."
}
MSG_WRONG_INPUT_WAIT_FOR_TEACHER_TO_SELECT = {
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
    'en': '⛔️ Input cannot contain the following characters: {}'.format(utility.escape_markdown(utility.MARKDOWN_CHARS)),
    'it': '⛔️ Il testo non può contenere i caratteri: {}'.format(utility.escape_markdown(utility.MARKDOWN_CHARS))
}
MSG_CHAT_MSG_NO_MARKDOWN = {
    'en': '⛔️ The chat message cannot contain the following characters: {}'.format(utility.escape_markdown(utility.MARKDOWN_CHARS)),
    'it': '⛔️ Il testo del messaggio non può contenere i caratteri: {}'.format(utility.escape_markdown(utility.MARKDOWN_CHARS))
}
MSG_INPUT_NO_GAP = {
    'en': '⛔️ The text you have inserted does not contain the sequence of 3 question marks (\'???\') to indicate the missing part to be completed.',
    'it': '⛔️ Il testo inserito non contiene la sequenza di 3 punti di domanda (\'???\') per indicare la parte mancante da completare.'
}
MSG_INPUT_NO_SYNONYM = {
    'en': '⛔️ The text you have inserted does not contain parenthesis or they are not in the correct format.',
    'it': '⛔️ Il testo inserito non contiene le parentsi in formato corretto.'
}
MSG_INPUT_SUBSTITUION_NOT_IN_SENTENCE = {
    'en': '⛔️ The string you have inserted is not present in the original sentence, try again.',
    'it': '⛔️ Il testo inserito non è presente nella frase inserita precedentemente, prova di nuovo.'
}
MSG_INPUT_SUBSTITUION_PRESENT_TWICE_OR_MORE_IN_SENTENCE = {
    'en': '⛔️ The string you have inserted is present more than once in the sentence, please try again.',
    'it': '⛔️ Il testo inserito è presente nella frase più di una volta, prova di nuovo.'
}
MSG_INPUT_NO_VALID_SYNONYM = {
    'en': '⛔️ The text you have inserted is identical to the one boldfaced, try again.',
    'it': '⛔️ Il testo inserito è identico a quello in grassetto, riprova di nuovo.'
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
        'SYNONYM': BUTTON_GAME_TYPE_SYNONYM[lang],
    },
    BUTTON_GAME_CONTROL[lang]: {
        'DEFAULT': BUTTON_GAME_CONTROL_DEFAULT[lang],
        'TEACHER': BUTTON_GAME_CONTROL_TEACHER[lang]
    },
    BUTTON_GAME_TRANSLATE_HELP[lang]: {
        True: BUTTON_YES[lang],
        False: BUTTON_NO[lang]
    }
}

def render_complete_text(game, answer):
    incomplete_text = game.get_current_incomplete_text()    
    if game.game_type == 'CONTINUATION':        
        completed_text = "{} *{}*".format(incomplete_text, answer)
    elif game.game_type == 'FILL':        
        pre_gap, post_gap = game.get_incomplete_text_pre_post_gap()
        completed_text = '{}*{}*{}'.format(pre_gap, answer, post_gap)
    else:
        assert game.game_type == 'SYNONYM'
        original_answer = game.get_current_completion_text()
        completed_text = incomplete_text.replace(original_answer, '*{}*'.format(answer))
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