import csv as c
import mysql.connector as mc

from basicModule.Basic import DataManager

"""
csv文件模式
"""


class csv(DataManager):
    def __init__(self, cvs: dict, **params):
        self.base_path = cvs['base_path']  # （文件基本路径）
        self.data_header = cvs['data_header']  # （数据表头）
        self.counts = cvs['counts']

    def save(self, rows):
        p = 0
        length = len(rows)
        while True:
            file_csv = self.base_path + '-' + str(p) + ".csv"
            start = p * self.counts
            end = start + self.counts
            if length <= end:
                end = length
            p += 1
            rs = rows[start: end]
            isnew = False
            try:
                with open(file_csv, "r") as n:
                    pass
            except FileNotFoundError as fn:  # 没有找到当前文件
                isnew = True
                print("Create file " + file_csv + ">>>>>")

            with open(file_csv, "a", newline="", encoding="utf-8-sig") as f:
                writer = c.writer(f)  # 列表模式写入
                if isnew:
                    writer.writerow(self.data_header)  # 输入表头
                writer.writerows(rs)  # 将当前行的数据写入csv文件中
                print("写入" + file_csv + "共" + str(end-start) + "条数据\n\n")

            if end == length:
                break


"""
数据库模式
"""


class db(DataManager):
    def __init__(self, params):
        self.connection = mc.connect(**params['info'])
        self.table = params['table']  # (操作的表）

    def close(self):
        self.connection.close()
        print("db connection is closed  ")

    def _create_table(self):
        try:
            fields = []
            for k in self.table['fields']:
                fields.append(k + ' ' + self.table['fields'][k])
            print("creating table " + self.table['name'])
            self.connection.cursor().execute("CREATE TABLE " + self.table['name'] + " (" + ','.join(fields) + ")")
        except Exception as e:
            print(e)

    def save(self, rows):
        self._create_table()
        filednames = []
        for k in self.table['fields']:
            filednames.append(k)
        fl = ",".join(filednames)
        cursor = self.connection.cursor()
        sql = "INSERT INTO " + self.table['name'] + "  VALUES ({})"
        print(sql)
        sql = self._sql_format(len(filednames), sql)
        print(sql)
        cursor.executemany(sql, rows)
        self.connection.commit()
        print(str(cursor.rowcount) + " rows inserted")
        self.close()

    def _sql_format(self, num, sql) -> str:
        ll = []
        for i in range(num):
            ll.append('%s')
        value = ','.join(ll)
        print(value + "fsaf")
        return sql.format(value)
