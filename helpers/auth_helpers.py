from data.endpoints import akbars_online_auth_login_init, akbars_online_auth_login_confirm, auth_create_session, akbars_online_send_otp, get_otp_code
from models.http import parametrized_post, parametrized_get
from data.external_variables import default_device_token
from data.users import protas
from bs4 import BeautifulSoup
import requests
import re


class Session:
    def __init__(self, current_user):
        self.current_user = current_user
        self.last_auth_time = None
        self.session_key = None
        self.session = {
            'DeviceToken': default_device_token
        }

    def create_session(self):
        self.get_auth()
        self.confirm_auth()
        self.get_token()
        return self.session_key



    def get_auth(self):
        data = {'Login': self.current_user['Login'], 'Password': self.current_user['Password']}
        r = parametrized_post(endpoint=akbars_online_auth_login_init, body_payload=data)
        self.session['AkbarsLoginOperationId'] = r.json()['Result']['AkbarsLoginOperationId']
        self.session['NeedOtp'] = r.json()['Result']['NeedOtp']
        if self.session['NeedOtp'] == True:
            send_otp(self.session)
            get_otp(self.session)



    def send_otp(self):
        data = {'AkbarsOnlineLoginOperationId': self.session['AkbarsLoginOperationId']}
        r = parametrized_post(endpoint=akbars_online_send_otp, body_payload=data)
        assert r.json()['Result']['Phone'] is not None, "Otp don't send"


    def get_otp(self):
        data = {'operationToken': 'IdentityAbo:'+self.session['AkbarsLoginOperationId']}
        r = parametrized_get(endpoint=get_otp_code, url_payload=data)
        assert r.json()['code'] is not None, "Otp code don't exist"
        self.session['OtpCode'] = r.json()['code']



    def confirm_auth(self):
        if self.session['NeedOtp'] == True:
            data = {"AkbarsOnlineLoginOperationId": self.session['AkbarsLoginOperationId'],
                    "DeviceToken": self.session['DeviceToken'], "OtpCode": self.session['OtpCode']}
        else:
            data = {"AkbarsOnlineLoginOperationId": self.session['AkbarsLoginOperationId'],
                    "DeviceToken": self.session['DeviceToken']}
        r = parametrized_post(endpoint=akbars_online_auth_login_confirm, body_payload=data)
        self.session['RefreshToken'] = r.json()['Result']['RefreshToken']


    def get_token(self):
        data = {"DeviceToken": self.session['DeviceToken'], "GeoLocation": {}, "RefreshToken": self.session['RefreshToken']}
        r = parametrized_post(endpoint=auth_create_session, body_payload=data)
        self.session_key = r.json()['Result']['SessionToken']


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
        self.session['OtpCode'] = reg

    def logout(self):
        self.session_key = None
        return self.session_key





session = Session(protas)
print(session.current_user) # Напечатает protas
print(session.session_key) # Напечатает созданную сессию
session.create_session()
print(session.session_key) # вернет новое значение ключа
session.logout() # обнуление ключа
print(session.session_key)
