class csv:
    def __init__(self,params: dict):
        self.base_path = params['base_path']  # （文件基本路径）
        self.data_header = params['data_header']  # （数据表头）