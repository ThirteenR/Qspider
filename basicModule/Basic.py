"""
 基本模块
 Autchor ：shaqing
"""
import time

import requests
from lxml import etree

"""
 URL管理器
"""


class URLManger:  # url管理器
    def __init__(self):
        self.url_basket = []  # 待处理URL列表
        self.url_trash = []  # 已爬取得
        self.recycle = False  # 是否回收URL（默认不回收）

    def use_page(self, config):
        for i in range(1, config['pg_count'] + 1):
            self.add(config['url'].format(i))

    def add(self, url):
        self.url_basket.append(url)
        print("添加URL：" + url)
        return self

    def call(self):  # call生成器用来生成url迭代
        for url in self.url_basket:
            print("调用URL：" + url)
            self.url_trash.append(url)
            yield url

    def recycling(self):  # 子类实现回收规则
        pass


"""
下载器
"""


class Downloader:
    def __init__(self, params):
        self.container = []  # （数据容器）
        self.headers = params['headers']

    def request(self, url_manage: URLManger):  # （获取想要内容) 子类实现
        for url in url_manage.call():
            time.sleep(2)  # 休眠两秒
            yield self.method(url)  # 执行下载调度器，获取响应内容

    def method(self, url) -> str:  # 子类可覆盖重新此方法，丰富请求方式
        return requests.get(url, headers=self.headers).content.decode()


"""
解析器
"""


class Parser:
    def __init__(self, params):
        self.conductor = params['conductor']  # 解析规则引导）
        self.mode = params['mode']  # 解析模式
        self.parse_fns = {'HTML': self._html_parse, 'JSON': self._json_parse}

    def parse(self, rsp) -> dict:  # （解析数据）
        return self.parse_fns[self.mode](rsp)

    def _json_parse(self, rsp) -> dict:  # 子类实现
        pass

    def _html_parse(self, rsp) -> dict:  # 基类实现
        container = {}
        html = etree.HTML(rsp)
        for k in self.conductor:
            print("将" + k + "数据放入容器")
            container[k] = html.xpath(self.conductor[k])
            print("riles: " + self.conductor[k])
            print("Matching data: " + str(container[k]))
        print("响应数据装载完成\n\n")
        return container

    def add_mode_fns(self, mode, fn):  # 添加自定义解析方法
        self.parse_fns[mode] = fn
        pass


"""
数据管理器
"""


class DataManager:
    data = []
    rows = []

    def load_data(self, data):
        self.data = data
        self._data_group()  # 数据分组
        self.save(self.rows)
        return self

    def _data_group(self):
        for container in self.data:
            data_iterators = {}
            for k in container:
                print("创建迭代器:\t" + k)
                data_iterators[k] = self._iterator(container[k])
            self._set_rows(container, data_iterators)
        print("所有迭代器创建完成\n")

    def _iterator(self, content):
        for i in range(len(content)):
            yield str(content[i])

    def _set_rows(self, container, data_iterators):
        count = len(list(container.values())[0]) + 1
        for i in range(1, count):
            content = []  # 定义一个列表行
            for name in container:
                content.append(next(data_iterators[name]))  # 执行每列数据的迭代器，取出当前行所对应的值
            self.rows.append(tuple(content))

    def save(self, rows):  # （保存数据）
        print("save mothed not be implemented ")
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

    def __init__(self):
        print('init no params')

    def execute(self):  # 调度程序的总执行入口
        rsp_generator = self.downloader.request(self.url_manager)  # 获取响应数据的生成器
        data = []
        for rsp in rsp_generator:  # 迭代执行生成器
            res = self.parser.parse(rsp)  # 解析每一次响应的数据
            print(res)
            data.append(res)
        self.data_manager.load_data(data)

    def load(self, **params):
        self.url_manager: URLManger = params['url_manager']  # URL管理器实例
        self.downloader: Downloader = params['downloader']  # 下载器实例
        self.parser: Parser = params['parser'] if 'parser' in params else None  # 解析器实例
        self.data_manager: DataManager = params['data_manager'] if 'data_manager' in params else None  # 数据管理器实例
        print("Scheduler load params successful")
        return self
