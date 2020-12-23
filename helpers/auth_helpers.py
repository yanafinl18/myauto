from data.endpoints import akbars_online_auth_login_init, akbars_online_auth_login_confirm, auth_create_session, akbars_online_send_otp, get_otp_code
from models.http import parametrized_post, parametrized_get
from data.external_variables import default_device_token
from data.users import protas
from bs4 import BeautifulSoup
import requests
import re


class Session:
    """ Класс создания сессии.

    Attributes
    ----------
    - current_user (пользователь на котором идут тесты)

    Methods
    -------
    - create_session  (создание сессии)
    - get_auth (логин)
    - send_otp (отправка отп кода)
    - get_otp (получение отп кода)
    - confirm_auth (подтверждения логина)
    - get_token (получение SessionToken)
    - logout (удаление SessionToken)

    На выходе получаем SessionToken для авторизации """

    def __init__(self, current_user):
        self.current_user = current_user
        self.last_auth_time = None
        self.session_key = None
        self.session = {
            'DeviceToken': default_device_token
        }


    def create_session(self):
        """ Получение SessionToken, последовательным вызовом методом"""

        self.get_auth()
        self.confirm_auth()
        self.get_token()
        return self.session_key


    def get_auth(self):
        """ Получение AkbarsLoginOperationId для использования в методе send_otp.

        Parameters
        ----------
         - login
         - password

         Если параметр NeedOtp пришел true в ответе, то вызываем последотвательно методы send_otp и get_otp.
         Параметр AkbarsLoginOperationId из ответа записываем в словарь session """

        data = {'Login': self.current_user['Login'], 'Password': self.current_user['Password']}
        r = parametrized_post(endpoint=akbars_online_auth_login_init, body_payload=data)
        self.session['AkbarsLoginOperationId'] = r.json()['Result']['AkbarsLoginOperationId']
        self.session['NeedOtp'] = r.json()['Result']['NeedOtp']
        if self.session['NeedOtp'] == True:
            self.send_otp()
            self.get_otp()


    def send_otp(self):
        """ Отправка кода OTP, тут же проверка что у клиента есть номер телефона.

        Parameters
        ----------
        - AkbarsOnlineLoginOperationId, который равен  AkbarsLoginOperationId из get_auth"""

        data = {'AkbarsOnlineLoginOperationId': self.session['AkbarsLoginOperationId']}
        r = parametrized_post(endpoint=akbars_online_send_otp, body_payload=data)
        assert r.json()['Result']['Phone'] is not None, "Otp don't send"


    def get_otp(self):
        """ Получение кода OTP для логина.

        Parameters
        ----------
        - AkbarsLoginOperationId

        Записываем OTP код в словарь session"""

        data = {'operationToken': 'IdentityAbo:'+self.session['AkbarsLoginOperationId']}
        r = parametrized_get(endpoint=get_otp_code, url_payload=data)
        assert r.json()['code'] is not None, "Otp code don't exist"
        self.session['OtpCode'] = r.json()['code']


    def confirm_auth(self):
        """ Подтверждение логина.

        Parameters
        ----------
        - DeviceToken
        - AkbarsOnlineLoginOperationId
        - OtpCode (если NeedOtp равен true).

        В ответе получили RefreshToken."""

        if self.session['NeedOtp'] == True:
            data = {"AkbarsOnlineLoginOperationId": self.session['AkbarsLoginOperationId'],
                    "DeviceToken": self.session['DeviceToken'], "OtpCode": self.session['OtpCode']}
        else:
            data = {"AkbarsOnlineLoginOperationId": self.session['AkbarsLoginOperationId'],
                    "DeviceToken": self.session['DeviceToken']}
        r = parametrized_post(endpoint=akbars_online_auth_login_confirm, body_payload=data)
        self.session['RefreshToken'] = r.json()['Result']['RefreshToken']


    def get_token(self):
        """ Получение SessionToken.

        Parameters
        ----------
        - DeviceToken
        - RefreshToken

        В ответе получаем заветный SessionToken"""

        data = {"DeviceToken": self.session['DeviceToken'], "GeoLocation": {}, "RefreshToken": self.session['RefreshToken']}
        r = parametrized_post(endpoint=auth_create_session, body_payload=data)
        self.session_key = r.json()['Result']['SessionToken']


    def get_otp_from_web(self):
        """ попытка получения otp кода  с веб страницы"""

        r = requests.get("https://testbankok.akbars.ru/6f1f60ba")
        html = r.content  # чтение и сохранение
        soup = BeautifulSoup(html, "html.parser")  # парсер
        otp = soup.find("table", id="Confirms")
        otp2 = otp.select("tr:nth-child(1)> td.col-md-8 > div > span")
        print(otp2[0])
        reg = re.findall('[0-9]+', str(otp2[0]))  # выборка цифр
        print("OTPCode: ", reg)
        self.session['OtpCode'] = reg


    def logout(self):
        """ Разлогин пользователя. Обнуление записи SessionToken в словаре session.
        Возвращаем значение пустого SessionToken """

        self.session_key = None
        return self.session_key


