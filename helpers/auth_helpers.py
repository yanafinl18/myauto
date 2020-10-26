from data.endpoints import akbars_online_auth_login_init, akbars_online_auth_login_confirm, auth_create_session, akbars_online_send_otp, get_otp_code
from data.users import protas, reimond
from models.http import parametrized_post, parametrized_get
from data.external_variables import default_device_token
from bs4 import BeautifulSoup
import requests
import re

class Session():
    def __init__(self, current_user, last_auth_time, session_key, session{}):
        self.current_user = current_user
        self.last_auth_time = last_auth_time
        self.session = session{}
        self.session_key = session_key



    def CreateSession(self):
        session["user"] = protas
        get_auth(self.session)
        confirm_auth(self.session)
        get_token(self.session)


    def get_auth(self):
        data = {'Login': self.current_user['Login'], 'Password': self.current_user['Password']}
        r = parametrized_post(endpoint=akbars_online_auth_login_init, body_payload=data)
        session['AkbarsLoginOperationId'] = r.json()['Result']['AkbarsLoginOperationId']
        session['NeedOtp'] = r.json()['Result']['NeedOtp']
        if session['NeedOtp'] == True:
            send_otp(session)
            get_otp(session)


    def send_otp(self):
        data = {'AkbarsOnlineLoginOperationId': session['AkbarsLoginOperationId']}
        r = parametrized_post(endpoint=akbars_online_send_otp, body_payload=data)
        assert r.json()['Result']['Phone'] is not None, "Otp don't send"


    def get_otp(self):
        data = {'operationToken': 'IdentityAbo:'+session['AkbarsLoginOperationId']}
        r = parametrized_get(endpoint=get_otp_code, url_payload=data)
        assert r.json()['code'] is not None, "Otp code don't exist"
        session['OtpCode'] = r.json()['code']




# попытка получения otp с веб страницы
    def get_otp_from_web(self):
        r = requests.get("https://testbankok.akbars.ru/6f1f60ba")
        html = r.content # чтение и сохранение
        soup = BeautifulSoup(html, "html.parser") # парсер
        otp = soup.find("table", id="Confirms")
        otp2 = otp.select("tr:nth-child(1)> td.col-md-8 > div > span")
        print(otp2[0])
        reg = re.findall('[0-9]+', str(otp2[0]))  # выборка цифр
        print("OTPCode: ", reg)
        session['OtpCode'] = reg



    def confirm_auth(self):
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







