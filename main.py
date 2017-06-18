#############################
# Data collector for CartolaFC
#
# Developed by Eric Baum
#
# Copyright, 2017 - Eric Baum
#############################

import argparse
from Auth.AuthenticationHandler import AuthenticationHandler
from Team.TeamManager import TeamManager


def app_loop(team_manager):
    dont_exit = True

    while dont_exit:
        print()
        print("Escolha um número:")
        print(" 1 - Ver time")
        print(" 2 - Recarregar time atual")
        print(" 3 - Gerar escalação randômica")
        print(" 4 - Salvar escalação")
        print(" 5 - Sair")
        choice = input("Opção?")

        if choice == "1":
            team_manager.print_team_info()
        elif choice == "2":
            team_manager.load_team_data()
        elif choice == "3":
            team_manager.generate_random_team()
        elif choice == "4":
            team_manager.save_team()
        elif choice == "5":
            dont_exit = False
        else:
            print("Opção inválida")

    return


def main():
    # Gather execution arguments
    parser = argparse.ArgumentParser('Login to cartola and collect some data.\n Parameters: ')
    parser.add_argument("-u", "--user", help='User email', nargs=1, type=str, required=True)
    parser.add_argument("-p", "--password", help='User password', nargs=1, type=str, required=True)
    args = parser.parse_args()

    # Authenticates
    authenticator = AuthenticationHandler(args.user[0], args.password[0])
    glb_token = authenticator.get_token()

    # Initialize the team manager
    team_manager = TeamManager(glb_token)

    app_loop(team_manager)
    print("Tchau!")

if __name__ == "__main__":
    main()
