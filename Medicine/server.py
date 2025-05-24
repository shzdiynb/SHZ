# -*- coding: utf-8 -*-

import re
import os
from flask import Flask, request, render_template, redirect, url_for, flash , jsonify ,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import zhipuai
from flask import session
import requests
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM

app=Flask(__name__)
app.secret_key = 'your_random_secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123||mysql66@106.54.225.159:3306/ZCMU'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # 生成一个随机的 secret key
db = SQLAlchemy(app)

ZHIPU_API_KEY="3cad4d747f8c41eaa1a246ed7fddc2ac.VO91Y3jqAhcP4DyE"

# # 检查可用设备
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#
# # 加载 Qwen 模型和 tokenizer
#
# # 加载模型和 tokenizer
# model_path = '../Qwen/output_qwen'  # 替换成你训练的模型路径
# tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
# model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True).to("cuda:0").eval()

class Herb(db.Model):
    __tablename__ = 'herbs'
    a = db.Column( db.String(30),primary_key=True)
    b = db.Column(db.String(450))
    c = db.Column(db.String(450))
    d = db.Column(db.String(100))
    e = db.Column(db.Text)
    f = db.Column(db.Text)
    g = db.Column(db.Text)
    h = db.Column(db.String(450))
    i = db.Column(db.String(45))
    j = db.Column(db.Text)
    k = db.Column(db.Text)

# 获取数据库中的数据


# @app.route('/chat', methods=['POST'])
# def chat():
#     # user_input = request.json.get("message")
#     # inputs = tokenizer(user_input, return_tensors="pt").to(device)  # 确保输入数据移动到设备
#     # outputs = model.generate(inputs.input_ids, max_length=150, pad_token_id=tokenizer.eos_token_id)
    
#     # # 直接给出答案
#     # response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    
#     # return jsonify({"response": response})
#     return 0
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    permission = db.Column(db.Integer, default=1)  # ✅ 添加这个字段

    def __repr__(self):
        return '<User %r>' % self.username

# 生成从 file1 到 file402 的 Flask 路由和对应的视图函数
# 获取数据库中的数据
def get_data_from_db():
    try:
        herbs = Herb.query.order_by(Herb.a).all()
        return herbs
    except Exception as e:
        print(f"Error fetching data from database: {e}")
        return []

# Function to dynamically register routes and define view functions
def generate_flask_routes_and_functions():
    for i in range(1, 403):
        filename = f'file{i}.html'
        route_path = f'/{filename}'

        # Dynamic view function
        def view_function(filename=filename):
            herbs = get_data_from_db()
            return render_template(filename, herbs=herbs)

        # Set unique endpoint name
        endpoint = f'file{i}'

        # Add the route to the Flask app
        app.add_url_rule(route_path, endpoint, view_function, methods=['GET', 'POST'])

# 邮箱格式验证函数
def is_valid_email(email):
    if not email or len(email) > 120:
        return False
    pattern = r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
    return re.match(pattern, email)


@app.route('/',methods=['get','post'])
def index1():
    return render_template('index.html')

@app.route('/About.html',methods=['get','post'])
def About():
    return render_template('About.html')

class ChatRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120))
    question = db.Column(db.Text)
    answer = db.Column(db.Text)


@app.route("/chaxun.html")
def chaxun():
    if not session.get('logged_in'):
        flash('请先登录再访问该页面', 'warning')
        return redirect(url_for('Login'))
    return render_template("chaxun.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question")

    username = session.get('user_name')
    email = session.get('user_email')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZHIPU_API_KEY}"
    }

    payload = {
        "model": "glm-4-plus",
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            headers=headers,
            json=payload
        )
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"出错了：{str(e)}"

    # 保存聊天记录
    if username and email:
        record = ChatRecords(
            username=username,
            email=email,
            question=user_input,
            answer=reply
        )
        db.session.add(record)
        db.session.commit()

    return jsonify({"answer": reply})


UPLOAD_FOLDER = os.path.abspath('uploads')
LOADS_FOLDER = os.path.abspath('loads')  # 确保是绝对路径
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOADS_FOLDER, exist_ok=True)

HERBS_COLUMNS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']

@app.route('/import', methods=['GET', 'POST'])
def import_data():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({'flag': 'error', 'message': '请上传一个合法的Excel文件'})

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            df = pd.read_excel(filepath, header=0)
            if len(df.columns) < 11:
                return jsonify({
                    'flag': 'error',
                    'message': '文件格式不符，请查看文件示例',
                    'example_columns': HERBS_COLUMNS
                })

            conn = get_db_connection()
            cursor = conn.cursor()
            placeholders = ', '.join(['%s'] * len(HERBS_COLUMNS))
            insert_sql = f"INSERT INTO herbs ({', '.join(HERBS_COLUMNS)}) VALUES ({placeholders})"

            for _, row in df.iterrows():
                row_data = row.iloc[:11].tolist()
                row_data = [None if pd.isna(val) else val for val in row_data]
                cursor.execute(insert_sql, row_data)

            conn.commit()
            cursor.close()
            conn.close()

            return jsonify({'flag': 'success', 'message': '数据导入成功'})
        except Exception as e:
            return jsonify({'flag': 'error', 'message': f'导入失败: {str(e)}'})
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    return render_template('import_data.html')

@app.route('/download_example')
def download_example():
    example_file = os.path.join(LOADS_FOLDER, 'example.xlsx')
    if not os.path.exists(example_file):
        return "示例文件不存在", 404
    return send_from_directory(directory=LOADS_FOLDER, path='example.xlsx', as_attachment=True)


# 返回HTML页面
@app.route('/feedback')
def feedback_page():
    return render_template('feedback.html')

# 返回JSON数据API
@app.route('/api/feedback', methods=['GET'])
def feedback_data():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, name AS user_name, query, qu_description AS content, 
                       email, status, created_at, updated_at
                FROM WebBoard
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))
            feedbacks = cursor.fetchall()

            cursor.execute("SELECT COUNT(*) AS total FROM WebBoard")
            total = cursor.fetchone()['total']

    total_pages = (total + limit - 1) // limit
    return jsonify({
        'feedbacks': feedbacks,
        'total': total,
        'total_pages': total_pages,
        'current_page': page
    })

# 更新反馈状态API
@app.route('/api/feedback/<int:feedback_id>', methods=['PATCH'])
def update_feedback(feedback_id):
    data = request.get_json()
    new_flag = data.get('status')

    if new_flag not in ['pending', 'approved', 'rejected']:
        return jsonify({'success': False, 'message': '无效的状态值'}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM WebBoard WHERE id = %s", (feedback_id,))
            if not cursor.fetchone():
                return jsonify({'success': False, 'message': '反馈不存在'}), 404

            cursor.execute("""
                UPDATE WebBoard 
                SET flag = %s, updated_at = NOW() 
                WHERE id = %s
            """, (new_flag, feedback_id))
            conn.commit()

            cursor.execute("""
                SELECT id, name AS user_name, query, qu_description AS content, 
                       email, status, created_at, updated_at
                FROM WebBoard
                WHERE id = %s
            """, (feedback_id,))
            updated_feedback = cursor.fetchone()

    return jsonify({
        'success': True,
        'message': '状态更新成功',
        'feedback': updated_feedback
    })

@app.route('/shanyao.html',methods=['get','post'])
def shanyao():
    herbs = get_data_from_db()
    return render_template('shanyao.html',herbs=herbs)

# @app.route('/file1.html',methods=['get','post'])
# def file1():
#     herbs = get_data_from_db()
#     return render_template('file1.html',herbs=herbs)


@app.route('/Blog-Grid.html',methods=['get','post'])
def BlogGrid():
    return render_template('Blog-Grid.html')

@app.route('/Blog-List.html',methods=['get','post'])
def BlogList():
    return render_template('Blog-List.html')

@app.route('/Blog-Single.html',methods=['get','post'])
def BlogSingle():
    return render_template('Blog-Single.html')

@app.route('/Career-Single.html',methods=['get','post'])
def CareerSingle():
    return render_template('Career-Single.html')

@app.route('/Career.html',methods=['get','post'])
def Career():
    return render_template('Career.html')

@app.route('/Cart.html',methods=['get','post'])
def Cart():
    return render_template('Cart.html')

@app.route('/Checkout.html',methods=['get','post'])
def Checkout():
    return render_template('Checkout.html')

# 数据库连接配置
db_config = {
    'host': '106.54.225.159',
    'user': 'root',         # 替换为你的用户名
    'password': '123||mysql66',   # 替换为你的密码
    'database': 'ZCMU'  # 替换为你的数据库名
}

@app.route('/Contact.html',methods=['get','post'])
def Contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()
            sql = "INSERT INTO WebBoard (name, query, qu_description, email) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, subject, message, email))
            conn.commit()
            flash('反馈成功！', 'success')
        except Exception as e:
            flash(f'提交失败: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
    return render_template('Contact.html')

@app.route('/Faqs.html',methods=['get','post'])
def Faqs():
    return render_template('Faqs.html')

@app.route('/Gallery.html',methods=['get','post'])
def Gallery():
    return render_template('Gallery.html')

@app.route('/Login.html', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['logged_in'] = True
            session['user_email'] = user.email
            session['user_name'] = user.name
            session['user_permission'] = user.permission
            flash('登录成功！', 'success')

            if user.permission == 1:
                return redirect(url_for('chaxun'))
            elif user.permission == 2:
                return redirect(url_for('base'))
            else:
                flash('未知权限，请联系管理员。', 'error')
                return redirect(url_for('Login'))
        else:
            flash('邮箱或密码错误，请重试。', 'error')
            return redirect(url_for('Login'))

    # ✅ 如果是 GET 请求，就返回登录页面
    return render_template('Login.html')


@app.route('/Partners.html',methods=['get','post'])
def Partners():
    return render_template('Partners.html')

@app.route('/Pricing.html',methods=['get','post'])
def Pricing():
    return render_template('Pricing.html')

@app.route('/Process.html',methods=['get','post'])
def Process():
    return render_template('Process.html')

@app.route('/Product-Single.html',methods=['get','post'])
def ProductSingle():
    return render_template('ProductSingle.html')

@app.route('/Project-Single.html',methods=['get','post'])
def ProjectSingle():
    return render_template('Project-Single.html')

@app.route('/Projects.html',methods=['get','post'])
def Projects():
    return render_template('Projects.html')

from werkzeug.security import generate_password_hash
import re

# 判断邮箱格式是否有效
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.route('/Register.html', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # 1. 检查邮箱格式
        if not is_valid_email(email):
            flash('请输入有效的邮箱地址。', 'error')
            return redirect(url_for('Register'))

        # 2. 检查用户名或邮箱是否已存在
        existing_user = User.query.filter(
            (User.name == username) | (User.email == email)
        ).first()

        if existing_user:
            flash('用户名或邮箱已存在，请更换后再试。', 'error')
            return redirect(url_for('Register'))

        # 3. 使用 Werkzeug 生成密码哈希（✅ 正确的方式）
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # 4. 创建新用户并默认权限为 1
        new_user = User(name=username, email=email, password_hash=hashed_password, permission=1)

        # 5. 插入数据库
        db.session.add(new_user)
        db.session.commit()

        flash('注册成功，请登录。', 'success')
        return redirect(url_for('Login'))

    # 处理 GET 请求
    return render_template('Register.html')

def get_db_connection():
    return pymysql.connect(
        host='106.54.225.159',
        user='root',
        password='123||mysql66',
        database='ZCMU',
        cursorclass=pymysql.cursors.DictCursor,  # 让 cursor 返回字典类型
        charset='utf8mb4'
    )

@app.route('/chat', methods=['get','post'])
def chat_page():
    return render_template('chat.html')

@app.route('/api/chat', methods=['get','post'])
def chat_data():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT cr.id, cr.username, cr.email, cr.question, cr.answer, cr.flag, u.permission
                FROM chat_records cr
                LEFT JOIN user u ON cr.email = u.email
                ORDER BY cr.id DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))
            chat_records = cursor.fetchall()

            cursor.execute("SELECT COUNT(*) AS total FROM chat_records")
            total = cursor.fetchone()['total']

    total_pages = (total + limit - 1) // limit
    return jsonify({
        'chats': chat_records,
        'total': total,
        'total_pages': total_pages,
        'current_page': page
    })

@app.route('/api/chat/<int:chat_id>', methods=['PATCH'])
def update_chat(chat_id):
    data = request.get_json()
    new_answer = data.get('answer')
    if not new_answer:
        return jsonify({'success': False, 'message': '没有提供新的回答'}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM chat_records WHERE id = %s", (chat_id,))
            if not cursor.fetchone():
                return jsonify({'success': False, 'message': '聊天记录不存在'}), 404

            cursor.execute("""
                UPDATE chat_records 
                SET answer = %s, flag = 1
                WHERE id = %s
            """, (new_answer, chat_id))
            conn.commit()

            cursor.execute("""
                SELECT id, username, email, question, answer, flag
                FROM chat_records
                WHERE id = %s
            """, (chat_id,))
            updated_chat = cursor.fetchone()

    return jsonify({
        'success': True,
        'message': '聊天记录更新成功',
        'chat_record': updated_chat
    })

@app.route('/chatreview', methods=['post','get'])
def chat_review():
    updated_count = 0
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, question, flag FROM chat_records WHERE flag IS NULL OR flag = ''")
            rows = cursor.fetchall()

            field_names = [desc[0] for desc in cursor.description]
            questions = [dict(zip(field_names, row)) for row in rows]

            for q in questions:
                risk_score = check_question_risk(q['question'])  # 传问题内容
                if risk_score is None:
                    continue
                flag = 'warning!' if risk_score > 0.9 else 'accept!'
                cursor.execute(
                    "UPDATE chat_records SET flag = %s WHERE id = %s",
                    (flag, q['id'])
                )
                updated_count += 1

        conn.commit()
        conn.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': f'审核完成，共更新 {updated_count} 条记录'})

# def check_question_risk(question):
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {ZHIPU_API_KEY}"
#     }
#     prompt = (
#         f"请判断以下用户问题的安全风险，输出一个0到1之间的数字表示危险系数，仅输出数字，不要多余文字：\n"
#         f"问题：{question}\n"
#         f"危险系数："
#     )
#     payload = {
#         "model": "glm-4-plus",
#         "messages": [
#             {"role": "user", "content": prompt}
#         ]
#     }
#     try:
#         response = requests.post(
#             "https://open.bigmodel.cn/api/paas/v4/model/chat/completions",
#             headers=headers,
#             json=payload,
#             verify=False,
#             timeout=10  # 设置超时时间
#         )

#         if response.status_code != 200:
#             print(f"智谱API请求失败，状态码: {response.status_code}，响应内容: {response.text}")
#             return None

#         result = response.json()
#         # 打印完整返回方便调试
#         print("智谱API返回结果:", result)

#         # 提取回复内容
#         reply = result["choices"][0]["message"]["content"].strip()
#         return float(reply)
#     except requests.exceptions.RequestException as e:
#         print(f"网络请求异常: {e}")
#         return None
#     except (KeyError, IndexError, ValueError) as e:
#         print(f"解析返回数据异常: {e}，返回内容: {result}")
#         return None

def check_question_risk(question):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZHIPU_API_KEY}"
    }
    # 确认URL正确
    api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    prompt = f"请判断以下用户问题的安全风险，输出0到1之间的数字，仅输出数字：\n问题：{question}\n危险系数："
    
    payload = {
        "model": "glm-4",  # 确认模型名称有效（如glm-4）
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()  # 触发HTTP错误
        result = response.json()
        reply = result["choices"][0]["message"]["content"].strip()
        return float(reply)
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {str(e)}")
    except KeyError as e:
        print(f"解析响应字段错误: {str(e)}")
    except ValueError as e:
        print(f"返回值非数字: {str(e)}")
    return None



@app.route('/Request-Quote.html',methods=['get','post'])
def RequestQuote():
    return render_template('Request-Quote.html')

@app.route('/Reset-Password.html',methods=['get','post'])
def ResetPassword():
    return render_template('Reset-Password.html')


@app.route('/Service-Single.html',methods=['get','post'])
def ServiceSingle():
    return render_template('Service-Single.html')

@app.route('/Services.html',methods=['get','post'])
def Service():
    return render_template('Services.html')

@app.route('/Shop-Grid.html',methods=['get','post'])
def ShopGrid():
    return render_template('Shop-Grid.html')

@app.route('/Shop-List.html',methods=['get','post'])
def ShopList():
    return render_template('Shop-List.html')

@app.route('/Team-Single.html',methods=['get','post'])
def TeamSingle():
    return render_template('Team-Single.html')

@app.route('/Team.html',methods=['get','post'])
def Team():
    return render_template('Team.html')

@app.route('/Testimonials.html',methods=['get','post'])
def Testimonials():
    return render_template('Testimonials.html')

@app.route('/Wishlist.html',methods=['get','post'])
def Wishlist():
    return render_template('Wishlist.html')

@app.route('/base',methods=['get','post'])
def base():
    return render_template('base.html')


@app.route('/dashboard',methods=['get','post'])
def show_dashboard():
    return render_template('dashboard.html', username=session.get('user_id'))

@app.route('/index.html',methods=['get','post'])
def index():
    return render_template('index.html')

    
if __name__ == '__main__':
    generate_flask_routes_and_functions()

    app.run(host='0.0.0.0', port=8080, debug=True)