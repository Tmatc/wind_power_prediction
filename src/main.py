import logging
from src.utils.config_loader import load_config
from src.data_ingestion.ingest_data import ingest_data

def main():
    # 加载配置
    config = load_config("config/database.yml")
    
    # 设置日志
    logging.config.fileConfig("config/logging.yml")
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("数据获取与入库开始")
        data_file_path = 'data/raw/wind_data.xlsx'  # 你可以更改为你的数据文件路径
        ingest_data(data_file_path, config)
        logger.info("数据获取与入库完成")
        
        # 这里可以继续调用其他模块，例如数据预处理、特征工程等
        
    except Exception as e:
        logger.error("执行过程中发生错误: %s", str(e))
        raise

if __name__ == "__main__":
    main()
