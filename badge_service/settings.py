import configparser


def get_config():
    config = configparser.ConfigParser()
    config.read('settings.cfg')

    return config
