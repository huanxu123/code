"""
用户认证相关路由
"""

from flask import Blueprint, request, jsonify, session
from models.models import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': '请输入用户名和密码'}), 400
    
    user = db.get_user_by_username(username)
    
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 401
    
    if user['password'] != password:
        return jsonify({'success': False, 'message': '密码错误'}), 401
    
    # 保存用户信息到 session
    session['user_id'] = user['id']
    session['role'] = user['role']
    
    # 根据角色获取额外信息
    extra_info = {}
    if user['role'] == 'student':
        student = db.get_student_by_user_id(user['id'])
        if student:
            extra_info = {
                'student_id': student['id'],
                'student_no': student['student_no'],
                'class_name': student['class_name'],
                'major': student['major'],
                'grade': student['grade'],
                'status': student['status']
            }
    elif user['role'] == 'teacher':
        teacher = db.get_teacher_by_user_id(user['id'])
        if teacher:
            extra_info = {
                'teacher_id': teacher['id'],
                'teacher_no': teacher['teacher_no'],
                'department': teacher['department'],
                'title': teacher['title']
            }
    
    return jsonify({
        'success': True,
        'message': '登录成功',
        'data': {
            'id': user['id'],
            'username': user['username'],
            'name': user['name'],
            'role': user['role'],
            **extra_info
        }
    })


@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    """用户登出"""
    session.clear()
    return jsonify({'success': True, 'message': '已登出'})


@auth_bp.route('/api/user/info', methods=['GET'])
def get_user_info():
    """获取当前用户信息"""
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'success': False, 'message': '未登录'}), 401
    
    user = db.get_user_by_id(user_id)
    
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    
    # 根据角色获取额外信息
    extra_info = {}
    if user['role'] == 'student':
        student = db.get_student_by_user_id(user['id'])
        if student:
            extra_info = {
                'student_id': student['id'],
                'student_no': student['student_no'],
                'class_name': student['class_name'],
                'major': student['major'],
                'grade': student['grade'],
                'status': student['status']
            }
    elif user['role'] == 'teacher':
        teacher = db.get_teacher_by_user_id(user['id'])
        if teacher:
            extra_info = {
                'teacher_id': teacher['id'],
                'teacher_no': teacher['teacher_no'],
                'department': teacher['department'],
                'title': teacher['title']
            }
    
    return jsonify({
        'success': True,
        'data': {
            'id': user['id'],
            'username': user['username'],
            'name': user['name'],
            'role': user['role'],
            **extra_info
        }
    })
