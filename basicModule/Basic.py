"""
 基本模块
 Autchor ：shaqing
"""

"""
 URL管理器
"""


class URLManger:  # url管理器
    def __init__(self):
        self.url_basket = []  # 待处理URL列表
        self.url_trash = []  # 已爬取得
        self.recycle = False  # 是否回收URL（默认不回收）

    def add(self):
        pass

    def call(self):
        pass

    def recycling(self):
        pass


"""
下载器
"""


class Downloader:
    def __init__(self, **params):
        self.container = []  # （数据容器）
        self.mode = params['mode'] if "mode" in params else "HTML"  # （下载数据的模式json/html）

    def request(self):  # （获取想要内容)
        pass


"""
解析器
"""


class Parser:
    def __init__(self, conductor):
        self.conductor = conductor  # 解析规则引导）

    def parse(self):  # （解析数据）
        pass

    def json_parse(self):
        pass

    def html_parse(self):
        pass


"""
数据管理器
"""


class DataManager:
    def __init__(self, **params):
        self.mode = params['mode'] if 'mode' in params else 'csv'  # （数据保存模式）
        self.base_path = params['base_path']  # （文件基本路径）
        self.data_header = params['data_header']  # （数据表头）
        self.mode_fns = {'csv': self.save_csv, 'db': self.save_db}

    def save(self):  # （保存数据）
        self.mode_fns[self.mode]()

    def save_csv(self):  # （以csv方式保存数据）
        pass

    def save_db(self):  # （以数据库的形式保存数据）
        pass

    def add_mode_fns(self):  # （自定义保存数据的方式）
        pass


"""
爬虫调度器
"""


class Scheduler:
    def __init__(self, **params):
        self.url_manager: URLManger = params['url_manager']  # URL管理器实例
        self.downloader: Downloader = params['downloader']  # 下载器实例
        self.parser: Parser = params['parser']  # 解析器实例
        self.data_manager: DataManager = params['data_manager']  # 数据管理器实例

    def execute(self):
        pass

