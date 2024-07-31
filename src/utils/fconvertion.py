import os.path
import pandas as pd
from datetime import datetime, timedelta
import os


def txt_to_csv(input_path, output_dir, mapping:dict):
    # 提取文件名中信息
    file_name = input_path.split('/')[-1]
    start_time_str = file_name.split('-')[2][:8]  # '20240724'
    drmno = file_name.split('-')[1][:7]
    farno = mapping.get(drmno) 
    start_time = datetime.strptime(start_time_str, '%Y%m%d') + timedelta(days=1)

    # 读取 txt 文件，逐行读取并过滤掉非数据行
    data = []
    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip() and not line.startswith('<'):
                data.append(line.strip().split('\t'))

    # 转换为 DataFrame
    columns = data[0]
    df = pd.DataFrame(data[1:], columns=columns)

    # 将时间列转换为 datetime 对象
    df['times'] = pd.to_datetime(df['times'], format='%Y-%m-%d_%H:%M:%S', errors='coerce')

    # 过滤掉无效时间行
    df = df.dropna(subset=['times'])

    # 选择从 start_time 开始的10天数据
    end_time = start_time + timedelta(days=10)
    df_filtered = df[(df['times'] >= start_time) & (df['times'] < end_time)]

    # 将时间格式修改为 'yyyy-MM-dd HH:mm:ss'
    df_filtered['times'] = df_filtered['times'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # 创建与模板相同的 DataFrame
    output_df = pd.DataFrame()
    output_df["time"] = df_filtered['times']
    output_df["PRED_DQ"] = df_filtered['prepower'].astype(float).round(3)  # 保留三位小数

    out_file_name = farno + "_DQ_" + start_time.strftime("%Y%m%d") + ".csv"

    if os.path.exists(output_dir)==False:
        os.makedirs(output_dir)
    outpath = os.path.join(output_dir, out_file_name)
    # 保存为 csv 文件
    output_df.to_csv(outpath, index=False, encoding='utf-8')



if __name__ == "__main__":
    from config_loader import load_config

    # 读取文件路径
    txt_file_path = 'data/raw/conv_temp/'
    output_dir = 'data/output/dasai'
    # 创建一个编号对应字典
    mapping = {"DRF3999": 'A', "DRF4000": 'B', "DRF4001": 'C',
               "DRF4002": 'D', "DRF4005": 'E', "DRF4006": 'F'}
    
    files = os.listdir(txt_file_path)
    for f in files:
        input_path = os.path.join(txt_file_path, f).replace("\\",'/')
        print(input_path)
        # txt_to_csv(input_path, mapping)
