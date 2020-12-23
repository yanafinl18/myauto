from data.endpoints import cardordering_cities
from models.http import parametrized_get
from pytest_testrail.plugin import pytestrail



@pytestrail.case('C1060115')
def test_get_cardordering_cities(session):
    r = parametrized_get(endpoint=cardordering_cities, header_payload={'SessionToken': session.session_key})
    result = r.json()['Result']['Localities'][0]['DeliveryIsAvailable']
    assert isinstance(result, bool)
    result =  r.json()['Result']['Localities'][0]['CardIssueIsAvailable']
    assert isinstance(result, bool)
    assert r.json()['Result']['Localities'][0]['Name']
    assert r.json()['Success'] == True