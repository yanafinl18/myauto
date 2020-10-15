from data.endpoints import akbars_online_auth_login_init, akbars_online_auth_login_confirm, auth_create_session
from data.users import protas
from models.http import parametrized_post
from data.external_variables import default_device_token


def get_auth(session):
    data = {'Login': protas['Login'], 'Password': protas['Password']}
    r = parametrized_post(endpoint=akbars_online_auth_login_init, body_payload=data)
    session['AkbarsLoginOperationId'] = r.json()['Result']['AkbarsLoginOperationId']


def confirm_auth(session):
    data = {"AkbarsOnlineLoginOperationId": session['AkbarsLoginOperationId'],
            "DeviceToken": "2a9f3045-ef42-49ac-b538-c80eb7b5dabc"}
    r = parametrized_post(endpoint=akbars_online_auth_login_confirm, body_payload=data)
    session['RefreshToken'] = r.json()['Result']['RefreshToken']


def get_token(session):
    data = {"DeviceToken": default_device_token, "GeoLocation": {}, "RefreshToken": session['RefreshToken']}
    r = parametrized_post(endpoint=auth_create_session, body_payload=data)
    session['SessionToken'] = r.json()['Result']['SessionToken']
    print('SessionToken: ', session['SessionToken'])

