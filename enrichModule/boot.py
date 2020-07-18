from basicModule.Basic import *
from enrichModule import DataModel
from enrichModule.configuration import config_loader


def run(name):
    config = config_loader(name).config
    url_manager = URLManger()
    url_manager.use_page("http://car.bitauto.com/xuanchegongju/?p=8-12&page={}", config['pg_count'])
    donwloader = Downloader(config['Downloader'])
    parser = Parser(config['Parser'])
    data_manager: DataManager = _load_data_mode(config)
    Scheduler().load(
        url_manager=url_manager,
        downloader=donwloader,
        parser=parser,
        data_manager=data_manager
    ).execute()


def _load_data_mode(config):
    mop = config['DataManager']['module']
    mo = __import__(mop)
    if hasattr(mo, mop.split('.')[-1]):
        dataM = getattr(mo, mop.split('.')[-1])
    else:
        dataM = DataModel
    mode = getattr(dataM, config['DataManager']['mode'])
    return mode(config[config['DataManager']['mode']])
