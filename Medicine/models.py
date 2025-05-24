import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def get_db_config():
    """获取数据库配置"""
    # return {
    #     'host': os.getenv('DB_HOST', 'localhost'),
    #     'user': os.getenv('DB_USER', 'root'),
    #     'password': os.getenv('DB_PASSWORD', '123456'),
    #     'database': os.getenv('DB_NAME', 'admin_system')
    # }

    return {
        'host': os.getenv('DB_HOST', '106.54.225.159'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', '123||mysql66'),
        'database': os.getenv('DB_NAME', 'ZCMU')
    }


def get_db_connection():
    """获取数据库连接"""
    config = get_db_config()
    try:
        conn = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            autocommit=True
        )
        return conn
    except Error as e:
        print(f"连接数据库失败: {e}")
        raise