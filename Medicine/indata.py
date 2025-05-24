import pandas as pd
import mysql.connector

# 读取Excel文件
def read_excel_file(file_path, sheet_name):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

# 连接到MySQL数据库
def connect_to_mysql(host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# 将数据写入MySQL数据库
def insert_data_to_mysql(conn, df, table_name):
    try:
        cursor = conn.cursor()

        # 处理NaN值
        df.fillna(value="暂未收集", inplace=True)

        # 执行插入操作
        for i, row in df.iterrows():
            sql = f"INSERT INTO {table_name} (`中药名`, `拼音`,`拉丁名`,`科目所属`,`产地`,`采摘时间`,`性状`,`性质`,`气味`,`功效`,`归经`) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s)"
            values = (row['中药名'], row['拼音'],row['拉丁名'],row['科目所属'],row['产地'],row['采摘时间'],row['性状'],row['性质'],row['气味'],row['功效'],row['归经'])
            cursor.execute(sql, values)

        conn.commit()
        print("Data inserted successfully into MySQL")
    except mysql.connector.Error as e:
        print(f"Error inserting data into MySQL: {e}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

if __name__ == "__main__":
    # Excel文件路径和表单名称
    excel_file = '中药.xlsx'
    excel_sheet = 'Sheet1'

    # MySQL数据库连接信息
    mysql_host = '106.54.225.159'
    mysql_user = 'root'
    mysql_password = '123||mysql66'
    mysql_database = 'ZCMU'

    # 表名
    mysql_table = 'herbs'

    # 读取Excel数据
    data = read_excel_file(excel_file, excel_sheet)

    if data is not None:
        # 连接到MySQL数据库
        conn = connect_to_mysql(mysql_host, mysql_user, mysql_password, mysql_database)

        if conn is not None:
            # 将数据插入MySQL数据库
            insert_data_to_mysql(conn, data, mysql_table)

            # 关闭数据库连接
            conn.close()
        else:
            print("Failed to connect to MySQL.")
    else:
        print("Failed to read Excel data.")
