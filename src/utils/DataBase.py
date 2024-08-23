import os
import pymysql
from src.utils.config_loader import load_config


class DataBase(object):
    def __init__(self):
        pass

    @staticmethod
    def dbconnect(where='localhost'):
        '''
        werer: localhost | remote
        '''

        sp = os.path.join(os.getcwd(), "config/database.yml").replace("\\","/")
        config = load_config(sp)
        infolist = config[where]

        try:
            connection = pymysql.connect(
                host=infolist['host'],
                user=infolist['username'],
                password=infolist['passwd'],
                database=infolist['database'],
                port=int(infolist['port']),
                charset='utf8mb4',
                read_timeout=30,
                write_timeout=30,
                connect_timeout=10,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            return connection
        except Exception as e:
            pass


