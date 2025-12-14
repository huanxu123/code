"""
教务端 API 路由
"""

from flask import Blueprint, request, jsonify, session
from models.models import db

admin_bp = Blueprint('admin', __name__)


def check_admin():
    """检查是否为管理员"""
    role = session.get('role')
    return role == 'admin'


# ==================== 学生管理 ====================

@admin_bp.route('/api/admin/students', methods=['GET'])
def get_students():
    """获取学生列表"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    result = []
    for student in db.students:
        user = db.get_user_by_id(student['user_id'])
        result.append({
            'id': student['id'],
            'user_id': student['user_id'],
            'name': user['name'] if user else '',
            'student_no': student['student_no'],
            'class_name': student['class_name'],
            'major': student['major'],
            'grade': student['grade'],
            'status': student['status']
        })
    
    return jsonify({'success': True, 'data': result})


@admin_bp.route('/api/admin/students', methods=['POST'])
def create_student():
    """创建学生"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    data = request.get_json()
    
    # 创建用户
    new_user_id = max(u['id'] for u in db.users) + 1
    db.users.append({
        'id': new_user_id,
        'username': data.get('username', data.get('student_no')),
        'password': data.get('password', '123456'),
        'role': 'student',
        'name': data.get('name')
    })
    
    # 创建学生
    new_student_id = max(s['id'] for s in db.students) + 1
    db.students.append({
        'id': new_student_id,
        'user_id': new_user_id,
        'student_no': data.get('student_no'),
        'class_name': data.get('class_name'),
        'major': data.get('major'),
        'grade': data.get('grade'),
        'status': 'normal'
    })
    
    return jsonify({'success': True, 'message': '学生创建成功'})


@admin_bp.route('/api/admin/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """更新学生信息"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    data = request.get_json()
    
    for student in db.students:
        if student['id'] == student_id:
            if 'class_name' in data:
                student['class_name'] = data['class_name']
            if 'major' in data:
                student['major'] = data['major']
            if 'status' in data:
                student['status'] = data['status']
            
            # 更新用户名
            if 'name' in data:
                user = db.get_user_by_id(student['user_id'])
                if user:
                    user['name'] = data['name']
            
            return jsonify({'success': True, 'message': '学生信息更新成功'})
    
    return jsonify({'success': False, 'message': '学生不存在'}), 404


@admin_bp.route('/api/admin/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """删除学生"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    for i, student in enumerate(db.students):
        if student['id'] == student_id:
            # 删除用户
            for j, user in enumerate(db.users):
                if user['id'] == student['user_id']:
                    db.users.pop(j)
                    break
            db.students.pop(i)
            return jsonify({'success': True, 'message': '学生删除成功'})
    
    return jsonify({'success': False, 'message': '学生不存在'}), 404


# ==================== 教师管理 ====================

@admin_bp.route('/api/admin/teachers', methods=['GET'])
def get_teachers():
    """获取教师列表"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    result = []
    for teacher in db.teachers:
        user = db.get_user_by_id(teacher['user_id'])
        result.append({
            'id': teacher['id'],
            'user_id': teacher['user_id'],
            'name': user['name'] if user else '',
            'teacher_no': teacher['teacher_no'],
            'department': teacher['department'],
            'title': teacher['title']
        })
    
    return jsonify({'success': True, 'data': result})


@admin_bp.route('/api/admin/teachers', methods=['POST'])
def create_teacher():
    """创建教师"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    data = request.get_json()
    
    # 创建用户
    new_user_id = max(u['id'] for u in db.users) + 1
    db.users.append({
        'id': new_user_id,
        'username': data.get('username', data.get('teacher_no')),
        'password': data.get('password', '123456'),
        'role': 'teacher',
        'name': data.get('name')
    })
    
    # 创建教师
    new_teacher_id = max(t['id'] for t in db.teachers) + 1
    db.teachers.append({
        'id': new_teacher_id,
        'user_id': new_user_id,
        'teacher_no': data.get('teacher_no'),
        'department': data.get('department'),
        'title': data.get('title', '讲师')
    })
    
    return jsonify({'success': True, 'message': '教师创建成功'})


# ==================== 课程管理 ====================

@admin_bp.route('/api/admin/courses', methods=['GET'])
def get_courses():
    """获取课程列表"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    result = []
    for course in db.courses:
        teacher = db.get_teacher_by_id(course['teacher_id'])
        teacher_user = db.get_user_by_id(teacher['user_id']) if teacher else None
        result.append({
            'id': course['id'],
            'code': course['code'],
            'name': course['name'],
            'credit': course['credit'],
            'hours': course['hours'],
            'teacher_id': course['teacher_id'],
            'teacher_name': teacher_user['name'] if teacher_user else ''
        })
    
    return jsonify({'success': True, 'data': result})


@admin_bp.route('/api/admin/courses', methods=['POST'])
def create_course():
    """创建课程"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    data = request.get_json()
    
    new_id = max(c['id'] for c in db.courses) + 1 if db.courses else 1
    db.courses.append({
        'id': new_id,
        'code': data.get('code'),
        'name': data.get('name'),
        'credit': data.get('credit', 3),
        'hours': data.get('hours', 48),
        'teacher_id': data.get('teacher_id')
    })
    
    return jsonify({'success': True, 'message': '课程创建成功'})


@admin_bp.route('/api/admin/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """更新课程信息"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    data = request.get_json()
    
    for course in db.courses:
        if course['id'] == course_id:
            if 'name' in data:
                course['name'] = data['name']
            if 'credit' in data:
                course['credit'] = data['credit']
            if 'hours' in data:
                course['hours'] = data['hours']
            if 'teacher_id' in data:
                course['teacher_id'] = data['teacher_id']
            
            return jsonify({'success': True, 'message': '课程更新成功'})
    
    return jsonify({'success': False, 'message': '课程不存在'}), 404


# ==================== 教室管理 ====================

@admin_bp.route('/api/admin/classrooms', methods=['GET'])
def get_classrooms():
    """获取教室列表"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    return jsonify({'success': True, 'data': db.classrooms})


@admin_bp.route('/api/admin/classrooms', methods=['POST'])
def create_classroom():
    """创建教室"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    data = request.get_json()
    
    new_id = max(c['id'] for c in db.classrooms) + 1 if db.classrooms else 1
    db.classrooms.append({
        'id': new_id,
        'building': data.get('building'),
        'room_no': data.get('room_no'),
        'capacity': data.get('capacity', 40),
        'type': data.get('type', '普通教室')
    })
    
    return jsonify({'success': True, 'message': '教室创建成功'})


# ==================== 排课管理 ====================

@admin_bp.route('/api/admin/schedule', methods=['GET'])
def get_all_schedule():
    """获取所有排课"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    weekday_names = ['', '周一', '周二', '周三', '周四', '周五', '周六', '周日']
    result = []
    for schedule in db.schedules:
        course = db.get_course_by_id(schedule['course_id'])
        teacher = db.get_teacher_by_id(course['teacher_id']) if course else None
        teacher_user = db.get_user_by_id(teacher['user_id']) if teacher else None
        result.append({
            'id': schedule['id'],
            'course_id': schedule['course_id'],
            'course_name': course['name'] if course else '',
            'course_code': course['code'] if course else '',
            'teacher_name': teacher_user['name'] if teacher_user else '',
            'semester': schedule['semester'],
            'weekday': schedule['weekday'],
            'weekday_name': weekday_names[schedule['weekday']] if schedule['weekday'] < len(weekday_names) else '',
            'start_period': schedule['start_period'],
            'end_period': schedule['end_period'],
            'classroom': schedule['classroom'],
            'weeks': schedule['weeks']
        })
    
    return jsonify({'success': True, 'data': result})


@admin_bp.route('/api/admin/schedule', methods=['POST'])
def create_schedule():
    """创建排课"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    data = request.get_json()
    
    new_id = max(s['id'] for s in db.schedules) + 1 if db.schedules else 1
    db.schedules.append({
        'id': new_id,
        'course_id': data.get('course_id'),
        'semester': data.get('semester', '2024-2025-1'),
        'weekday': data.get('weekday'),
        'start_period': data.get('start_period'),
        'end_period': data.get('end_period'),
        'classroom': data.get('classroom'),
        'weeks': data.get('weeks', '1-16')
    })
    
    return jsonify({'success': True, 'message': '排课创建成功'})


@admin_bp.route('/api/admin/schedule/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    """调课"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    data = request.get_json()
    
    for schedule in db.schedules:
        if schedule['id'] == schedule_id:
            if 'weekday' in data:
                schedule['weekday'] = data['weekday']
            if 'start_period' in data:
                schedule['start_period'] = data['start_period']
            if 'end_period' in data:
                schedule['end_period'] = data['end_period']
            if 'classroom' in data:
                schedule['classroom'] = data['classroom']
            if 'weeks' in data:
                schedule['weeks'] = data['weeks']
            
            return jsonify({'success': True, 'message': '调课成功'})
    
    return jsonify({'success': False, 'message': '排课不存在'}), 404


# ==================== 考试安排 ====================

@admin_bp.route('/api/admin/exams', methods=['GET'])
def get_exams():
    """获取考试安排"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    result = []
    for exam in db.exam_arrangements:
        schedule = db.get_schedule_by_id(exam['schedule_id'])
        course = db.get_course_by_id(schedule['course_id']) if schedule else None
        result.append({
            'id': exam['id'],
            'schedule_id': exam['schedule_id'],
            'course_name': course['name'] if course else '',
            'course_code': course['code'] if course else '',
            'date': exam['date'],
            'start_time': exam['start_time'],
            'end_time': exam['end_time'],
            'classroom': exam['classroom']
        })
    
    return jsonify({'success': True, 'data': result})


@admin_bp.route('/api/admin/exams', methods=['POST'])
def create_exam():
    """创建考试安排"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    data = request.get_json()
    
    new_id = max(e['id'] for e in db.exam_arrangements) + 1 if db.exam_arrangements else 1
    db.exam_arrangements.append({
        'id': new_id,
        'schedule_id': data.get('schedule_id'),
        'date': data.get('date'),
        'start_time': data.get('start_time'),
        'end_time': data.get('end_time'),
        'classroom': data.get('classroom')
    })
    
    return jsonify({'success': True, 'message': '考试安排创建成功'})


# ==================== 监考安排 ====================

@admin_bp.route('/api/admin/invigilators', methods=['GET'])
def get_invigilators():
    """获取监考安排"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    result = []
    for assignment in db.invigilator_assignments:
        exam = None
        for e in db.exam_arrangements:
            if e['id'] == assignment['exam_id']:
                exam = e
                break
        
        teacher = db.get_teacher_by_id(assignment['teacher_id'])
        teacher_user = db.get_user_by_id(teacher['user_id']) if teacher else None
        
        schedule = db.get_schedule_by_id(exam['schedule_id']) if exam else None
        course = db.get_course_by_id(schedule['course_id']) if schedule else None
        
        result.append({
            'id': assignment['id'],
            'exam_id': assignment['exam_id'],
            'course_name': course['name'] if course else '',
            'exam_date': exam['date'] if exam else '',
            'exam_time': f"{exam['start_time']}-{exam['end_time']}" if exam else '',
            'classroom': exam['classroom'] if exam else '',
            'teacher_id': assignment['teacher_id'],
            'teacher_name': teacher_user['name'] if teacher_user else '',
            'role': assignment['role']
        })
    
    return jsonify({'success': True, 'data': result})


@admin_bp.route('/api/admin/invigilators', methods=['POST'])
def create_invigilator():
    """创建监考安排"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    data = request.get_json()
    
    new_id = max(a['id'] for a in db.invigilator_assignments) + 1 if db.invigilator_assignments else 1
    db.invigilator_assignments.append({
        'id': new_id,
        'exam_id': data.get('exam_id'),
        'teacher_id': data.get('teacher_id'),
        'role': data.get('role', '监考')
    })
    
    return jsonify({'success': True, 'message': '监考安排创建成功'})


# ==================== 借教室审批 ====================

@admin_bp.route('/api/admin/classroom-borrow', methods=['GET'])
def get_classroom_borrow():
    """获取借教室申请列表"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    result = []
    for record in db.classroom_borrow_records:
        classroom = db.get_classroom_by_id(record['classroom_id'])
        result.append({
            'id': record['id'],
            'classroom': classroom['room_no'] if classroom else '',
            'building': classroom['building'] if classroom else '',
            'applicant': record['applicant'],
            'purpose': record['purpose'],
            'date': record['date'],
            'time': f"{record['start_time']}-{record['end_time']}",
            'status': record['status']
        })
    
    return jsonify({'success': True, 'data': result})


@admin_bp.route('/api/admin/classroom-borrow/<int:record_id>', methods=['PUT'])
def process_classroom_borrow(record_id):
    """处理借教室申请"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    data = request.get_json()
    action = data.get('action')  # 'approve' or 'reject'
    
    if action not in ['approve', 'reject']:
        return jsonify({'success': False, 'message': '无效的操作'}), 400
    
    for record in db.classroom_borrow_records:
        if record['id'] == record_id:
            record['status'] = 'approved' if action == 'approve' else 'rejected'
            return jsonify({'success': True, 'message': '处理成功'})
    
    return jsonify({'success': False, 'message': '申请不存在'}), 404


# ==================== 审批中心 ====================

@admin_bp.route('/api/admin/approvals', methods=['GET'])
def get_approvals():
    """获取所有待审批项目"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    approvals = db.get_all_approvals()
    
    return jsonify({'success': True, 'data': approvals})


@admin_bp.route('/api/admin/approve', methods=['PUT'])
def process_approval():
    """处理审批"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    data = request.get_json()
    approval_type = data.get('type')
    approval_id = data.get('id')
    action = data.get('action')  # 'approve' or 'reject'
    
    if action not in ['approve', 'reject']:
        return jsonify({'success': False, 'message': '无效的操作'}), 400
    
    new_status = 'approved' if action == 'approve' else 'rejected'
    
    if approval_type == 'status_change':
        for item in db.status_changes:
            if item['id'] == approval_id:
                item['status'] = new_status
                # 如果通过，更新学生状态
                if action == 'approve':
                    student = db.get_student_by_id(item['student_id'])
                    if student:
                        if item['type'] == '休学':
                            student['status'] = 'suspended'
                        elif item['type'] == '退学':
                            student['status'] = 'withdrawn'
                return jsonify({'success': True, 'message': '处理成功'})
    
    elif approval_type == 'retake':
        for item in db.retake_applications:
            if item['id'] == approval_id:
                item['status'] = new_status
                return jsonify({'success': True, 'message': '处理成功'})
    
    elif approval_type == 'grade_review':
        for item in db.grade_reviews:
            if item['id'] == approval_id:
                item['status'] = new_status
                return jsonify({'success': True, 'message': '处理成功'})
    
    elif approval_type == 'topic_application':
        for item in db.topic_applications:
            if item['id'] == approval_id:
                item['status'] = new_status
                if action == 'approve':
                    # 创建指导关系
                    topic = db.get_topic_by_id(item['topic_id'])
                    if topic:
                        new_relation_id = max(r['id'] for r in db.instructor_relations) + 1 if db.instructor_relations else 1
                        db.instructor_relations.append({
                            'id': new_relation_id,
                            'student_id': item['student_id'],
                            'teacher_id': topic['teacher_id'],
                            'topic_id': item['topic_id'],
                            'status': 'confirmed'
                        })
                return jsonify({'success': True, 'message': '处理成功'})
    
    elif approval_type == 'classroom_borrow':
        for item in db.classroom_borrow_records:
            if item['id'] == approval_id:
                item['status'] = new_status
                return jsonify({'success': True, 'message': '处理成功'})
    
    return jsonify({'success': False, 'message': '审批项不存在'}), 404


# ==================== 统计数据 ====================

@admin_bp.route('/api/admin/statistics', methods=['GET'])
def get_statistics():
    """获取统计数据"""
    if not check_admin():
        return jsonify({'success': False, 'message': '无权访问'}), 403
    
    return jsonify({
        'success': True,
        'data': {
            'student_count': len(db.students),
            'teacher_count': len(db.teachers),
            'course_count': len(db.courses),
            'classroom_count': len(db.classrooms),
            'pending_approvals': len([a for a in db.get_all_approvals() if a['status'] == 'pending'])
        }
    })
