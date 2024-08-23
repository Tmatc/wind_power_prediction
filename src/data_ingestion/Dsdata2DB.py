import pymysql
import pandas as pd
from src.utils.DataBase import DataBase


class Dsdata2DB(object):
    def __init__(self):
        pass

    def datamap(self):
        '''
        将dataframe中的数据顺序与数据库表字段对应起来
        '''
        

    def insert_data_to_mysql(self, dataframe, table_name, column_mapping):
        """
        """
        # 建立数据库连接
        connection = DataBase.dbconnect()

        # 根据列名映射关系重排列 DataFrame 列顺序并重命名列名
        dataframe = dataframe.rename(columns=column_mapping)
        db_columns = list(column_mapping.values())
        dataframe = dataframe[db_columns]
        print(dataframe)
        return
        # 获取DataFrame列名
        cols = ",".join([str(i) for i in db_columns])

        # 创建插入数据的SQL模板
        placeholders = ",".join(["%s"] * len(db_columns))
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

        try:
            with connection.cursor() as cursor:
                # 将DataFrame数据转换为元组列表
                data = [tuple(x) for x in dataframe.to_numpy()]
                
                # 批量插入数据
                cursor.executemany(sql, data)
            
            # 提交事务
            connection.commit()
            print("数据插入成功")
        
        except pymysql.MySQLError as e:
            print(f"插入数据时出错: {e}")
            connection.rollback()
        
        finally:
            # 关闭数据库连接
            connection.close()

# 示例用法
if __name__ == "__main__":
    # 示例DataFrame
    data = {
        'df_col1': [1, 2, 3],
        'df_col2': ['a', 'b', 'c'],
        'df_col3': [4.5, 5.6, 6.7]
    }
    df = pd.DataFrame(data)

    # 数据库配置
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'database': 'test_db'
    }

    # 列名映射关系
    column_mapping = {
        'df_col1': 'db_col1',
        'df_col2': 'db_col2',
        'df_col3': 'db_col3'
    }

    # 插入数据
    insert_data_to_mysql(df, 'test_table', db_config, column_mapping)
