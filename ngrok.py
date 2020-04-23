import requests

def get_ngrok_base():
    import requests
    r = requests.get('http://localhost:4040/api/tunnels')
    json_data = r.json()
    for t in json_data['tunnels']:
        url = t['public_url']
        if url.startswith('https'):
            return url
    return None
