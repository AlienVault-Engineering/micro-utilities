import json

import logging
import os
import sys

from datetime import timedelta

config = None
conn = None
CONFIG_FILE = "CONFIG_FILE"
BASE_CONFIG_FILE = "BASE_CONFIG_FILE"
os.environ.setdefault('ENVIRONMENT','unit-test')


def _load_config():
    global config
    if not config:
        reload_config()
    return config


def reload_config(additional_config_files=None):
    global config
    config_file_list = [os.environ.get(BASE_CONFIG_FILE, "{0}/config.json".format(os.path.dirname(__file__))),
                        os.environ.get(CONFIG_FILE, "config.json")]
    if additional_config_files:
        if isinstance(additional_config_files,list):
            config_file_list.extend(additional_config_files)
        else:
            config_file_list.append(additional_config_files)
    config = {}
    for config_file in config_file_list:
        if os.path.exists(config_file):
            load_config_file(config, config_file)
    expanded = {}
    for key, value in config.iteritems():
        if key in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]:
            os.environ[key] = value
        if isinstance(value, basestring) and "{" in value and "}" in value and "{}" not in value:
            try:
                expanded[key] = value.format(**config)
            except IndexError:
                logging.error("Error expanding value {} - {}".format(value, str(config)))
    config.update(expanded)


def load_config_file(config_target, config_file):
    env = get_environment()
    with open(config_file, "r+") as fp:
        evaluated_content = ""
        for line in fp.readlines():
            expanded = os.path.expandvars(line)
            evaluated_content += expanded
        config_store = json.loads(evaluated_content)
        default_ = config_store["default"]
        if default_:
            config_target.update(default_)
        if env in config_store:
            config_target.update(config_store[env])


def get_environment():
    return str.lower(os.environ.get("ENVIRONMENT", "DEVELOPMENT"))


def get_value(key):
    return get_value_default(key, None)


def get_int_value(key):
    default = get_value_default(key, None)
    if default:
        return int(default)
    raise ValueError("Requested unknown key")


def get_boolean(key):
    default = get_value_default(key, None)
    if default is not None:
        return bool(default)
    raise ValueError("Requested unknown key")


def get_secret(key):
    return get_value(key)


def get_value_default(key, default):
    return _load_config().get(key, default)


def init_docker_logging():
    init_logger(logging.root)

def init_flask_app(app):
    config = _load_config()
    app.config.from_mapping(config)
    app.secret_key = app.config['SECRET_KEY']
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=get_value_default("jwt-expiration-time-minutes",60))
    app.config['PREFERRED_URL_SCHEME'] = get_value_default('external-url-scheme','https')


def init_flask_logging(app):
    # Configure logging
    init_logger(app.logger)


def init_logger(root):
    level_name = logging.getLevelName(get_value_default('root-logging-level', 'WARN'))
    root.setLevel(level_name)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level_name)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    py_root = logging.getLogger()
    py_root.setLevel(level_name)
    py_root.addHandler(ch)


def get_config():
    return _load_config()


def render_string(template):
    return template.format(**_load_config())