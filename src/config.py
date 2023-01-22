from dynaconf import Dynaconf
import os

settings = Dynaconf(
    settings_files=[os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'default_settings.toml'),
                    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'endpoints_settings.toml'),
                    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'path_settings.toml'),
                    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'tioj_instance_settings.toml')])
