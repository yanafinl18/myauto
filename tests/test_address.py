from data.endpoints import find_address
from data.data_address import address_1
#from helpers.auth_helpers import get_auth, confirm_auth, get_token
from helpers.auth_helpers import Session
from models.http import parametrized_post
from data.external_variables import default_user_agent
from data.users import protas



session = Session(protas)

def test_get_address(self, session):


    r = parametrized_post(endpoint=find_address, body_payload=address_1, header_payload={'SessionToken': session.session_key,
                                                               'Content-Type': 'application/json; charset=utf-8',
                                                               'User-Agent': default_user_agent
                                                               })

    assert r.json()['Result'][0]['StreetFias'] == "63b26927-9a86-4b80-bba9-02b37135c686", "Запрос на получение адреса не прошел или fias сменился "
    assert r.json()['Result'][0]['House'] == "11", "Некорректный номер дома"
    assert r.json()['Result'][0]['Value'] == "г Казань, ул Чистопольская, д 11"
    assert r.json()['Result'][0]['Granularity'] == 8, "Некорректная гранулярность (полнота адреса)"


