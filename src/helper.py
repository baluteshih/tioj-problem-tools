from rich import print
import json
import os
from pathlib import Path

import src.env as env

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
    var = var.replace('{SCRIPT_DIR}', env.SCRIPT_DIR)
    var = var.replace('{CONFIGS_DIR}', env.CONFIGS_DIR)
    return var

def read_file(path):
    path = expand_settings_variable(path)
    try:
        content = Path(path).read_text()
    except FileNotFoundError as err:
        throw_error(f'({path}) ' + str(err))
    except Exception as err:
        throw_error(f'Unexpected error ({type(err).__name__}) while opening {path}: ' + str(err))
    return content 

def read_json(path):
    path = expand_settings_variable(path) 
    with open(path) as json_file:
        try:
            res = json.load(json_file)
        except FileNotFoundError as err:
            throw_error(f'({path}) ' + str(err))
        except ValueError as err:
            throw_error(f'({path}) ' + str(err))
        except Exception as err:
            throw_error(f'Unexpected error ({type(err).__name__}) while opening {path}: ' + str(err))
    return res

def write_json(path, data):
    path = expand_settings_variable(path) 
    with open(path, 'w') as json_file:
        json.dump(data, json_file)

def replace_header(content, settings):
    for header in settings.default.replace_headers:
        path = expand_settings_variable(settings.default.replace_header_paths)
        content = content.replace(f'#include "{header}"', read_file(os.path.join(path, header)))
    return content
