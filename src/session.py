import src.helper as helper
from src.config import settings
from src.tioj_interactor import TIOJ_Session

'''
Requirement: None.

Description: Open a logged in TIOJ session from the configured credentials. Every command that
             talks to TIOJ goes through here, so that resolving the credentials stays in one
             place.

Return value: A logged in TIOJ_Session. Prints an error and terminates when admin permission is
              required but the account does not have it.
'''
def open_session(require_admin=False):
    tioj = TIOJ_Session(settings.default.tioj_url, settings.endpoints.login)
    tioj.login(settings.default.tioj_username, settings.default.tioj_password)

    if require_admin and not tioj.isadmin():
        helper.throw_error(f'The user [bold]{tioj.whoami()}[/bold] doesn\'t have admin permission!')

    return tioj
