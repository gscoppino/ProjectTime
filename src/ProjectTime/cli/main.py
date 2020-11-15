""" A command line client to the ProjectTime REST API.
"""

import os
import requests

from cmd import Cmd
from datetime import datetime

import pandas as pd


class ProjectTimeCmdPrompt(Cmd):
    """ Class definition for the ProjectTime CLI.
    """
    server = None
    server_headers = None

    def do_exit(self, args: str):
        """ Exit the CLI. """
        print("Exiting...")
        raise SystemExit

    ##################### Project-specific #####################

    def do_projects(self, args: str):
        """ List projects. """
        args = args.split()
        active = '--active' in args
        inactive = '--inactive' in args

        # if both active and inactive flags are used, treat it as if no flags were used
        if active and inactive:
            active = False
            inactive = False

        params = {}

        if active:
            params['active'] = True
        if inactive:
            params['active'] = False

        response = requests.get(
            f'{self.server}/rest/projects/',
            params=params,
            headers=self.server_headers
        )

        response.raise_for_status()
        data = response.json()
        print(pd.DataFrame(data).to_markdown())

    def do_mkproject(self, args: str):
        """ Create a project with the given NAME. """
        name = args

        response = requests.post(
            f'{self.server}/rest/projects/',
            headers=self.server_headers,
            json={ 'name': name, 'active': True }
        )

        response.raise_for_status()
        data = response.json()
        print(data)

    def do_rename(self, args: str):
        """ Rename a project with the given ID to the given NAME. """
        args = args.split()
        pk = args[0]
        new_name = ' '.join(args[1:])

        response = requests.patch(
            f'{self.server}/rest/projects/{pk}/',
            headers=self.server_headers,
            json={ 'name': new_name }
        )

        response.raise_for_status()
        data = response.json()
        print(data)

    def do_setactive(self, args: str):
        """ Set the project with the given ID as active. """
        pk = args

        response = requests.patch(
            f'{self.server}/rest/projects/{pk}/',
            headers=self.server_headers,
            json={ 'active': True }
        )

        response.raise_for_status()
        data = response.json()
        print(data)

    def do_setinactive(self, args: str):
        """ Set the project with the given ID as inactive. """
        pk = args

        response = requests.patch(
            f'{self.server}/rest/projects/{pk}/',
            headers=self.server_headers,
            json={ 'active': False }
        )

        response.raise_for_status()
        data = response.json()
        print(data)

    def do_rmproject(self, args: str):
        """ Delete the project with the given ID. """
        pk = args

        response = requests.delete(
            f'{self.server}/rest/projects/{pk}',
            headers=self.server_headers
        )

        response.raise_for_status()
        print("Project has been deleted")

    ##################### Charge-specific #####################

    def do_charges(self, args: str):
        """ List charges. """
        args = args.split()

        # Possible filters on the project list
        filter_by_project = None
        view_open = False
        view_closed = False

        # Parse args
        num_args = len(args)
        while num_args > 0:
            arg = args.pop()
            if arg == "--open":
                view_open = True
            elif arg == "--closed":
                view_closed = True
            else:
                filter_by_project = int(arg)

            num_args = num_args -1

        # if both active and inactive flags are used, treat it as if neither flag was used
        if view_open and view_closed:
            view_open = False
            view_closed = False

        # Build query parameters based on filters
        params = {}

        if view_open:
            params['closed'] = False
        if view_closed:
            params['closed'] = True
        if filter_by_project:
            params['project'] = filter_by_project

        # Issue request and print results
        response = requests.get(
            f'{self.server}/rest/charges/',
            params=params,
            headers=self.server_headers
        )

        response.raise_for_status()
        data = response.json()
        print(pd.DataFrame(data).to_markdown())

    def do_mkcharge(self, args: str):
        """ Create a charge for the project with the given ID, with a start time of now. """
        project_pk = args
        now = datetime.now()

        response = requests.post(
            f'{self.server}/rest/charges/',
            headers=self.server_headers,
            json={ 'project': project_pk, 'start_time': now.isoformat() }
        )

        response.raise_for_status()
        data = response.json()
        print(data)

    def do_commit(self, args: str):
        """ Create an end time commit for the charge with the given ID. """
        pk = args
        now = datetime.now()

        response = requests.patch(
            f'{self.server}/rest/charges/{pk}/',
            headers=self.server_headers,
            json={ 'end_time': now.isoformat() }
        )

        response.raise_for_status()
        data = response.json()
        print(data)

    def do_close(self, args: str):
        """ Close the charge with the given ID. """
        pk = args

        response = requests.patch(
            f'{self.server}/rest/charges/{pk}/',
            headers=self.server_headers,
            json={ 'closed': True }
        )

        response.raise_for_status()
        data = response.json()
        print(data)

    def do_open(self, args: str):
        """ Re-open the charge with the given ID. """
        pk = args

        response = requests.patch(
            f'{self.server}/rest/charges/{pk}/',
            headers=self.server_headers,
            json={ 'closed': False }
        )

        response.raise_for_status()
        data = response.json()
        print(data)


    def do_rmcharge(self, args: str):
        """ Delete the charge with the given ID. """
        pk = args

        response = requests.delete(
            f'{self.server}/rest/charges/{pk}/',
            headers=self.server_headers
        )

        response.raise_for_status()
        print("Charge has been deleted")


def start_repl():
    """ Given credentials to login with, starts the REPL for the ProjectTime CLI.
    """
    server = os.environ.get("PT_SERVER")
    if not server:
        raise Exception(
            "Unable to determine the ProjectTime server to communicate with"
        )

    username = input("Enter username: ")
    password = input("Enter password: ")

    timezone = os.environ.get("PROJECT_TIME_CLI_TIMEZONE")
    if not timezone:
        timezone = input("Enter a timezone: ")

    headers = {'tz':timezone}

    response = requests.post(f"{server}/rest/auth/", headers=headers, json={
        'username': username,
        'password': password
    })

    response.raise_for_status()

    data = response.json()
    token = data['token']
    headers['Authorization'] = f'Token {token}'

    prompt = ProjectTimeCmdPrompt()
    prompt.prompt = '> '
    prompt.server = server
    prompt.server_headers = headers

    prompt.cmdloop('Welcome to the ProjectTime CLI!')

if __name__ == '__main__':
    start_repl()
