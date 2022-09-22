import requests
from urllib.parse import urljoin
from getpass import getpass
from termcolor import colored
from html_form_to_dict import html_form_to_dict
from bs4 import BeautifulSoup

from src import helper

'''
An object supports basic TIOJ session operations.
With an assumption of interacting with TIOJ, 
some behaviors become simplified rather than generalized.

Always print error and terminate when an unexpected error happen.
'''
class TIOJ_Session:
    
    def __init__(self, tioj_url, login_endpoint='users/sign_in'):
        self.tioj_url = tioj_url
        self.tioj_session = requests.Session()
        self.login_endpoint = login_endpoint

    # send a get request to the endpoint
    def get(self, endpoint):
        response = self.tioj_session.get(urljoin(self.tioj_url, endpoint))
        if response.status_code >= 400:
            helper.throw_error(f"GET {endpoint}: Status Error with http status code {response.status_code}")
        return response

    # send a post request to the endpoint with given data
    def post(self, endpoint, data={}):
        response = self.tioj_session.post(urljoin(self.tioj_url, endpoint), data=data)
        if response.status_code >= 400:
            helper.throw_error(f"POST {endpoint}: Status Error with http status code {response.status_code}")
        return response

    # parse the form in the endpoint, replace the fields from given data
    # Note: we assume that there is only one TIOJ form in the endpoint
    def submit_form(self, endpoint, data):
        response = self.get(endpoint)
        try:
            form = html_form_to_dict(response.content)
        except IndexError as e:
            helper.throw_error(f'Cannot find a form at endpoint {endpoint}')
        form_data = dict(form)
        submit_endpoint = form.form.get('action')
        for key in data:
            if key not in form_data:
                helper.throw_error(f"Cannot find {key} in the form at endpoint {endpoint}")
            form_data[key] = data[key]
        response = self.post(submit_endpoint, form_data)
        if response.status_code >= 400:
            helper.throw_error(f"Form submission {endpoint}: Status Error with http status code {response.status_code}")
        return response

    # return True if the session is logged in now
    def loggedin(self):
        return len(self.tioj_session.cookies) == 2

    # login TIOJ
    def login(self, tioj_username='', tioj_password=''):
        if tioj_username == '':
            tioj_username = input('TIOJ username: ')
        if tioj_password == '':
            tioj_password = getpass()
        helper.throw_status('Logging in...')
        data = {
            'user[username]': tioj_username,
            'user[password]': tioj_password,
            'user[remember_me]': '1'
        }
        self.submit_form(self.login_endpoint, data)
        if not self.loggedin():
            helper.throw_error("Oh No! Invalid login or password.") 
        helper.throw_info('Login successful!')

    # return current session's username, or return an empty string if not logged in
    def whoami(self):
        if not self.loggedin():
            return ''
        response = self.get('/')
        html_soup = BeautifulSoup(response.text, "html.parser")
        return html_soup.find_all('td')[2].string #TODO: find a more general approach
        
    # check whehter current session has admin permission
    def isadmin(self):
        if not self.loggedin():
            return False
        response = self.get(f'/users/{self.whoami()}')
        html_soup = BeautifulSoup(response.text, "html.parser")
        td_array = html_soup.find_all('td')
        for i, tag in enumerate(td_array):
            if tag.string == 'Admin:':
                return td_array[i + 1].string == 'true'
        return False
