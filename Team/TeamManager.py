#############################
# Data collector for CartolaFC
#
# Developed by Eric Baum
#
# Copyright, 2017 - Eric Baum
#############################

import requests
import pprint

TEAM_DATA_URL = 'https://api.cartolafc.globo.com/auth/time'


class TeamManager:
    """
    This class reads the team data from the game
    I also provides methods for managing the team
    """
    def __init__(self, token):
        # Inicialize team data
        self.token = token
        self.headers = {'X-GLB-Token': self.token}
        self.team_info = {}
        self.patrimonio = 0
        self.valor_time = 0
        self.esquema = 0
        self.atletas = {}
        # Load team data
        self.load_team_data()

    def load_team_data(self):

        team_data = requests.get(TEAM_DATA_URL, headers=self.headers)
        team_data.raise_for_status()

        team_json = team_data.json()
        self.team_info = team_json['time']
        self.patrimonio = team_json['patrimonio']
        self.valor_time = team_json['valor_time']
        self.esquema = team_json['esquema_id']
        self.atletas = team_json['atletas']

    def print_team_info(self):
        print('')
        print('Time atual:')
        print(' Nome do Time: %s' % self.team_info['nome'])
        print(' Nome do Cartoleiro: %s' % self.team_info['nome_cartola'])
        print(' Patrimônio: %f' % self.patrimonio)
        print(' Valor do Time: %f' % self.valor_time)
        print(' Atletas:')
        for atleta in self.atletas:
            print(' - ' + atleta['apelido'])
