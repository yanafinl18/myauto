import requests
from data.endpoints import find_address
from helpers.auth_helpers import get_auth, confirm_auth, get_token
from config import host


get_auth()
confirm_auth()
get_token()

def get_address():  # как в request передать sessionToken
    data = {'SearchTerm': 'г Казань ул Чистопольская 11', 'MaxCount': 5}
    r = requests.post(host + find_address, data=data, headers={'SessionToken': session['SessionToken']})
    assert r.status_code == 200
    assert r.json()['Result'][0]['StreetFias'] == "63b26927-9a86-4b80-bba9-02b37135c686", "Запрос на получение адреса не прошел или fias сменился "
    assert r.json()['Result'][0]['House'] == "11"
    assert r.json()['Result'][0]['Value'] == "г Казань, ул Чистопольская, д 11"
    assert r.json()['Result'][0]['Granularity'] == 8


get_address()