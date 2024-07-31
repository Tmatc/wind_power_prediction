import os
import os.path
from typing import Any
from src.utils.config_loader import load_config


class DataSetting(object):

    def __init__(self, fp=os.path.join(os.getcwd(), "config/data_setting.yml").replace("\\","/") ):
        self.fp = fp
        self.config = load_config(self.fp)

    def __call__(self, what):
        if what == "dasai_conv":
            return self.dasai_conv()
        if what == "dasai_dhp":
            return self.dasai_dhp()


    def dasai_conv(self):
        file_type = self.config['inputwork']['tmp']
        data_input_base = self.config['inputwork']['base']  # 数据输入的基础目录
        txt_file_path = os.path.join(data_input_base, file_type).replace("\\","/")

        outp = self.config['outputwork']['tmp']
        out_base = self.config['outputwork']['base']
        output_dir = os.path.join(out_base, outp).replace("\\","/")
        return txt_file_path, output_dir
    
    def dasai_dhp(self):
        '''处理大赛数据源目录处理'''
        data_input_base = self.config['inputwork']['base']
        site_list = self.config['inputwork']['subsite']
        return [os.path.join(data_input_base, f).replace("\\", '/')  for f in site_list]





if __name__ == "__main__":
    print(os.getcwd())
