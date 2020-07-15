"""
数据库表类
Autchor: shaoqing
"""


class table:
    def __init__(self, **params):
        self.name = params['name']
        self.field_map = params['field_map']

    def set(self, **params):  # 设置属性
        if 'name' in params:
            self.name = params['name']
        if 'field_map' in params:
            self.field_map = params['field_map']
