from data.endpoints import deposit_rateinfo
from models.http import parametrized_get

def test_get_deposit_rate(session):
    r = parametrized_get(endpoint=deposit_rateinfo, header_payload={'SessionToken': session.session_key})
    assert r.json()['Result']['MaxPercentageRateText'] is not None
