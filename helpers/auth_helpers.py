from data.endpoints import akbars_online_auth_login_init, akbars_online_auth_login_confirm, auth_create_session, akbars_online_send_otp, get_otp_code
from data.users import reimond
from models.http import parametrized_post, parametrized_get
from data.external_variables import default_device_token
from bs4 import BeautifulSoup
import requests



def get_auth(session):
    data = {'Login': reimond['Login'], 'Password': reimond['Password']}
    r = parametrized_post(endpoint=akbars_online_auth_login_init, body_payload=data)
    session['AkbarsLoginOperationId'] = r.json()['Result']['AkbarsLoginOperationId']
    session['NeedOtp'] = r.json()['Result']['NeedOtp']
    if session['NeedOtp'] == True:
        send_otp(session)
        get_otp(session)

    print(session['AkbarsLoginOperationId'])#для отладки


def send_otp(session):
    data = {'AkbarsOnlineLoginOperationId': session['AkbarsLoginOperationId']}
    r = parametrized_post(endpoint=akbars_online_send_otp, body_payload=data)
    assert r.json()['Result']['Phone'] is not None, "Otp don't send"

    print("Phone: ",r.json()['Result']['Phone'])#для отладки

def get_otp(session):
    data = {'operationToken': 'IdentityAbo:'+session['AkbarsLoginOperationId']}
    r = parametrized_get(endpoint=get_otp_code, url_payload=data)
    assert r.json()['code'] is not None, "Otp code don't exist"
    session['OtpCode'] = r.json()['code']

    print("Code: ", r.json()['code'])

def get_otp_from_web():
    r = requests.get("https://testbankok.akbars.ru/6f1f60ba")
    html = r.content # чтение и сохранение
    soup = BeautifulSoup(html, "html.parser") # парсер
    otp = soup.find("table", id="Confirms")
    otp2 = otp.select("tr:nth-child(1)> td.col-md-8 > div > span")  #тут не пойму как выборку из таблицы сделать и я просто выбираю 1 элемент что заведемо неверно
    print(otp2)
    print(type(otp2)) # как у данного типа bs4.element.ResultSet   произвести выборку элементов,  чтобы выдрать код из полученного ответа



def confirm_auth(session):
    if session['NeedOtp'] == True:
        data = {"AkbarsOnlineLoginOperationId": session['AkbarsLoginOperationId'],
            "DeviceToken": default_device_token, "OtpCode": session['OtpCode']}
    else:
        data = {"AkbarsOnlineLoginOperationId": session['AkbarsLoginOperationId'],
                "DeviceToken": default_device_token}
    r = parametrized_post(endpoint=akbars_online_auth_login_confirm, body_payload=data)
    session['RefreshToken'] = r.json()['Result']['RefreshToken']

def get_token(session):
    data = {"DeviceToken": default_device_token, "GeoLocation": {}, "RefreshToken": session['RefreshToken']}
    r = parametrized_post(endpoint=auth_create_session, body_payload=data)
    session['SessionToken'] = r.json()['Result']['SessionToken']
    print('SessionToken: ', session['SessionToken'])

session = {}#для отладки

#get_auth(session)
#confirm_auth(session)
#get_token(session)
get_otp_from_web()
