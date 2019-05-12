import requests
import key

def get_google_translation(text, source_lang='it', target_lang='en'):
    url = 'https://translation.googleapis.com/language/translate/v2'
    querystring = {
        "q": text,        
        "source": source_lang,
        "target": target_lang, # https://cloud.google.com/translate/docs/languages?hl=it
        "key": key.GOOGLE_API_KEY,        
    }    
    r = requests.request("POST", url, params=querystring)
    if r.status_code == 200:
        return r.json()['data']['translations'][0]['translatedText']
    return None

def get_yandex_translation(text, source_lang='it', target_lang='en'):
    url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    querystring = {
        "key": key.YANDEX_API_KEY,
        "text": text,
        "lang": "{}-{}".format(source_lang, target_lang),
    }

    r = requests.request("GET", url, params=querystring)

    if r.status_code == 200:
        return r.json()['text'][0]
    return None

if __name__ == "__main__":
    # print(get_yandex_translation("Come stai?"))
    print(get_google_translation("Come stai?"))