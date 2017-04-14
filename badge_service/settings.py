import configparser
import os


def get_config():
    config = configparser.ConfigParser()
    config.read('../settings.cfg')
    parsed_config = {
        'client_id': os.getenv("")
    }

    if parsed_config['client_id'] is None:
        parsed_config['client_id'] = config['DEFAULT'].get('client_id')


    return parsed_config
