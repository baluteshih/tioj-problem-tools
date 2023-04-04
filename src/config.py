from dynaconf import Dynaconf
import os

CONFIGS_DIR = os.environ.get('CONFIGS_DIR')
if not CONFIGS_DIR:
    CONFIGS_DIR = 'configs'

settings = Dynaconf(
    settings_files=[os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIGS_DIR, 'default_settings.toml'),
                    os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIGS_DIR, 'endpoints_settings.toml'),
                    os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIGS_DIR, 'path_settings.toml'),
                    os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIGS_DIR, 'tioj_instance_settings.toml')])
