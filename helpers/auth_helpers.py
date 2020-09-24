import requests
from data.endpoints import akbars_online_auth_login_init, akbars_online_auth_login_confirm, auth_create_session
from data.users import protas

host = 'http://testbankok.akbars.ru/'


def auth():
    data = {'Login': protas['Login'], 'Password': protas['Password']}
    r = requests.post(host+akbars_online_auth_login_init, data = data )
    assert r.status_code == 200
    global AkbarsLoginOperationId
    AkbarsLoginOperationId = r.json()['Result']['AkbarsLoginOperationId']
    print('AkbarsLoginOperationId: ', AkbarsLoginOperationId)

def confirm():
    data = {"AkbarsOnlineLoginOperationId": AkbarsLoginOperationId,"DeviceToken":"2a9f3045-ef42-49ac-b538-c80eb7b5dabc"}
    r = requests.post(host + akbars_online_auth_login_confirm, data=data)
    global RefreshToken
    RefreshToken = r.json()['Result']['RefreshToken']
    print('RefreshToken: ', RefreshToken)

def sessiontoken():
    data = {"DeviceToken":"2a9f3045-ef42-49ac-b538-c80eb7b5dabc","GeoLocation":{},"RefreshToken": RefreshToken}
    r = requests.post(host + auth_create_session, data=data)
    SessionToken =r.json()['Result']['SessionToken']
    print('SessionToken: ', SessionToken)


auth()
confirm()
sessiontoken()