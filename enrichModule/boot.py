from basicModule.Basic import *
from enrichModule.configuration import config_loader


def run(name):
    config = config_loader(name).config
    url_manager = URLManger()
    url_manager.add("http://car.bitauto.com/xuanchegongju/?p=8-12&page={}".format(1))\
        .add("http://car.bitauto.com/xuanchegongju/?p=8-12&page={}".format(2))
    donwloader = Downloader(config['Downloader'])
    parser = Parser(config['Parser'])
    Scheduler().load(
        url_manager=url_manager,
        downloader=donwloader,
        parser=parser
    ).execute()
    
