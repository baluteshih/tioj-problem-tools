from rich import print

def throw_info(msg):
    print('[bold green]Info: [/bold green]' + msg)

def throw_status(msg):
    print('[blue]Status: [/blue]' + msg)

def throw_warning(msg):
    print('[bold orange]Warning: [/bold orange]' + msg)

def throw_error(msg, exit_code=1):
    print('[bold red]Error: [/bold red]' + msg)
    exit(exit_code)
