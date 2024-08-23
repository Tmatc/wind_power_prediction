import pandas as pd
import os


class DsdataClass(object):
    '''大赛数据类，用于从文件读取大赛提供的原始数据
       根据文件加载数据到内存
    '''
    def __init__(self, type_dict:dict):
        '''
        type_dict: 文件类型与内容结构的映射
        '''
        self.file_path = ""
        self.type_dict = type_dict
        
    def __call__(self, p, ft):
        self.file_path = p
        return self.fit(ft)

    def fit(self, ft):
        if ft not in self.type_dict:
            raise "没有该类型文件的映射列"
        columns = self.type_dict[ft]  # 文件列名数组
        _, file_extension = os.path.splitext(self.file_path.lower())
        if file_extension == '.csv':
            df = pd.read_csv(self.file_path, usecols=columns, encoding='utf-8')
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(self.file_path, usecols=columns)
        else:
            df = df = pd.read_csv(self.file_path, usecols=columns, encoding='utf-8')
        return df


    