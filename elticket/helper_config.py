from configparser import RawConfigParser
from elticket import config


def _get_config_path():
    return config.config_ini_filepath


def get_config():
    cfg = RawConfigParser()
    cfg.read(_get_config_path())
    return cfg


# def write_to_config(config_parser: RawConfigParser):
#     with open(_get_config_path(), 'w') as configfile:
#         config_parser.write(configfile)


def get_config_value(section, option):
    cfg = get_config()
    # cfg.get(section, option)
    return cfg.get(cfg.sections()[section], option)



def write_to_config(section, option, value):
    cfg = get_config()
    cfg.set(cfg.sections()[section], option, value)
    with open(_get_config_path(), 'w') as configfile:
        cfg.write(configfile)

