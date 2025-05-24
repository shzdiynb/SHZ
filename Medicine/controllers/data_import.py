from flask import Blueprint, render_template, request, jsonify,send_from_directory
from decorators import login_required
import pandas as pd
from models import get_db_connection
import os
import pymysql

data_import_bp = Blueprint('data_import', __name__)

# UPLOAD_FOLDER = 'uploads'
UPLOAD_FOLDER = os.path.abspath('uploads')
LOADS_FOLDER = 'loads'  # 添加loads文件夹的路径
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOADS_FOLDER, exist_ok=True)  # 确保loads文件夹存在

HERBS_COLUMNS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']

# @login_required


@data_import_bp.route('/import', methods=['GET', 'POST'])
def import_data():
    if request.method == 'POST':
        print("Processing POST request")  # 打印处理POST请求的信息
        file = request.files['file']
        print("File received:", file.filename)  # 打印接收到的文件名
        if not file or not file.filename.endswith(('.xlsx', '.xls')):
            print("Invalid file type or no file selected")  # 打印无效文件类型或未选择文件的信息
            return jsonify({'status': 'error', 'message': '请上传一个合法的Excel文件'})

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            df = pd.read_excel(filepath, header=0)
            if len(df.columns) < 11:
                return jsonify({
                    'status': 'error',
                    'message': '文件格式不符，请查看文件示例',
                    'example_columns': HERBS_COLUMNS
                })

            # 读取Excel文件，跳过第一行（header=0表示第一行是列名，但实际不读取为数据）
            # df = pd.read_excel(file_path, header=0)  # header=0表示第一行作为列名但不作为数据

            # 或者明确跳过第一行（如果第一行不是列名而是无用数据）
            # df = pd.read_excel(file_path, header=None, skiprows=1)  # 跳过第一行
            conn = get_db_connection()
            cursor = conn.cursor()
            placeholders = ', '.join(['%s'] * len(HERBS_COLUMNS))
            insert_sql = f"INSERT INTO ZCMU.herbs ({', '.join(HERBS_COLUMNS)}) VALUES ({placeholders})"

            for _, row in df.iterrows():
                row_data = row.iloc[:11].tolist()
                row_data = [None if pd.isna(val) else val for val in row_data]
                cursor.execute(insert_sql, row_data)

            conn.commit()
            cursor.close()
            conn.close()

            return jsonify({'status': 'success', 'message': '数据导入成功'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'导入失败: {str(e)}'})
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    # 对于GET请求，返回导入页面（如果需要的话）
    return render_template('import_data.html')

@data_import_bp.route('/download_example')  # 添加下载示例文件的路由
def download_example():
    example_file = os.path.join(LOADS_FOLDER, 'example.xlsx')  # 示例文件的完整路径
    if not os.path.exists(example_file):
        return "示例文件不存在", 404
    return send_from_directory(directory=LOADS_FOLDER, path='example.xlsx', as_attachment=True)
