"""
数据库类
"""


class database:
    def __init__(self, table, **conf):
        self.connection = mc.connect(**conf)
        self.db_table = table  # (操作的表）

    def create_table(self):
        pass

    def insert(self, rows):
        pass

    def sql_format(self) -> str:
        pass
