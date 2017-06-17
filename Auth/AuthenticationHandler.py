#############################
# Data collector for CartolaFC
#
# Developed by Eric Baum
#
# Copyright, 2017 - Eric Baum
#############################

import requests
from pathlib import Path
from requests import HTTPError

GLOBO_LOGIN_URL = 'https://login.globo.com/api/authentication'
VALIDOR_URL = 'https://api.cartolafc.globo.com/auth/time'
TOKEN_FILE_NAME = './token_tmp'


class AuthenticationHandler:
    """
    Class responsible for handling the authentication to globo.com
    """

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def get_token(self):
        glb_token = ""

        token_file = Path(TOKEN_FILE_NAME)

        try:
            # Check if token file exists
            token_file.resolve()
            with token_file.open('r') as file:
                glb_token = file.readline()
                file.close()
            # Test token validity
            self._test_token(glb_token)
        except FileNotFoundError or RuntimeError or HTTPError:
            glb_token = self._authenticate()
            with token_file.open('w') as file:
                file.write(glb_token)
                file.close()
        finally:
            return glb_token

    @staticmethod
    def _test_token(token):
        header = {'X-GLB-Token': token}
        resp = requests.get(url=VALIDOR_URL, headers=header)
        resp.raise_for_status()
        print("O token ainda é válido!")

    def _authenticate(self):
        url = GLOBO_LOGIN_URL
        body = {
            'payload': {
                'email': self.email,
                'password': self.password,
                'serviceId': 438
            },
            'captcha': ""
        }

        try:
            resp = requests.post(url=url, json=body)
            resp.raise_for_status()
        except HTTPError as e:
            print(e.response)
            print(e.args)
            return ""

        glb_token = resp.json().get('glbId')
        print("Usuário %s autenticado com sucesso" % self.email)

        return glb_token
