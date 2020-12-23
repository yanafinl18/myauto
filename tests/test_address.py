from data.endpoints import find_address
from data.data_address import address_1
from models.http import parametrized_post
from data.external_variables import default_user_agent
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C2622159')
def test_get_address(session):
    r = parametrized_post(endpoint=find_address, body_payload=address_1, header_payload={'SessionToken': session.session_key,
                                                               'Content-Type': 'application/json; charset=utf-8',
                                                               'User-Agent': default_user_agent
                                                               })
    assert r.json()['Result'][0]['StreetFias'] == "63b26927-9a86-4b80-bba9-02b37135c686", "Request of address isn't pass or fias is changed "
    assert r.json()['Result'][0]['House'] == "11", "Incorrect house number"
    assert r.json()['Result'][0]['Value'] == "г Казань, ул Чистопольская, д 11", "Incorrect address"
    assert r.json()['Result'][0]['Granularity'] == 8, "Incorrect granularity (completeness of address)"


