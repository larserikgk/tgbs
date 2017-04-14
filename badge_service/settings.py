import configparser
import os


def get_config():
    config = configparser.ConfigParser()
    config.read('settings.cfg')

    parsed_config = {
        'crew_template': os.getenv(""),
        'other_template': os.getenv(""),
        'crew_ribbon_folder': os.getenv(""),
        'other_ribbon_folder': os.getenv("")
    }

    if parsed_config['crew_template'] is None:
        parsed_config['crew_template'] = config['BadgeService'].get('crew_template')

    if parsed_config['other_template'] is None:
        parsed_config['other_template'] = config['BadgeService'].get('other_template')

    if parsed_config['crew_ribbon_folder'] is None:
        parsed_config['crew_ribbon_folder'] = config['BadgeService'].get('crew_ribbon_folder')

    if parsed_config['other_ribbon_folder'] is None:
        parsed_config['other_ribbon_folder'] = config['BadgeService'].get('other_ribbon_folder')

    return parsed_config
