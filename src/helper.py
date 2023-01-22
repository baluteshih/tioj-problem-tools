from rich import print
import json
import os
from pathlib import Path

def throw_info(msg):
    print('[bold green]Info: [/bold green]' + msg)

def throw_status(msg):
    print('[blue]Status: [/blue]' + msg)

def throw_warning(msg):
    print('[bold dark_orange]Warning: [/bold dark_orange]' + msg)

def throw_error(msg, exit_code=1):
    print('[bold red]Error: [/bold red]' + msg)
    exit(exit_code)

def expand_settings_variable(var):
    var = var.replace('{SCRIPT_DIR}', os.path.dirname(os.path.dirname(__file__)))
    return var

def read_file(path):
    path = expand_settings_variable(path) 
    return Path(path).read_text() 

def read_json(path):
    path = expand_settings_variable(path) 
    with open(path) as json_file:
        try:
            res = json.load(json_file)
        except ValueError as err:
            throw_error(f'({path}) ' + str(err))
    return res

def write_json(path, data):
    path = expand_settings_variable(path) 
    with open(path, 'w') as json_file:
        json.dump(data, json_file)
