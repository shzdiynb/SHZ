# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import json

db_uri = 'mysql+pymysql://root:123||mysql66@106.54.225.159:3306/ZCMU'
engine = create_engine(db_uri)
Base = declarative_base()  # 声明基类
Session = sessionmaker(bind=engine)  # 创建 sessionmaker 并绑定 engine
session = Session()

# 定义数据表模型
class Herbs(Base):
    __tablename__ = 'herbs'
    a = Column(String(30), primary_key=True)

# 获取数据库中的数据并生成映射
def generate_mapping():
    # 查询数据库表中的数据，按名称升序排序
    data = session.query(Herbs).order_by(Herbs.a).all()

    # 构建映射对象
    mapping = {}
    for index, row in enumerate(data):
        filename = f'file{index + 1}.html'  # 生成升序命名的文件名
        mapping[row.a] = filename  # 使用主键列 'a' 作为映射的键

    return mapping

if __name__ == '__main__':
    # 生成映射
    mapping = generate_mapping()

    # 输出映射内容
    print("const mapping = ", mapping)

    # 将映射写入文件
    output_file = os.path.join(os.getcwd(), 'mapping.js')
    with open(output_file, 'w') as f:
        f.write(f"const mapping = {json.dumps(mapping, indent=4)};\n\nmodule.exports = mapping;")

    print(f"映射对象已写入文件: {output_file}")
