import os
from src.utils.config_loader import load_config

class CRemote():
    def __init__(self, fp=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config/remote.yml").replace("\\","/")):
        self.config = load_config(fp)

        self.hostname = self.config['server']['hostname']
        self.port = self.config['server']['port']
        self.username = self.config['server']['username']
        self.password = self.config['server'].get('password', None)
        self.private_key_path = self.config['server'].get('private_key_path', None)

        self.refilepath = self.config['file_path']['remote']
        objwork = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.localpath = os.path.join(objwork,self.config['file_path']['local'])