'''This module creates a authentication session object '''
__version__ = 1.0
__author__ = "Harikrishnan T"
__website__ = "vxplanet.com"

import requests
from tabulate import tabulate
import sys

class NsxLogin():
    def __init__(self, url, headers, body):
        self._url = url
        self.headers = headers
        self._body = body

    def create_session(self):
        '''Class method to create a session based authentication token (X-XSRFToken) and use it for subsequent operations.'''
        try:
            response = requests.post(self._url + "/api/session/create", headers=self.headers, data=self._body, verify=False)
        except requests.exceptions.RequestException as exception:
            print(tabulate([["NSX Manager API not reachable", exception]], headers=["Error", "Details"], showindex=True, tablefmt="fancy_grid"))
            sys.exit()
        if response:
            self.xsrftoken = response.headers["x-xsrf-token"]
            self.cookie = response.cookies
        else:
            print(f"\nAuthentication Failure ({response.status_code})\n")
            print(response.json())
            #print(tabulate(list(map(list, response.json().items())), headers=["Error", "Details"], showindex=True, tablefmt="fancy_grid"))
            sys.exit()

    def destroy_session(self):
        '''Class method to destroy the API session token and logout'''
        response = requests.post(self._url + "/api/session/destroy", headers=self.headers, cookies=self.cookie, verify=False)
        if response:
            print(f"\nSUCCESS!!! Successfully logged out from the system ({response.status_code})\n")
        else:
            print(f"\nFAILURE!!! Logout failed. Try again")