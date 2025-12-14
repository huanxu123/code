"""
教师端 API 路由
"""

from flask import Blueprint, request, jsonify, session
from models.models import db

teacher_bp = Blueprint('teacher', __name__)


def get_current_teacher():
    """获取当前登录的教师信息"""
    user_id = session.get('user_id')
    if not user_id:
        return None
    return db.get_teacher_by_user_id(user_id)


@teacher_bp.route('/api/teacher/profile', methods=['GET'])
def get_profile():
    """获取教师个人信息"""
    teacher = get_current_teacher()
    if not teacher:
        return jsonify({'success': False, 'message': '未登录或非教师用户'}), 401
    
    user = db.get_user_by_id(session.get('user_id'))
    
    return jsonify({
        'success': True,
        'data': {
            'name': user['name'],
            'teacher_no': teacher['teacher_no'],
            'department': teacher['department'],
            'title': teacher['title']
        }
    })


@teacher_bp.route('/api/teacher/schedule', methods=['GET'])
def get_schedule():
    """获取我的排课"""
    teacher = get_current_teacher()
    if not teacher:
        return jsonify({'success': False, 'message': '未登录或非教师用户'}), 401
    
    schedules = db.get_schedules_by_teacher(teacher['id'])
    
    weekday_names = ['', '周一', '周二', '周三', '周四', '周五', '周六', '周日']
    result = []
    for s in schedules:
        result.append({
            'id': s['id'],
            'course_name': s['course']['name'] if s['course'] else '',
            'course_code': s['course']['code'] if s['course'] else '',
            'weekday': s['weekday'],
            'weekday_name': weekday_names[s['weekday']] if s['weekday'] < len(weekday_names) else '',
            'start_period': s['start_period'],
            'end_period': s['end_period'],
            'classroom': s['classroom'],
            'weeks': s['weeks'],
            'credit': s['course']['credit'] if s['course'] else 0,
            'semester': s['semester']
        })
    
    return jsonify({'success': True, 'data': result})


@teacher_bp.route('/api/teacher/courses', methods=['GET'])
def get_courses():
    """获取我教授的课程列表"""
    teacher = get_current_teacher()
    if not teacher:
        return jsonify({'success': False, 'message': '未登录或非教师用户'}), 401
    
    result = []
    for course in db.courses:
        if course['teacher_id'] == teacher['id']:
            result.append({
                'id': course['id'],
                'code': course['code'],
                'name': course['name'],
                'credit': course['credit'],
                'hours': course['hours']
            })
    
    return jsonify({'success': True, 'data': result})


@teacher_bp.route('/api/teacher/students/<int:schedule_id>', methods=['GET'])
def get_course_students(schedule_id):
    """获取课程学生列表及成绩"""
    teacher = get_current_teacher()
    if not teacher:
        return jsonify({'success': False, 'message': '未登录或非教师用户'}), 401
    
    # 验证课程属于该教师
    schedule = db.get_schedule_by_id(schedule_id)
    if not schedule:
        return jsonify({'success': False, 'message': '课程不存在'}), 404
    
    course = db.get_course_by_id(schedule['course_id'])
    if not course or course['teacher_id'] != teacher['id']:
        return jsonify({'success': False, 'message': '无权访问该课程'}), 403
    
    students = db.get_course_students(schedule_id)
    
    result = []
    for s in students:
        result.append({
            'selection_id': s['selection_id'],
            'student_no': s['student']['student_no'] if s['student'] else '',
            'student_name': s['student_name'],
            'class_name': s['student']['class_name'] if s['student'] else '',
            'score': s['grade']['score'] if s['grade'] else None,
            'gpa': s['grade']['gpa'] if s['grade'] else None,
            'grade_status': s['grade']['status'] if s['grade'] else 'not_entered'
        })
    
    return jsonify({
        'success': True,
        'data': {
            'course': course,
            'students': result
        }
    })


@teacher_bp.route('/api/teacher/grades', methods=['POST'])
def enter_grades():
    """录入成绩"""
    teacher = get_current_teacher()
    if not teacher:
        return jsonify({'success': False, 'message': '未登录或非教师用户'}), 401
    
    data = request.get_json()
    grades_data = data.get('grades', [])
    
    if not grades_data:
        return jsonify({'success': False, 'message': '请提供成绩数据'}), 400
    
    for grade_item in grades_data:
        selection_id = grade_item.get('selection_id')
        score = grade_item.get('score')
        
        if selection_id is None or score is None:
            continue
        
        # 计算 GPA
        if score >= 90:
            gpa = 4.0
        elif score >= 85:
            gpa = 3.7
        elif score >= 80:
            gpa = 3.3
        elif score >= 75:
            gpa = 3.0
        elif score >= 70:
            gpa = 2.7
        elif score >= 65:
            gpa = 2.3
        elif score >= 60:
            gpa = 2.0
        else:
            gpa = 0.0
        
        # 查找现有成绩记录
        found = False
        for grade in db.grades:
            if grade['selection_id'] == selection_id:
                grade['score'] = score
                grade['gpa'] = gpa
                grade['status'] = 'final'
                found = True
                break
        
        # 如果没有找到，创建新记录
        if not found:
            new_id = max(g['id'] for g in db.grades) + 1 if db.grades else 1
            db.grades.append({
                'id': new_id,
                'selection_id': selection_id,
                'score': score,
                'gpa': gpa,
                'status': 'final'
            })
    
    return jsonify({'success': True, 'message': '成绩录入成功'})


@teacher_bp.route('/api/teacher/reviews', methods=['GET'])
def get_reviews():
    """获取成绩复核申请列表"""
    teacher = get_current_teacher()
    if not teacher:
        return jsonify({'success': False, 'message': '未登录或非教师用户'}), 401
    
    reviews = db.get_grade_reviews_by_teacher(teacher['id'])
    
    result = []
    for r in reviews:
        result.append({
            'id': r['id'],
            'student_name': r['student_name'],
            'course_name': r['course']['name'] if r['course'] else '',
            'original_score': r['grade']['score'] if r['grade'] else 0,
            'reason': r['reason'],
            'status': r['status'],
            'created_at': r['created_at']
        })
    
    return jsonify({'success': True, 'data': result})


@teacher_bp.route('/api/teacher/reviews/<int:review_id>', methods=['PUT'])
def process_review(review_id):
    """处理成绩复核"""
    teacher = get_current_teacher()
    if not teacher:
        return jsonify({'success': False, 'message': '未登录或非教师用户'}), 401
    
    data = request.get_json()
    action = data.get('action')  # 'approve' or 'reject'
    new_score = data.get('new_score')
    
    if action not in ['approve', 'reject']:
        return jsonify({'success': False, 'message': '无效的操作'}), 400
    
    for review in db.grade_reviews:
        if review['id'] == review_id:
            if action == 'approve' and new_score is not None:
                # 更新成绩
                for grade in db.grades:
                    if grade['id'] == review['grade_id']:
                        grade['score'] = new_score
                        # 重新计算 GPA
                        if new_score >= 90:
                            grade['gpa'] = 4.0
                        elif new_score >= 85:
                            grade['gpa'] = 3.7
                        elif new_score >= 80:
                            grade['gpa'] = 3.3
                        elif new_score >= 75:
                            grade['gpa'] = 3.0
                        elif new_score >= 70:
                            grade['gpa'] = 2.7
                        elif new_score >= 65:
                            grade['gpa'] = 2.3
                        elif new_score >= 60:
                            grade['gpa'] = 2.0
                        else:
                            grade['gpa'] = 0.0
                        break
                review['status'] = 'approved'
            else:
                review['status'] = 'rejected'
            
            return jsonify({'success': True, 'message': '复核处理完成'})
    
    return jsonify({'success': False, 'message': '复核申请不存在'}), 404


@teacher_bp.route('/api/teacher/topics', methods=['GET'])
def get_topics():
    """获取毕设课题列表"""
    teacher = get_current_teacher()
    if not teacher:
        return jsonify({'success': False, 'message': '未登录或非教师用户'}), 401
    
    topics = db.get_topics_by_teacher(teacher['id'])
    
    return jsonify({'success': True, 'data': topics})


@teacher_bp.route('/api/teacher/topics', methods=['POST'])
def create_topic():
    """创建毕设课题"""
    teacher = get_current_teacher()
    if not teacher:
        return jsonify({'success': False, 'message': '未登录或非教师用户'}), 401
    
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    max_students = data.get('max_students', 1)
    
    if not title or not description:
        return jsonify({'success': False, 'message': '请填写完整信息'}), 400
    
    new_id = max(t['id'] for t in db.graduation_topics) + 1 if db.graduation_topics else 1
    db.graduation_topics.append({
        'id': new_id,
        'teacher_id': teacher['id'],
        'title': title,
        'description': description,
        'max_students': max_students,
        'status': 'open'
    })
    
    return jsonify({'success': True, 'message': '课题创建成功'})


@teacher_bp.route('/api/teacher/topics/<int:topic_id>', methods=['PUT'])
def update_topic(topic_id):
    """更新毕设课题"""
    teacher = get_current_teacher()
    if not teacher:
        return jsonify({'success': False, 'message': '未登录或非教师用户'}), 401
    
    data = request.get_json()
    
    for topic in db.graduation_topics:
        if topic['id'] == topic_id and topic['teacher_id'] == teacher['id']:
            if 'title' in data:
                topic['title'] = data['title']
            if 'description' in data:
                topic['description'] = data['description']
            if 'max_students' in data:
                topic['max_students'] = data['max_students']
            if 'status' in data:
                topic['status'] = data['status']
            
            return jsonify({'success': True, 'message': '课题更新成功'})
    
    return jsonify({'success': False, 'message': '课题不存在或无权修改'}), 404


@teacher_bp.route('/api/teacher/topic-applications', methods=['GET'])
def get_topic_applications():
    """获取课题申请列表"""
    teacher = get_current_teacher()
    if not teacher:
        return jsonify({'success': False, 'message': '未登录或非教师用户'}), 401
    
    result = []
    for app in db.topic_applications:
        topic = db.get_topic_by_id(app['topic_id'])
        if topic and topic['teacher_id'] == teacher['id']:
            student = db.get_student_by_id(app['student_id'])
            user = db.get_user_by_id(student['user_id']) if student else None
            result.append({
                'id': app['id'],
                'topic_title': topic['title'],
                'student_name': user['name'] if user else '',
                'student_no': student['student_no'] if student else '',
                'status': app['status'],
                'created_at': app['created_at']
            })
    
    return jsonify({'success': True, 'data': result})


@teacher_bp.route('/api/teacher/topic-applications/<int:app_id>', methods=['PUT'])
def process_topic_application(app_id):
    """处理课题申请"""
    teacher = get_current_teacher()
    if not teacher:
        return jsonify({'success': False, 'message': '未登录或非教师用户'}), 401
    
    data = request.get_json()
    action = data.get('action')  # 'approve' or 'reject'
    
    if action not in ['approve', 'reject']:
        return jsonify({'success': False, 'message': '无效的操作'}), 400
    
    for app in db.topic_applications:
        if app['id'] == app_id:
            topic = db.get_topic_by_id(app['topic_id'])
            if not topic or topic['teacher_id'] != teacher['id']:
                return jsonify({'success': False, 'message': '无权处理该申请'}), 403
            
            if action == 'approve':
                app['status'] = 'approved'
                # 创建指导关系
                new_id = max(r['id'] for r in db.instructor_relations) + 1 if db.instructor_relations else 1
                db.instructor_relations.append({
                    'id': new_id,
                    'student_id': app['student_id'],
                    'teacher_id': teacher['id'],
                    'topic_id': app['topic_id'],
                    'status': 'confirmed'
                })
            else:
                app['status'] = 'rejected'
            
            return jsonify({'success': True, 'message': '申请处理完成'})
    
    return jsonify({'success': False, 'message': '申请不存在'}), 404


@teacher_bp.route('/api/teacher/students-thesis', methods=['GET'])
def get_thesis_students():
    """获取指导的学生列表"""
    teacher = get_current_teacher()
    if not teacher:
        return jsonify({'success': False, 'message': '未登录或非教师用户'}), 401
    
    students = db.get_students_by_teacher(teacher['id'])
    
    result = []
    for s in students:
        # 获取学生的过程文档
        docs = [d for d in db.process_documents if d['student_id'] == s['student']['id']] if s['student'] else []
        
        result.append({
            'student_id': s['student']['id'] if s['student'] else None,
            'student_no': s['student']['student_no'] if s['student'] else '',
            'student_name': s['student_name'],
            'topic_title': s['topic']['title'] if s['topic'] else '',
            'status': s['status'],
            'documents': docs
        })
    
    return jsonify({'success': True, 'data': result})


@teacher_bp.route('/api/teacher/exams', methods=['GET'])
def get_exams():
    """获取监考安排"""
    teacher = get_current_teacher()
    if not teacher:
        return jsonify({'success': False, 'message': '未登录或非教师用户'}), 401
    
    exams = db.get_exams_by_teacher(teacher['id'])
    
    result = []
    for e in exams:
        result.append({
            'id': e['id'],
            'course_name': e['course']['name'] if e['course'] else '',
            'course_code': e['course']['code'] if e['course'] else '',
            'date': e['exam']['date'],
            'start_time': e['exam']['start_time'],
            'end_time': e['exam']['end_time'],
            'classroom': e['exam']['classroom'],
            'role': e['role']
        })
    
    return jsonify({'success': True, 'data': result})
