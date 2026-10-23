import requests
from urllib.parse import urljoin
from getpass import getpass
from termcolor import colored
from html_form_to_dict import html_form_to_dict
from bs4 import BeautifulSoup
import re
from requests_toolbelt import MultipartEncoder
import random
import string

from src import helper

def gen_multipart_format(data):
    """Generate multipart format for form data.
    
    Args:
        data: Dictionary of form data to encode.
        
    Returns:
        MultipartEncoder with the formatted data.
    """
    boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    return MultipartEncoder(fields=data, boundary=boundary)

class TIOJ_Session:
    """Session handler for TIOJ operations.
    
    An object that supports basic TIOJ session operations.
    With an assumption of interacting with TIOJ, 
    some behaviors become simplified rather than generalized.
    
    Always prints error and terminates when an unexpected error occurs.
    """
    
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
        """Construct full URL from endpoint."""
        return urljoin(self.tioj_url, endpoint)

    def get(self, endpoint):
        """Send a GET request to the endpoint.
        
        Args:
            endpoint: The endpoint path to request.
            
        Returns:
            Response object from the GET request.
            
        Raises:
            Calls helper.throw_error on request failure.
        """
        try:
            response = self.tioj_session.get(self.get_url(endpoint))
        except Exception as e:
            helper.throw_error(str(e))
        if response.status_code >= 400:
            helper.throw_error(f"GET {endpoint}: Status Error with http status code {response.status_code}")
        return response

    def post(self, endpoint, data=None, files=None, headers=None):
        """Send a POST request to the endpoint with given data.
        
        Args:
            endpoint: The endpoint path to request.
            data: Optional dictionary of form data.
            files: Optional files to upload.
            headers: Optional HTTP headers.
            
        Returns:
            Response object from the POST request.
            
        Raises:
            Calls helper.throw_error on request failure.
        """
        if data is None:
            data = {}
        if files is None:
            files = {}
        if headers is None:
            headers = {}
        try:
            response = self.tioj_session.post(self.get_url(endpoint), data=data, files=files, allow_redirects=True, headers=headers)
        except Exception as e:
            helper.throw_error(str(e))
        if response.status_code >= 400:
            helper.throw_error(f"POST {endpoint}: Status Error with http status code {response.status_code}")
        return response

    def get_form(self, endpoint, index=0, name=None, id=None):
        """Parse the form at the endpoint.
        
        Args:
            endpoint: The endpoint containing the form.
            index: Index of the form to parse (default: 0).
            name: Optional name attribute of the form.
            id: Optional id attribute of the form.
            
        Returns:
            Tuple of (form_data dict, submit_endpoint).
        """
        response = self.get(endpoint)
        try:
            form = html_form_to_dict(response.content, index=index, name=name, id=id)
        except IndexError as e:
            helper.throw_error(f'Cannot find a form at endpoint {endpoint}')
        form_data = dict(form)
        submit_endpoint = form.form.get('action')
        return form_data, submit_endpoint 

    def submit_form(self, endpoint, data, deldata=None, files=None, index=0, name=None, id=None, multipart=False):
        """Parse form, replace fields from given data, and submit.
        
        Args:
            endpoint: The endpoint containing the form.
            data: Dictionary of form fields to update.
            deldata: Optional list of fields to delete.
            files: Optional files to upload.
            index: Index of the form to parse (default: 0).
            name: Optional name attribute of the form.
            id: Optional id attribute of the form.
            multipart: Whether to use multipart encoding (default: False).
            
        Returns:
            Response object from form submission.
        """
        if deldata is None:
            deldata = []
        if files is None:
            files = {}
        form_data, submit_endpoint = self.get_form(endpoint, index, name, id)
        response = self.get(endpoint)
        for key in data:
            form_data[key] = data[key]
        for key in deldata:
            del form_data[key]
        headers = {}
        if multipart:
            m = gen_multipart_format(form_data)
            headers = {
                "Content-Type": m.content_type
            }
            form_data = m
        response = self.post(submit_endpoint, data=form_data, files=files, headers=headers)
        if response.status_code >= 400:
            helper.throw_error(f"Form submission {endpoint}: Status Error with http status code {response.status_code}")
        return response

    def loggedin(self):
        """Check if the session is currently logged in.
        
        Returns:
            True if logged in, False otherwise.
        """
        return len(self.tioj_session.cookies) == 2  # TODO: find a more general approach

    def login(self, tioj_username='', tioj_password=''):
        """Login to TIOJ with username and password.
        
        Args:
            tioj_username: TIOJ username (prompted if empty).
            tioj_password: TIOJ password (prompted if empty).
            
        Raises:
            Calls helper.throw_error if login fails.
        """
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

    def whoami(self):
        """Return current session's username.
        
        Returns:
            Username if logged in, empty string otherwise.
            
        Raises:
            Calls helper.throw_error if user page cannot be found.
        """
        if not self.loggedin():
            return ''
        response = self.get('/')
        html_soup = BeautifulSoup(response.text, "html.parser")
        for li in html_soup.find_all('li'):
            if re.match("^/users/+", li.find('a')['href']) and li.text != 'Sign out':
                return li.text
        helper.throw_error("Cannot find the user page, maybe your TIOJ has an unexpected format?")
        
    def isadmin(self):
        """Check whether current session has admin permission.
        
        Returns:
            True if user is admin, False otherwise.
        """
        if not self.loggedin():
            return False
        # New TIOJ
        response = self.get(f'/users/{self.whoami()}')
        html_soup = BeautifulSoup(response.text, "html.parser")
        td_array = html_soup.find_all('td')
        for i, tag in enumerate(td_array):
            if tag.string == 'Admin:' and td_array[i + 1].string == 'true':
                return True 
        # Old TIOJ
        response = self.get(f'/')
        html_soup = BeautifulSoup(response.text, "html.parser")
        links = html_soup.find_all('a', href=True)
        for link in links:
            if link['href'] == '/edit_announcement':
                return True
        return False
