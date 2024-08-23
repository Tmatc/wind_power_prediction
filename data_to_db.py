import os
from utils.CDataSetting import DataSetting
from src.data_ingestion import Dsdata2DB, DsdataClass
import time
import concurrent.futures
from functools import partial



def determine_file_type(fpath):
    if 'Meteologica' in fpath:
        return 'Meteologica'
    elif 'dsqx' in fpath:
        return 'Qx1'
    elif 'farminf' in fpath:
        return 'Farminfo'
    else:
        return fpath.split("_")[1]  # 通过文件名获取文件的类型

def process_file(dsdc, fpath):
    fpath = fpath.replace("\\", "/")
    ft = determine_file_type(fpath)
    return ft, dsdc(fpath, ft)

def dasai():
    start = time.time()
    ds = DataSetting()
    org_dir_list, type_fd, put_in_db, column_mapping = ds("dasai_dhp")
    dsdc = DsdataClass.DsdataClass(type_fd)
    ds2db = Dsdata2DB.Dsdata2DB()

    # 获取所有文件路径
    file_paths = [os.path.join(d, f).replace("\\", "/") for d in org_dir_list for f in os.listdir(d)]
    
    data_list = []
    
    # 使用多线程并行处理文件
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(partial(process_file, dsdc), file_paths))
    
    # 将结果添加到字典中
    for ft, data in results:
        data_list.append([data, ft])

    end = time.time()
    print("耗时：", end - start)
    print(len(data_list))




if __name__ == "__main__":
    dasai()
   