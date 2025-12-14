"""
学生端 API 路由
"""

from flask import Blueprint, request, jsonify, session
from models.models import db

student_bp = Blueprint('student', __name__)


def get_current_student():
    """获取当前登录的学生信息"""
    user_id = session.get('user_id')
    if not user_id:
        return None
    return db.get_student_by_user_id(user_id)


@student_bp.route('/api/student/profile', methods=['GET'])
def get_profile():
    """获取个人信息与学籍状态"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    user = db.get_user_by_id(session.get('user_id'))
    
    return jsonify({
        'success': True,
        'data': {
            'name': user['name'],
            'student_no': student['student_no'],
            'class_name': student['class_name'],
            'major': student['major'],
            'grade': student['grade'],
            'status': student['status'],
            'status_text': {
                'normal': '正常',
                'suspended': '休学',
                'graduated': '已毕业',
                'withdrawn': '退学'
            }.get(student['status'], student['status'])
        }
    })


@student_bp.route('/api/student/schedule', methods=['GET'])
def get_schedule():
    """获取学期课表"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    schedules = db.get_schedules_by_student(student['id'])
    
    # 转换为课表格式
    weekday_names = ['', '周一', '周二', '周三', '周四', '周五', '周六', '周日']
    result = []
    for s in schedules:
        result.append({
            'id': s['id'],
            'course_name': s['course']['name'] if s['course'] else '',
            'course_code': s['course']['code'] if s['course'] else '',
            'teacher_name': s['teacher_name'],
            'weekday': s['weekday'],
            'weekday_name': weekday_names[s['weekday']] if s['weekday'] < len(weekday_names) else '',
            'start_period': s['start_period'],
            'end_period': s['end_period'],
            'classroom': s['classroom'],
            'weeks': s['weeks'],
            'credit': s['course']['credit'] if s['course'] else 0
        })
    
    return jsonify({'success': True, 'data': result})


@student_bp.route('/api/student/courses', methods=['GET'])
def get_available_courses():
    """获取可选课程列表"""
    semester = request.args.get('semester', '2024-2025-1')
    
    courses = db.get_available_courses(semester)
    
    result = []
    for c in courses:
        result.append({
            'schedule_id': c['id'],
            'course_id': c['course']['id'] if c['course'] else '',
            'course_name': c['course']['name'] if c['course'] else '',
            'course_code': c['course']['code'] if c['course'] else '',
            'credit': c['course']['credit'] if c['course'] else 0,
            'hours': c['course']['hours'] if c['course'] else 0,
            'teacher_name': c['teacher_name'],
            'weekday': c['weekday'],
            'start_period': c['start_period'],
            'end_period': c['end_period'],
            'classroom': c['classroom'],
            'weeks': c['weeks']
        })
    
    return jsonify({'success': True, 'data': result})


@student_bp.route('/api/student/select-course', methods=['POST'])
def select_course():
    """选课"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    data = request.get_json()
    schedule_id = data.get('schedule_id')
    
    if not schedule_id:
        return jsonify({'success': False, 'message': '请选择课程'}), 400
    
    # 检查是否已选
    for selection in db.course_selections:
        if selection['student_id'] == student['id'] and selection['schedule_id'] == schedule_id:
            return jsonify({'success': False, 'message': '已选择该课程'}), 400
    
    # 添加选课记录
    new_id = max(s['id'] for s in db.course_selections) + 1
    db.course_selections.append({
        'id': new_id,
        'student_id': student['id'],
        'schedule_id': schedule_id,
        'status': 'confirmed',
        'selected_at': '2024-12-14'
    })
    
    return jsonify({'success': True, 'message': '选课成功'})


@student_bp.route('/api/student/drop-course', methods=['POST'])
def drop_course():
    """退课"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    data = request.get_json()
    schedule_id = data.get('schedule_id')
    
    for i, selection in enumerate(db.course_selections):
        if selection['student_id'] == student['id'] and selection['schedule_id'] == schedule_id:
            db.course_selections.pop(i)
            return jsonify({'success': True, 'message': '退课成功'})
    
    return jsonify({'success': False, 'message': '未找到选课记录'}), 404


@student_bp.route('/api/student/grades', methods=['GET'])
def get_grades():
    """获取成绩列表"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    grades = db.get_grades_by_student(student['id'])
    
    result = []
    for g in grades:
        result.append({
            'id': g['id'],
            'course_name': g['course']['name'] if g['course'] else '',
            'course_code': g['course']['code'] if g['course'] else '',
            'credit': g['course']['credit'] if g['course'] else 0,
            'score': g['score'],
            'gpa': g['gpa'],
            'semester': g['semester'],
            'status': g['status']
        })
    
    # 计算平均绩点
    if result:
        total_credits = sum(g['credit'] for g in result)
        total_gpa_points = sum(g['credit'] * g['gpa'] for g in result)
        avg_gpa = round(total_gpa_points / total_credits, 2) if total_credits > 0 else 0
    else:
        avg_gpa = 0
        total_credits = 0
    
    return jsonify({
        'success': True,
        'data': {
            'grades': result,
            'summary': {
                'total_credits': total_credits,
                'avg_gpa': avg_gpa
            }
        }
    })


@student_bp.route('/api/student/grade-review', methods=['POST'])
def submit_grade_review():
    """提交成绩复核申请"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    data = request.get_json()
    grade_id = data.get('grade_id')
    reason = data.get('reason')
    
    if not grade_id or not reason:
        return jsonify({'success': False, 'message': '请填写完整信息'}), 400
    
    # 检查是否已申请
    for review in db.grade_reviews:
        if review['grade_id'] == grade_id and review['status'] == 'pending':
            return jsonify({'success': False, 'message': '该成绩已有待处理的复核申请'}), 400
    
    new_id = max(r['id'] for r in db.grade_reviews) + 1 if db.grade_reviews else 1
    db.grade_reviews.append({
        'id': new_id,
        'grade_id': grade_id,
        'student_id': student['id'],
        'reason': reason,
        'status': 'pending',
        'created_at': '2024-12-14'
    })
    
    return jsonify({'success': True, 'message': '复核申请已提交'})


@student_bp.route('/api/student/evaluations', methods=['GET'])
def get_evaluations():
    """获取未完成评教列表"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    evaluations = db.get_pending_evaluations(student['id'])
    
    result = []
    for e in evaluations:
        result.append({
            'id': e['id'],
            'course_name': e['course']['name'] if e['course'] else '',
            'course_code': e['course']['code'] if e['course'] else '',
            'teacher_name': e['teacher_name'],
            'status': e['status']
        })
    
    return jsonify({'success': True, 'data': result})


@student_bp.route('/api/student/evaluate', methods=['POST'])
def submit_evaluation():
    """提交评教"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    data = request.get_json()
    evaluation_id = data.get('evaluation_id')
    rating = data.get('rating')
    comment = data.get('comment', '')
    
    if not evaluation_id or not rating:
        return jsonify({'success': False, 'message': '请填写评分'}), 400
    
    for evaluation in db.evaluations:
        if evaluation['id'] == evaluation_id:
            evaluation['rating'] = rating
            evaluation['comment'] = comment
            evaluation['status'] = 'completed'
            return jsonify({'success': True, 'message': '评教提交成功'})
    
    return jsonify({'success': False, 'message': '评教记录不存在'}), 404


@student_bp.route('/api/student/status-changes', methods=['GET'])
def get_status_changes():
    """获取学籍异动申请列表"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    result = []
    for item in db.status_changes:
        if item['student_id'] == student['id']:
            result.append({
                'id': item['id'],
                'type': item['type'],
                'reason': item['reason'],
                'status': item['status'],
                'status_text': {
                    'pending': '待审批',
                    'approved': '已通过',
                    'rejected': '已拒绝'
                }.get(item['status'], item['status']),
                'created_at': item['created_at']
            })
    
    return jsonify({'success': True, 'data': result})


@student_bp.route('/api/student/status-changes', methods=['POST'])
def submit_status_change():
    """提交学籍异动申请"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    data = request.get_json()
    change_type = data.get('type')
    reason = data.get('reason')
    
    if not change_type or not reason:
        return jsonify({'success': False, 'message': '请填写完整信息'}), 400
    
    new_id = max(s['id'] for s in db.status_changes) + 1 if db.status_changes else 1
    db.status_changes.append({
        'id': new_id,
        'student_id': student['id'],
        'type': change_type,
        'reason': reason,
        'status': 'pending',
        'created_at': '2024-12-14'
    })
    
    return jsonify({'success': True, 'message': '申请已提交'})


@student_bp.route('/api/student/retakes', methods=['GET'])
def get_retakes():
    """获取重修申请列表"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    result = []
    for item in db.retake_applications:
        if item['student_id'] == student['id']:
            course = db.get_course_by_id(item['course_id'])
            result.append({
                'id': item['id'],
                'course_name': course['name'] if course else '',
                'course_code': course['code'] if course else '',
                'reason': item['reason'],
                'status': item['status'],
                'status_text': {
                    'pending': '待审批',
                    'approved': '已通过',
                    'rejected': '已拒绝'
                }.get(item['status'], item['status']),
                'created_at': item['created_at']
            })
    
    return jsonify({'success': True, 'data': result})


@student_bp.route('/api/student/retakes', methods=['POST'])
def submit_retake():
    """提交重修申请"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    data = request.get_json()
    course_id = data.get('course_id')
    reason = data.get('reason')
    
    if not course_id or not reason:
        return jsonify({'success': False, 'message': '请填写完整信息'}), 400
    
    new_id = max(r['id'] for r in db.retake_applications) + 1 if db.retake_applications else 1
    db.retake_applications.append({
        'id': new_id,
        'student_id': student['id'],
        'course_id': course_id,
        'reason': reason,
        'status': 'pending',
        'created_at': '2024-12-14'
    })
    
    return jsonify({'success': True, 'message': '重修申请已提交'})


@student_bp.route('/api/student/topics', methods=['GET'])
def get_topics():
    """获取毕设课题列表"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    result = []
    for topic in db.graduation_topics:
        if topic['status'] == 'open':
            teacher = db.get_teacher_by_id(topic['teacher_id'])
            teacher_user = db.get_user_by_id(teacher['user_id']) if teacher else None
            
            # 检查是否已申请
            applied = any(app['student_id'] == student['id'] and app['topic_id'] == topic['id'] 
                         for app in db.topic_applications)
            
            result.append({
                'id': topic['id'],
                'title': topic['title'],
                'description': topic['description'],
                'teacher_name': teacher_user['name'] if teacher_user else '',
                'department': teacher['department'] if teacher else '',
                'max_students': topic['max_students'],
                'applied': applied
            })
    
    return jsonify({'success': True, 'data': result})


@student_bp.route('/api/student/apply-topic', methods=['POST'])
def apply_topic():
    """申请毕设课题"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    data = request.get_json()
    topic_id = data.get('topic_id')
    
    if not topic_id:
        return jsonify({'success': False, 'message': '请选择课题'}), 400
    
    # 检查是否已申请
    for app in db.topic_applications:
        if app['student_id'] == student['id'] and app['topic_id'] == topic_id:
            return jsonify({'success': False, 'message': '已申请该课题'}), 400
    
    new_id = max(a['id'] for a in db.topic_applications) + 1 if db.topic_applications else 1
    db.topic_applications.append({
        'id': new_id,
        'student_id': student['id'],
        'topic_id': topic_id,
        'status': 'pending',
        'created_at': '2024-12-14'
    })
    
    return jsonify({'success': True, 'message': '课题申请已提交'})


@student_bp.route('/api/student/my-topic', methods=['GET'])
def get_my_topic():
    """获取我的毕设课题"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    # 查找已确认的指导关系
    for relation in db.instructor_relations:
        if relation['student_id'] == student['id']:
            topic = db.get_topic_by_id(relation['topic_id'])
            teacher = db.get_teacher_by_id(relation['teacher_id'])
            teacher_user = db.get_user_by_id(teacher['user_id']) if teacher else None
            
            return jsonify({
                'success': True,
                'data': {
                    'topic': topic,
                    'teacher_name': teacher_user['name'] if teacher_user else '',
                    'status': relation['status']
                }
            })
    
    # 查找待审批的申请
    for app in db.topic_applications:
        if app['student_id'] == student['id'] and app['status'] == 'pending':
            topic = db.get_topic_by_id(app['topic_id'])
            teacher = db.get_teacher_by_id(topic['teacher_id']) if topic else None
            teacher_user = db.get_user_by_id(teacher['user_id']) if teacher else None
            
            return jsonify({
                'success': True,
                'data': {
                    'topic': topic,
                    'teacher_name': teacher_user['name'] if teacher_user else '',
                    'status': 'pending'
                }
            })
    
    return jsonify({'success': True, 'data': None})


@student_bp.route('/api/student/documents', methods=['GET'])
def get_documents():
    """获取过程文档列表"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    result = []
    for doc in db.process_documents:
        if doc['student_id'] == student['id']:
            result.append({
                'id': doc['id'],
                'type': doc['type'],
                'file_name': doc['file_name'],
                'status': doc['status'],
                'submitted_at': doc['submitted_at']
            })
    
    return jsonify({'success': True, 'data': result})


@student_bp.route('/api/student/documents', methods=['POST'])
def submit_document():
    """提交过程文档"""
    student = get_current_student()
    if not student:
        return jsonify({'success': False, 'message': '未登录或非学生用户'}), 401
    
    data = request.get_json()
    doc_type = data.get('type')
    file_name = data.get('file_name')
    
    if not doc_type or not file_name:
        return jsonify({'success': False, 'message': '请填写完整信息'}), 400
    
    new_id = max(d['id'] for d in db.process_documents) + 1 if db.process_documents else 1
    db.process_documents.append({
        'id': new_id,
        'student_id': student['id'],
        'type': doc_type,
        'file_name': file_name,
        'status': 'submitted',
        'submitted_at': '2024-12-14'
    })
    
    return jsonify({'success': True, 'message': '文档提交成功'})
