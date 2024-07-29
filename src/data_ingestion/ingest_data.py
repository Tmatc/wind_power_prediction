import os
import pandas as pd
import pymysql
import logging
from src.utils.config_loader import load_config

def connect_to_database(config):
    db_config = config['database']
    connection = pymysql.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        db=db_config['dbname'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def ingest_data(file_path, config):
    # 检查文件类型
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == '.csv':
        data = pd.read_csv(file_path)
    elif file_extension.lower() == '.xlsx':
        data = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format: {}".format(file_extension))
    
    # 数据库连接
    connection = connect_to_database(config)
    
    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows():
                sql = """
                INSERT INTO wind_data (date, wind_speed, power_output)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (row['date'], row['wind_speed'], row['power_output']))
        
        connection.commit()
    finally:
        connection.close()
    
    logging.info("Data ingestion completed successfully.")

# 加载配置和执行数据入库
if __name__ == "__main__":
    config_path = 'config/database.yml'
    data_file_path = 'data/raw/wind_data.xlsx'  # 你可以更改为你的数据文件路径
    config = load_config(config_path)
    
    logging.basicConfig(level=logging.INFO)
    ingest_data(data_file_path, config)
