from data.endpoints import analytics_info
from models.http import parametrized_get

def test_get_analytics_info(session):
    r = parametrized_get(endpoint=analytics_info, header_payload={'SessionToken': session.session_key})
    assert r.json()['Result']['Identifier'] is not None
    assert r.json()['Result']['CustomerImportance'] is not None

