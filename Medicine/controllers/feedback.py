from flask import Blueprint, jsonify, request, render_template
from models import get_db_connection


feedback_bp = Blueprint('feedback', __name__)

# 返回HTML页面
@feedback_bp.route('/feedback')
def feedback_page():
    return render_template('feedback.html')

# 返回JSON数据API
@feedback_bp.route('/api/feedback', methods=['GET'])
def feedback_data():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            # 根据你的截图修改了查询语句
            cursor.execute("""
                SELECT id, name AS user_name, query, qu_description AS content, 
                       email, status, created_at, updated_at
                FROM WebBoard
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))
            feedbacks = cursor.fetchall()
            print("Fetched feedbacks:", feedbacks)  # 调试输出

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
@feedback_bp.route('/api/feedback/<int:feedback_id>', methods=['PATCH'])
def update_feedback(feedback_id):
    data = request.get_json()
    new_status = data.get('status')

    if new_status not in ['pending', 'approved', 'rejected']:
        return jsonify({'success': False, 'message': '无效的状态值'}), 400

    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            # 检查反馈是否存在
            cursor.execute("SELECT id FROM WebBoard WHERE id = %s", (feedback_id,))
            if not cursor.fetchone():
                return jsonify({'success': False, 'message': '反馈不存在'}), 404

            # 更新状态
            cursor.execute("""
                UPDATE WebBoard 
                SET status = %s, updated_at = NOW() 
                WHERE id = %s
            """, (new_status, feedback_id))
            conn.commit()

            # 返回更新后的反馈
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