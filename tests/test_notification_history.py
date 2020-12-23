from data.endpoints import notificationhistory, notificationhistory_hasunread, notificationhistory_viewed, notifications_history
from models.http import parametrized_get, parametrized_post
from data.external_variables import default_user_agent
from pytest_testrail.plugin import pytestrail



@pytestrail.case('C969930')
def test_get_notificationhistory_hasunread(session):
    r = parametrized_get(endpoint=notificationhistory_hasunread, header_payload={'SessionToken': session.session_key})
    result = r.json()['Result']['HasUnread']
    assert isinstance(result, bool), "Incorrect answear: must be True or False"


@pytestrail.case('C969932')
def test_get_notificationhistory(session):
    url_payload = {'limit': '20'}
    r = parametrized_get(endpoint=notificationhistory, url_payload=url_payload, header_payload={'SessionToken': session.session_key})
    assert r.json()['Success'] == True


@pytestrail.case('C969931')
def test_set_notificationhistory_viewed(session):
    header_payload = {'SessionToken': session.session_key,
                      'Content-Type': 'application/json; charset=utf-8',
                      'User-Agent': default_user_agent
                      }
    r = parametrized_post(endpoint=notificationhistory_viewed, header_payload=header_payload)
    assert r.json()['Success'] == True, "Notification msg didn't change"


@pytestrail.case('C2622551')
def test_get_notificationhistory_login(session):
    url_payload = {'limit': '20'}
    r = parametrized_get(endpoint=notifications_history, url_payload=url_payload, header_payload={'SessionToken': session.session_key})
    assert r.json()['NextPage'] is not None
    assert r.json()['Result'][0]['Id'] is not None
    assert r.json()['Result'][0]['CreatedOn'] is not None