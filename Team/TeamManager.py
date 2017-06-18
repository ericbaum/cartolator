#############################
# Data collector for CartolaFC
#
# Developed by Eric Baum
#
# Copyright, 2017 - Eric Baum
#############################

import requests
import random
import operator

TEAM_DATA_URL = 'https://api.cartolafc.globo.com/auth/time'
MERCADO_URL = 'https://api.cartolafc.globo.com/atletas/mercado'
ESQUEMAS_URL = 'https://api.cartolafc.globo.com/esquemas'


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
        self.esquema = ''
        self.atletas = []
        self.new_team = []
        self.posicoes = {}
        self.esquemas = []
        self.mercado = {'goleiro': ''}
        # Load market and team data
        self._load_market()
        self._load_esquemas()
        self.load_team_data()

    def load_team_data(self):

        team_data = requests.get(TEAM_DATA_URL, headers=self.headers)
        team_data.raise_for_status()

        team_json = team_data.json()
        self.team_info = team_json['time']
        self.patrimonio = team_json['patrimonio']
        self.valor_time = team_json['valor_time']
        esquema_id = team_json['esquema_id']
        for esquema in self.esquemas:
            if esquema['esquema_id'] == esquema_id:
                self.esquema = esquema['nome']
                break
        self.atletas = team_json['atletas']

    def _load_market(self):
        mercado_data = requests.get(MERCADO_URL)
        mercado_data.raise_for_status()

        mercado_json = mercado_data.json()
        self.posicoes = mercado_json['posicoes']
        for posicao in self.posicoes.keys():
            self.mercado[int(posicao)] = []

        provavel_id = 0
        for status_id, status in mercado_json['status'].items():
            if status['nome'] == "Provável":
                provavel_id = status['id']
                break

        for atleta in mercado_json['atletas']:
            if atleta['status_id'] is provavel_id:
                posicao_id = atleta['posicao_id']
                mercado_pos = self.mercado[posicao_id]
                mercado_pos.append((atleta['atleta_id'], atleta['apelido'], atleta['preco_num'], posicao_id))

    def _load_esquemas(self):
        esquemas_data = requests.get(ESQUEMAS_URL)
        esquemas_data.raise_for_status()

        self.esquemas = esquemas_data.json()

    def generate_random_team(self):
        esquema = random.choice(self.esquemas)
        posicoes = esquema['posicoes']
        posicoes_map = {}
        random_team = []

        for posicao in self.posicoes.values():
            posicoes_map[posicao['id']] = posicao['abreviacao']
            posicoes_map[posicao['abreviacao']] = posicao['id']

        for posicao_name, posicao_quant in posicoes.items():
            posicao_id = posicoes_map[posicao_name]

            for _ in range(posicao_quant):
                atleta = random.choice(self.mercado[posicao_id])
                if atleta not in random_team:
                    random_team.append(atleta)

        team_value = 0
        for atleta in random_team:
            team_value += atleta[2]

        while team_value > self.patrimonio:
            atleta_caro = max(random_team, key=operator.itemgetter(2))
            posicao_caro = atleta_caro[3]
            valor_caro = atleta_caro[2]
            index_caro = random_team.index(atleta_caro)
            team_value -= valor_caro

            novo_atleta = random.choice(self.mercado[posicao_caro])
            random_team[index_caro] = novo_atleta
            team_value += novo_atleta[2]

        self.new_team = random_team
        self.valor_time = team_value
        self.esquema = esquema['nome']
        self.atletas = []
        for atleta in random_team:
            self.atletas.append({'apelido': atleta[1]})

        print()
        print("Esquema escolhido: %s" % esquema['nome'])
        print("Valor do time: %.2f" % team_value)
        print("Atletas: ")
        for atleta in random_team:
            print(' - ' + atleta[1])

    def save_team(self):
        print("Time salvo!")

    def print_team_info(self):
        print('')
        print('Time atual:')
        print(' Nome do Time: %s' % self.team_info['nome'])
        print(' Nome do Cartoleiro: %s' % self.team_info['nome_cartola'])
        print(' Patrimônio: %f' % self.patrimonio)
        print(' Valor do Time: %f' % self.valor_time)
        print(' Esquema: %s' % self.esquema)
        print(' Atletas:')
        for atleta in self.atletas:
            print(' - ' + atleta['apelido'])
