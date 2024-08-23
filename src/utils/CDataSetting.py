import os
import os.path
from typing import Any
from src.utils.config_loader import load_config


class CDataSetting(object):

    def __init__(self, fp=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config/data_setting.yml").replace("\\","/") ):
        self.config = load_config(fp)

    def __call__(self, what):
        if what == "dasai_conv":
            return self.dasai_conv()
        if what == "dasai_dhp":
            return self.dasai_dhp()


    def dasai_conv(self):
        '''主要提供调用者将主站预测的文件转换工作所需要的目录'''
        file_type = self.config['inputwork']['tmp']
        data_input_base = self.config['inputwork']['base']  # 数据输入的基础目录
        txt_file_path = os.path.join(data_input_base, file_type).replace("\\","/")

        outp = self.config['outputwork']['tmp']
        out_base = self.config['outputwork']['base']
        output_dir = os.path.join(out_base, outp).replace("\\","/")
        return txt_file_path, output_dir
    
    def dasai_dhp(self):
        '''处理大赛数据源目录处理
            返回数据文件父目录列表，文件名与必要内容映射字典，文件名与应执行的入库sql字典
        '''
        data_input_base = self.config['inputwork']['base']
        site_list = self.config['inputwork']['subsite']
        type_fd = self.config['structmapping_dasai']
        put_in_db_p = self.config['file_tablename_mapping_dasai']
        column_map = self.config['columns_mapping_dasai']
        return ([os.path.join(data_input_base, f).replace("\\", '/')  for f in site_list],
                type_fd, put_in_db_p, column_map)





if __name__ == "__main__":
    print(os.getcwd())
