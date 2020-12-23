from data.endpoints import banks_bin
from models.http import parametrized_get
from pytest_testrail.plugin import pytestrail
import pytest

@pytestrail.case('C274995')
@pytest.mark.xfail
def test_get_banks_bin(session):
    r = parametrized_get(endpoint=banks_bin, header_payload={'SessionToken': session.session_key})
    assert r.json()['Result']['Bin'] == '557030', "Incorrect bin"
    assert r.json()['Result']['Name'] == 'Зенит', "Incorrect name"

