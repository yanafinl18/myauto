import requests
from data.endpoints import akbars_online_auth_login_init, akbars_online_auth_login_confirm, auth_create_session
from data.users import protas
from config import host

session = {
    'AkbarsLoginOperationId': None,
    'RefreshToken': None,
    'SessionToken': None
}

def get_auth(session):
    data = {'Login': protas['Login'], 'Password': protas['Password']}
    r = requests.post(host + akbars_online_auth_login_init, data=data)
    assert r.status_code == 200
    session['AkbarsLoginOperationId'] = r.json()['Result']['AkbarsLoginOperationId']


def confirm_auth(session):
    data = {"AkbarsOnlineLoginOperationId": session['AkbarsLoginOperationId'],
            "DeviceToken": "2a9f3045-ef42-49ac-b538-c80eb7b5dabc"}
    r = requests.post(host + akbars_online_auth_login_confirm, data=data)
    session['RefreshToken'] = r.json()['Result']['RefreshToken']


def get_token(session):
    data = {"DeviceToken": "2a9f3045-ef42-49ac-b538-c80eb7b5dabc", "GeoLocation": {}, "RefreshToken": session['RefreshToken']}
    r = requests.post(host + auth_create_session, data=data)
    session['SessionToken'] = r.json()['Result']['SessionToken']
    print('SessionToken: ', session['SessionToken'])


get_auth(session)
confirm_auth(session)
get_token(session)