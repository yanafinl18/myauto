from data.endpoints import notifications_settings
from models.http import parametrized_get, parametrized_post
from data.external_variables import default_user_agent
from pytest_testrail.plugin import pytestrail



@pytestrail.case('C977575')
def test_get_notification_settings(session):
    r = parametrized_get(endpoint=notifications_settings, header_payload={'SessionToken': session.session_key})
    result = r.json()['Result']['SendOperationsCodesWithPush']
    assert isinstance(result, bool), "Incorrect value: must be True or False"
    result = r.json()['Result']['SendMarketingNotificationsWithPush']
    assert isinstance(result, bool), "Incorrect value: must be True or False"
    result = r.json()['Result']['SendCardOperationsWithPush']
    assert isinstance(result, bool), "Incorrect value: must be True or False"


@pytestrail.case('C977576')
def test_set_notification_settings(session):
    header_payload = {'SessionToken': session.session_key,
                      'Content-Type': 'application/json; charset=utf-8',
                      'User-Agent': default_user_agent
                      }
    body_payload = {'SendOperationsCodesWithPush': True,
                    'SendMarketingNotificationWithPush': True,
                    'SendCardOperationsWithPush': True
                    }
    r = parametrized_post(endpoint=notifications_settings, body_payload=body_payload, header_payload=header_payload)
    assert r.json()['Success'] == True, "Notification method didn't change"
