import requests
from data.endpoints import find_address
from data.data_address import address_1
from helpers.auth_helpers import get_auth, confirm_auth, get_token
from config import host


session = {}

get_auth(session)
confirm_auth(session)
get_token(session)

def test_get_address():
    data = address_1
    # Когда передаешь json нельзя просто использовать data=data, где data это словарь.
    r = requests.post(host + find_address, json=data, headers={'SessionToken': session['SessionToken'],
                                                               'Content-Type': 'application/json; charset=utf-8',
                                                               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 OPR/71.0.3770.138 (Edition Yx GX)'
                                                               })
    assert r.status_code == 200
    assert r.json()['Result'][0]['StreetFias'] == "63b26927-9a86-4b80-bba9-02b37135c686", "Запрос на получение адреса не прошел или fias сменился "
    assert r.json()['Result'][0]['House'] == "11"
    assert r.json()['Result'][0]['Value'] == "г Казань, ул Чистопольская, д 11"
    assert r.json()['Result'][0]['Granularity'] == 8


