from data.endpoints import analytics_info
from models.http import parametrized_get
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C2622168')
def test_get_analytics_info(session):
    r = parametrized_get(endpoint=analytics_info, header_payload={'SessionToken': session.session_key})
    assert r.json()['Result']['Identifier'] is not None, "User has not CRM id"
    assert r.json()['Result']['CustomerImportance'] is not None, "User has not customerImportance"

