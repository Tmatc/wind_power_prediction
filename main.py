import os.path
from src.utils.config_loader import load_config
from src.utils import fconvertion
from src.utils.DataSetting import DataSetting
import os


def file_converted():
    '''
    将主站预测文件装换成大赛需要的文件
    '''
    # 定义主站编号与大赛编号映射
    mapping = {"DRF3999": 'A', "DRF4000": 'B', "DRF4001": 'C',
               "DRF4002": 'D', "DRF4005": 'E', "DRF4006": 'F'}
    
    ds = DataSetting()

    txt_file_path, output_dir = ds('dasai_conv')

    files = os.listdir(txt_file_path)
    for f in files:
        input_path = os.path.join(txt_file_path, f).replace("\\",'/')
        # print(input_path)

        fconvertion.txt_to_csv(input_path, output_dir, mapping)
    

if __name__ == "__main__":

    file_converted()
    

