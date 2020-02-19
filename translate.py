import requests
import key

GOOGLE_API_ENDPOINT = 'https://translation.googleapis.com/language/translate/v2'
YANDEX_API_ENDPOINT = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

def get_google_translation(text, source_lang='it', target_lang='en'):
    querystring = {
        "q": text,        
        "source": source_lang,
        "target": target_lang, # https://cloud.google.com/translate/docs/languages?hl=it
        "key": key.GOOGLE_API_KEY,        
    }    
    r = requests.request("POST", GOOGLE_API_ENDPOINT, params=querystring)
    if r.status_code == 200:
        return r.json()['data']['translations'][0]['translatedText']
    return None

def get_yandex_translation(text, source_lang='it', target_lang='en'):
    querystring = {
        "key": key.YANDEX_API_KEY,
        "text": text,
        "lang": "{}-{}".format(source_lang, target_lang),
    }

    r = requests.request("GET", YANDEX_API_ENDPOINT, params=querystring)

    if r.status_code == 200:
        return r.json()['text'][0]
    return None

def get_google_back_translation(text, source_lang='it', pivot_lang='en'):
    translation = get_google_translation(text, source_lang, pivot_lang)
    back_translation = get_google_translation(translation, pivot_lang, source_lang)
    return back_translation

def get_yandex_back_translation(text, source_lang='it', pivot_lang='en'):
    translation = get_yandex_translation(text, source_lang, pivot_lang)
    back_translation = get_yandex_translation(translation, pivot_lang, source_lang)
    return back_translation


if __name__ == "__main__":
    # print(get_yandex_translation("Come stai?"))
    # print(get_google_translation("Come stai?"))
    print(
        get_yandex_back_translation(
            "He just held on to me, his fingers strong against my left arm.",
            'en',
            'it'
        )
    )