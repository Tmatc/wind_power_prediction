import os
import sys
import time
from src.utils.config_loader import load_config
from src.utils import fconvertion
from src.utils.CDataSetting import CDataSetting
from src.utils.CRemote import CRemote
from src.communication.Filetransfer import Filetransfer
from scripts import upload_ds_interface as updi
ds = CDataSetting()


def file_down(far_list:list):
    current_time = time.localtime()
    cremote = CRemote()
    remotep = cremote.refilepath  # 远程目录基础目录
    locap = cremote.localpath
    for z in far_list:
        refile_name = f"modeloutput-{z}-{current_time.tm_year}{current_time.tm_mon:02d}{current_time.tm_mday}PM.txt"
        remote_file = os.path.join(remotep, str(current_time.tm_year), f"{current_time.tm_mon:02d}", z[:7], refile_name).replace("\\","/")
        local_file = os.path.join(locap, refile_name).replace("\\","/")
        
        with Filetransfer() as ft:
            ft.download_file(remote_file, local_file)


def file_converted():
    '''
    将主站预测文件装换成大赛需要的文件
    '''
    # 定义主站编号与大赛编号映射
    mapping = {"DRF3999": 'A', "DRF4000": 'B', "DRF4001": 'C',
               "DRF4002": 'D', "DRF4005": 'E', "DRF4006": 'F'}
    
    

    txt_file_path, output_dir = ds('dasai_conv')

    files = os.listdir(txt_file_path)
    for f in files:
        input_path = os.path.join(txt_file_path, f).replace("\\",'/')
        # print(input_path)

        fconvertion.txt_to_csv(input_path, output_dir, mapping)

def upload_yun(uplist:list):
    current_time = time.localtime()
    _, output_dir = ds('dasai_conv')
    for fr in uplist:
        filename = f"{fr}_DQ_{current_time.tm_year}{current_time.tm_mon:02d}{current_time.tm_mday+1}.csv"
        outfile = os.path.join(output_dir, filename).replace("\\",'/')
        fkres = updi.dasai_upload(fr, outfile)  # 上传到大赛云平台，返回上报情况
        if fkres['statusCode'] == "200" or fkres['statusCode'] == 200: # 200表示成功
            with open('logs/bj/dsupok.bj', 'w') as f:
                f.write('upload_file is OK')



if __name__ == "__main__":

    far_list = ["DRF4002J001", "DRF4005J001", "DRF4006J001"]
    uplist = ['D', 'E', 'F']
    if not os.path.exists('logs/bj/dsupok.bj'):
        file_down(far_list=far_list)
        file_converted()
        upload_yun(uplist)
    else:
        print("文件已经上传！")
        sys.exit(0)
    
    

