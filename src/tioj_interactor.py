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
    
    def __init__(self, tioj_url='', login_endpoint=''):
        if tioj_url == '':
            self.tioj_url = input('TIOJ url: ')
        else:
            self.tioj_url = tioj_url
        if login_endpoint == '':
            self.login_endpoint = input('Login endpoint: ')
        else:
            self.login_endpoint = login_endpoint
        self.tioj_session = requests.Session()

    def get_url(self, endpoint):
        return urljoin(self.tioj_url, endpoint)

    # send a get request to the endpoint
    def get(self, endpoint):
        try:
            response = self.tioj_session.get(self.get_url(endpoint))
        except Exception as e:
            helper.throw_error(str(e))
        if response.status_code >= 400:
            helper.throw_error(f"GET {endpoint}: Status Error with http status code {response.status_code}")
        return response

    # send a post request to the endpoint with given data
    def post(self, endpoint, data={}, files={}):
        try:
            response = self.tioj_session.post(self.get_url(endpoint), data=data, files=files, allow_redirects=True)
        except Exception as e:
            helper.throw_error(str(e))
        if response.status_code >= 400:
            helper.throw_error(f"POST {endpoint}: Status Error with http status code {response.status_code}")
        return response

    # parse the index-th form with name and id in the endpoint
    def get_form(self, endpoint, index=0, name=None, id=None):
        response = self.get(endpoint)
        try:
            form = html_form_to_dict(response.content, index=index, name=name, id=id)
        except IndexError as e:
            helper.throw_error(f'Cannot find a form at endpoint {endpoint}')
        form_data = dict(form)
        submit_endpoint = form.form.get('action')
        return form_data, submit_endpoint 

    # parse the index-th form with name and id in the endpoint, replace the fields from given data
    def submit_form(self, endpoint, data, deldata=[], files={}, index=0, name=None, id=None):
        form_data, submit_endpoint = self.get_form(endpoint, index, name, id)
        response = self.get(endpoint)
        for key in data:
            form_data[key] = data[key]
        for key in deldata:
            del form_data[key]
        response = self.post(submit_endpoint, data=form_data, files=files)
        if response.status_code >= 400:
            helper.throw_error(f"Form submission {endpoint}: Status Error with http status code {response.status_code}")
        return response

    # return True if the session is logged in now
    def loggedin(self):
        return len(self.tioj_session.cookies) == 2 #TODO: find a more general approach

    # login TIOJ
    def login(self, tioj_username='', tioj_password=''):
        if tioj_username == '':
            tioj_username = input('TIOJ username: ')
        if tioj_password == '':
            tioj_password = getpass(f'(user: {tioj_username}) Password: ')
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
        return html_soup.find_all('li')[-2].text
        
    # check whehter current session has admin permission
    def isadmin(self):
        if not self.loggedin():
            return False
        response = self.get(f'/')
        html_soup = BeautifulSoup(response.text, "html.parser")
        links = html_soup.find_all('a', href=True)
        for link in links:
            if link['href'] == '/edit_announcement':
                return True
        return False
