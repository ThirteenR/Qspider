import yaml

'''
配置文件加载
'''


class config_loader:
    config = dict()

    def __init__(self, name):
        with open("config/" + name + ".yaml", "rb") as y:
            data = yaml.safe_load_all(y)
            self.config = list(data)[0]

if __name__=="__main__":
    loader = config_loader('yc')
    print(loader.config)