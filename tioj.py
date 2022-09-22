import typer
import json

import src.helper as helper
from src.tioj_interactor import TIOJ_Session

TIOJ_URL = 'http://localhost:4000' #TODO: read from the configuration file

app = typer.Typer()

@app.command()
def whoami(username='', password=''):
    tioj_session = TIOJ_Session(TIOJ_URL)
    tioj_session.login(username, password)
    helper.throw_info(f'You are: [bold]{tioj_session.whoami()}[/bold]')

@app.command()
def isadmin(username='', password=''):
    tioj_session = TIOJ_Session(TIOJ_URL)
    tioj_session.login(username, password)
    if tioj_session.isadmin():
        helper.throw_info(f'You have admin permission!')
    else:
        helper.throw_info(f'You don\'t have admin permission!')

if __name__ == "__main__":
    app()
