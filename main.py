#############################
# Data collector for CartolaFC
#
# Developed by Eric Baum
#
# Copyright, 2017 - Eric Baum
#############################

import argparse
from Auth.authentication_handler import AuthenticationHandler


def main():
    # Gather execution arguments
    parser = argparse.ArgumentParser('Login to cartola and collect some data.\n Parameters: ')
    parser.add_argument("-u", "--user", help='User email', nargs=1, type=str, required=True)
    parser.add_argument("-p", "--password", help='User password', nargs=1, type=str, required=True)
    args = parser.parse_args()

    authenticator = AuthenticationHandler(args.user[0], args.password[0])
    glb_token = authenticator.get_token()
    print(glb_token)

if __name__ == "__main__":
    main()
