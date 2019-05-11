import requests

def get_ngrok_base():
    import requests
    r = requests.get('http://localhost:4040/api/tunnels')
    remote_base = r.json()['tunnels'][0]['public_url'] # 'http://xxxxxx.ngrok.io'
    return remote_base
