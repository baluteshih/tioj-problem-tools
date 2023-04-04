import os

SCRIPT_DIR = os.environ.get('SCRIPT_DIR')
if not SCRIPT_DIR:
    SCRIPT_DIR = os.path.dirname(os.path.dirname(__file__))

CONFIGS_DIR = os.environ.get('CONFIGS_DIR')
if not CONFIGS_DIR:
    CONFIGS_DIR = os.path.join(SCRIPT_DIR, 'configs')
