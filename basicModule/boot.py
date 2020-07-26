from basicModule import Basic
from basicModule.configuration import config_loader


def run(name):
    config = config_loader(name).config
    url_manager = _load_url_manager(config['URLManger'])
    donwloader = _load_donwloader(config['Downloader'])
    parser = _load_parser(config['Parser'])
    data_manager: Basic.DataManager = _load_data_mode(config['DataManager'])
    Basic.Scheduler().load(
        url_manager=url_manager,
        downloader=donwloader,
        parser=parser,
        data_manager=data_manager
    ).execute()


def import_mo(config):
    if 'module' not in config:
        return None
    mop = config['module']
    mo = __import__(mop)
    if hasattr(mo, mop.split('.')[-1]):
        return getattr(mo, mop.split('.')[-1])
    else:
        return None


def _load_url_manager(config):
    mo = import_mo(config)
    if mo is None:
        mode = Basic.URLManger
    else:
        mode = getattr(mo, config['classN'])
    url_manager = mode()
    method = getattr(url_manager, config['method'])
    method(config)
    return url_manager


def _load_donwloader(config):
    mo = import_mo(config)
    if mo is None:
        mode = Basic.Downloader
    else:
        mode = getattr(mo, config['classN'])
    return mode(config)


def _load_parser(config):
    mo = import_mo(config)
    if mo is None:
        mode = Basic.Parser
    else:
        mode = getattr(mo, config['classN'])
    return mode(config)


def _load_data_mode(config):
    mo = import_mo(config)
    mode = getattr(mo, config['mode'])
    return mode(config[config['mode']])
