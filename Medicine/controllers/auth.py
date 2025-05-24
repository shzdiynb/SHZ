from flask import Blueprint, render_template, request, session, jsonify, url_for, redirect
from models import get_db_connection
from werkzeug.security import check_password_hash  # 用于密码哈希比较

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('logged_in'):
            return redirect(url_for('dashboard.show_dashboard'))
        return render_template('login.html')

    if not request.is_json:
        return jsonify({
            'success': False,
            'message': '请使用JSON格式提交数据',
            'error': 'invalid_content_type'
        }), 415

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            'success': False,
            'message': '用户名和密码不能为空',
            'error': 'missing_fields'
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 查询用户，同时检查权限为2
        cursor.execute("""
            SELECT id, name, password_hash, permission 
            FROM user 
            WHERE name = %s AND permission = 2
        """, (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password_hash'], password):
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = user['id']
            return jsonify({
                'success': True,
                'message': '登录成功',
                'redirect': url_for('dashboard.show_dashboard'),
                'user': {
                    'id': user['id'],
                    'username': user['name']  # 注意字段名是 name 不是 username
                }
            })
        else:
            # 更详细的错误处理
            if not user:
                # 用户名不存在或权限不足
                cursor.execute("SELECT id FROM user WHERE name = %s", (username,))
                if not cursor.fetchone():
                    return jsonify({
                        'success': False,
                        'message': '用户名不存在',
                        'error': 'username_not_found'
                    }), 401
                else:
                    return jsonify({
                        'success': False,
                        'message': '用户权限不足，无法登录',
                        'error': 'insufficient_permissions'
                    }), 401
            else:
                # 密码不正确
                return jsonify({
                    'success': False,
                    'message': '密码错误',
                    'error': 'invalid_password'
                }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '登录时发生错误',
            'error': str(e)
        }), 500
    finally:
        cursor.close()
        conn.close()

@auth_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))