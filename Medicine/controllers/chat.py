from flask import Blueprint, jsonify, request, render_template
from models import get_db_connection

chat_bp = Blueprint('chat', __name__)

# 返回HTML页面
@chat_bp.route('/chat')
def chat_page():
    return render_template('chat.html')

# 返回JSON数据API
@chat_bp.route('/api/chat', methods=['GET'])
def chat_data():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    with get_db_connection() as conn:
        # with conn.cursor(dictionary=True) as cursor:
        #     # 使用正确的表名 chat_records
        #     cursor.execute("""
        #         SELECT id, username, email, question, answer, flag
        #         FROM chat_records
        #         ORDER BY id DESC  -- 按ID降序排列
        #         LIMIT %s OFFSET %s
        #     """, (limit, offset))
        #     chat_records = cursor.fetchall()
        with conn.cursor(dictionary=True) as cursor:
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
        # 'chat_records': chat_records,
        'chats': chat_records,
        'total': total,
        'total_pages': total_pages,
        'current_page': page
    })

# 更新聊天记录API
@chat_bp.route('/api/chat/<int:chat_id>', methods=['PATCH'])
def update_chat(chat_id):
    data = request.get_json()
    # 示例：更新answer字段
    new_answer = data.get('answer')
    if not new_answer:
        return jsonify({'success': False, 'message': '没有提供新的回答'}), 400

    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id FROM chat_records WHERE id = %s", (chat_id,))
            if not cursor.fetchone():
                return jsonify({'success': False, 'message': '聊天记录不存在'}), 404

            cursor.execute("""
                UPDATE chat_records 
                SET answer = %s, flag = 1  -- 更新answer并设置flag为1
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