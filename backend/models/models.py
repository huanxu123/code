"""
数据模型定义
包含所有实体的模型定义和模拟数据
"""

from datetime import datetime
from enum import Enum


# ==================== 枚举类型 ====================

class UserRole(Enum):
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'


class ApprovalStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class StudentStatus(Enum):
    NORMAL = 'normal'
    SUSPENDED = 'suspended'
    GRADUATED = 'graduated'
    WITHDRAWN = 'withdrawn'


# ==================== 模拟数据存储 ====================

class MockDatabase:
    """模拟数据库，用于开发测试"""
    
    def __init__(self):
        self._init_users()
        self._init_students()
        self._init_teachers()
        self._init_courses()
        self._init_schedules()
        self._init_selections()
        self._init_grades()
        self._init_evaluations()
        self._init_topics()
        self._init_classrooms()
        self._init_exams()
        self._init_applications()
    
    def _init_users(self):
        """初始化用户数据"""
        self.users = [
            {'id': 1, 'username': 'student1', 'password': '123456', 'role': 'student', 'name': '张三'},
            {'id': 2, 'username': 'student2', 'password': '123456', 'role': 'student', 'name': '李四'},
            {'id': 3, 'username': 'student3', 'password': '123456', 'role': 'student', 'name': '王五'},
            {'id': 4, 'username': 'teacher1', 'password': '123456', 'role': 'teacher', 'name': '刘教授'},
            {'id': 5, 'username': 'teacher2', 'password': '123456', 'role': 'teacher', 'name': '陈教授'},
            {'id': 6, 'username': 'admin1', 'password': '123456', 'role': 'admin', 'name': '教务管理员'},
        ]
    
    def _init_students(self):
        """初始化学生数据"""
        self.students = [
            {'id': 1, 'user_id': 1, 'student_no': '2021001001', 'class_name': '计算机2101班', 
             'major': '计算机科学与技术', 'grade': '2021级', 'status': 'normal'},
            {'id': 2, 'user_id': 2, 'student_no': '2021001002', 'class_name': '计算机2101班',
             'major': '计算机科学与技术', 'grade': '2021级', 'status': 'normal'},
            {'id': 3, 'user_id': 3, 'student_no': '2021002001', 'class_name': '软件2101班',
             'major': '软件工程', 'grade': '2021级', 'status': 'normal'},
        ]
    
    def _init_teachers(self):
        """初始化教师数据"""
        self.teachers = [
            {'id': 1, 'user_id': 4, 'teacher_no': 'T001', 'department': '计算机学院', 'title': '教授'},
            {'id': 2, 'user_id': 5, 'teacher_no': 'T002', 'department': '计算机学院', 'title': '副教授'},
        ]
    
    def _init_courses(self):
        """初始化课程数据"""
        self.courses = [
            {'id': 1, 'code': 'CS101', 'name': '程序设计基础', 'credit': 4, 'hours': 64, 'teacher_id': 1},
            {'id': 2, 'code': 'CS201', 'name': '数据结构', 'credit': 4, 'hours': 64, 'teacher_id': 1},
            {'id': 3, 'code': 'CS301', 'name': '操作系统', 'credit': 3, 'hours': 48, 'teacher_id': 2},
            {'id': 4, 'code': 'CS302', 'name': '计算机网络', 'credit': 3, 'hours': 48, 'teacher_id': 2},
            {'id': 5, 'code': 'CS401', 'name': '数据库原理', 'credit': 3, 'hours': 48, 'teacher_id': 1},
            {'id': 6, 'code': 'CS402', 'name': '软件工程', 'credit': 3, 'hours': 48, 'teacher_id': 2},
        ]
    
    def _init_schedules(self):
        """初始化课程表数据"""
        self.schedules = [
            {'id': 1, 'course_id': 1, 'semester': '2024-2025-1', 'weekday': 1, 
             'start_period': 1, 'end_period': 2, 'classroom': 'A101', 'weeks': '1-16'},
            {'id': 2, 'course_id': 2, 'semester': '2024-2025-1', 'weekday': 2, 
             'start_period': 3, 'end_period': 4, 'classroom': 'A102', 'weeks': '1-16'},
            {'id': 3, 'course_id': 3, 'semester': '2024-2025-1', 'weekday': 3, 
             'start_period': 1, 'end_period': 2, 'classroom': 'B201', 'weeks': '1-16'},
            {'id': 4, 'course_id': 4, 'semester': '2024-2025-1', 'weekday': 4, 
             'start_period': 5, 'end_period': 6, 'classroom': 'B202', 'weeks': '1-16'},
            {'id': 5, 'course_id': 5, 'semester': '2024-2025-1', 'weekday': 5, 
             'start_period': 3, 'end_period': 4, 'classroom': 'A103', 'weeks': '1-16'},
        ]
    
    def _init_selections(self):
        """初始化选课数据"""
        self.course_selections = [
            {'id': 1, 'student_id': 1, 'schedule_id': 1, 'status': 'confirmed', 'selected_at': '2024-09-01'},
            {'id': 2, 'student_id': 1, 'schedule_id': 2, 'status': 'confirmed', 'selected_at': '2024-09-01'},
            {'id': 3, 'student_id': 1, 'schedule_id': 3, 'status': 'confirmed', 'selected_at': '2024-09-01'},
            {'id': 4, 'student_id': 2, 'schedule_id': 1, 'status': 'confirmed', 'selected_at': '2024-09-01'},
            {'id': 5, 'student_id': 2, 'schedule_id': 4, 'status': 'confirmed', 'selected_at': '2024-09-01'},
        ]
    
    def _init_grades(self):
        """初始化成绩数据"""
        self.grades = [
            {'id': 1, 'selection_id': 1, 'score': 85, 'gpa': 3.7, 'status': 'final'},
            {'id': 2, 'selection_id': 2, 'score': 92, 'gpa': 4.0, 'status': 'final'},
            {'id': 3, 'selection_id': 3, 'score': 78, 'gpa': 3.0, 'status': 'final'},
            {'id': 4, 'selection_id': 4, 'score': 88, 'gpa': 3.7, 'status': 'final'},
        ]
        
        self.grade_reviews = [
            {'id': 1, 'grade_id': 3, 'student_id': 1, 'reason': '考试时身体不适，成绩与平时表现不符', 
             'status': 'pending', 'created_at': '2024-12-10'},
        ]
    
    def _init_evaluations(self):
        """初始化评教数据"""
        self.evaluations = [
            {'id': 1, 'selection_id': 1, 'student_id': 1, 'rating': 0, 'comment': '', 'status': 'pending'},
            {'id': 2, 'selection_id': 2, 'student_id': 1, 'rating': 5, 'comment': '讲解清晰', 'status': 'completed'},
        ]
    
    def _init_topics(self):
        """初始化毕设课题数据"""
        self.graduation_topics = [
            {'id': 1, 'teacher_id': 1, 'title': '基于深度学习的图像识别系统', 
             'description': '研究卷积神经网络在图像分类中的应用', 'max_students': 2, 'status': 'open'},
            {'id': 2, 'teacher_id': 1, 'title': '分布式数据库系统设计与实现',
             'description': '设计一个支持水平扩展的分布式数据库', 'max_students': 1, 'status': 'open'},
            {'id': 3, 'teacher_id': 2, 'title': 'Web应用安全漏洞检测工具',
             'description': '开发自动化的Web安全扫描工具', 'max_students': 2, 'status': 'open'},
        ]
        
        self.topic_applications = [
            {'id': 1, 'student_id': 1, 'topic_id': 1, 'status': 'pending', 'created_at': '2024-12-01'},
        ]
        
        self.instructor_relations = [
            {'id': 1, 'student_id': 2, 'teacher_id': 1, 'topic_id': 2, 'status': 'confirmed'},
        ]
        
        self.process_documents = [
            {'id': 1, 'student_id': 2, 'type': '开题报告', 'file_name': 'opening_report.pdf', 
             'status': 'submitted', 'submitted_at': '2024-11-15'},
        ]
    
    def _init_classrooms(self):
        """初始化教室数据"""
        self.classrooms = [
            {'id': 1, 'building': 'A楼', 'room_no': 'A101', 'capacity': 60, 'type': '普通教室'},
            {'id': 2, 'building': 'A楼', 'room_no': 'A102', 'capacity': 60, 'type': '普通教室'},
            {'id': 3, 'building': 'A楼', 'room_no': 'A103', 'capacity': 40, 'type': '多媒体教室'},
            {'id': 4, 'building': 'B楼', 'room_no': 'B201', 'capacity': 80, 'type': '阶梯教室'},
            {'id': 5, 'building': 'B楼', 'room_no': 'B202', 'capacity': 80, 'type': '阶梯教室'},
            {'id': 6, 'building': 'C楼', 'room_no': 'C301', 'capacity': 30, 'type': '机房'},
        ]
        
        self.classroom_borrow_records = [
            {'id': 1, 'classroom_id': 3, 'applicant': '学生会', 'purpose': '社团活动',
             'date': '2024-12-20', 'start_time': '14:00', 'end_time': '17:00', 'status': 'pending'},
        ]
    
    def _init_exams(self):
        """初始化考试数据"""
        self.exam_arrangements = [
            {'id': 1, 'schedule_id': 1, 'date': '2025-01-10', 'start_time': '09:00', 
             'end_time': '11:00', 'classroom': 'A101'},
            {'id': 2, 'schedule_id': 2, 'date': '2025-01-12', 'start_time': '14:00',
             'end_time': '16:00', 'classroom': 'A102'},
            {'id': 3, 'schedule_id': 3, 'date': '2025-01-14', 'start_time': '09:00',
             'end_time': '11:00', 'classroom': 'B201'},
        ]
        
        self.invigilator_assignments = [
            {'id': 1, 'exam_id': 1, 'teacher_id': 1, 'role': '主监考'},
            {'id': 2, 'exam_id': 1, 'teacher_id': 2, 'role': '副监考'},
            {'id': 3, 'exam_id': 2, 'teacher_id': 2, 'role': '主监考'},
        ]
    
    def _init_applications(self):
        """初始化申请数据"""
        self.status_changes = [
            {'id': 1, 'student_id': 3, 'type': '休学', 'reason': '身体原因需要休养',
             'status': 'pending', 'created_at': '2024-12-05'},
        ]
        
        self.retake_applications = [
            {'id': 1, 'student_id': 1, 'course_id': 3, 'reason': '成绩不理想，希望重修提高',
             'status': 'pending', 'created_at': '2024-12-08'},
        ]
    
    # ==================== 查询方法 ====================
    
    def get_user_by_username(self, username):
        """根据用户名查找用户"""
        for user in self.users:
            if user['username'] == username:
                return user
        return None
    
    def get_user_by_id(self, user_id):
        """根据ID查找用户"""
        for user in self.users:
            if user['id'] == user_id:
                return user
        return None
    
    def get_student_by_user_id(self, user_id):
        """根据用户ID查找学生信息"""
        for student in self.students:
            if student['user_id'] == user_id:
                return student
        return None
    
    def get_teacher_by_user_id(self, user_id):
        """根据用户ID查找教师信息"""
        for teacher in self.teachers:
            if teacher['user_id'] == user_id:
                return teacher
        return None
    
    def get_course_by_id(self, course_id):
        """根据ID查找课程"""
        for course in self.courses:
            if course['id'] == course_id:
                return course
        return None
    
    def get_schedule_by_id(self, schedule_id):
        """根据ID查找课程表"""
        for schedule in self.schedules:
            if schedule['id'] == schedule_id:
                return schedule
        return None
    
    def get_schedules_by_student(self, student_id):
        """获取学生的课程表"""
        result = []
        for selection in self.course_selections:
            if selection['student_id'] == student_id and selection['status'] == 'confirmed':
                schedule = self.get_schedule_by_id(selection['schedule_id'])
                if schedule:
                    course = self.get_course_by_id(schedule['course_id'])
                    teacher = self.get_teacher_by_id(course['teacher_id']) if course else None
                    teacher_user = self.get_user_by_id(teacher['user_id']) if teacher else None
                    result.append({
                        **schedule,
                        'course': course,
                        'teacher_name': teacher_user['name'] if teacher_user else ''
                    })
        return result
    
    def get_teacher_by_id(self, teacher_id):
        """根据ID查找教师"""
        for teacher in self.teachers:
            if teacher['id'] == teacher_id:
                return teacher
        return None
    
    def get_schedules_by_teacher(self, teacher_id):
        """获取教师的课程表"""
        result = []
        for schedule in self.schedules:
            course = self.get_course_by_id(schedule['course_id'])
            if course and course['teacher_id'] == teacher_id:
                result.append({
                    **schedule,
                    'course': course
                })
        return result
    
    def get_grades_by_student(self, student_id):
        """获取学生成绩"""
        result = []
        for selection in self.course_selections:
            if selection['student_id'] == student_id:
                for grade in self.grades:
                    if grade['selection_id'] == selection['id']:
                        schedule = self.get_schedule_by_id(selection['schedule_id'])
                        course = self.get_course_by_id(schedule['course_id']) if schedule else None
                        result.append({
                            **grade,
                            'course': course,
                            'semester': schedule['semester'] if schedule else ''
                        })
        return result
    
    def get_pending_evaluations(self, student_id):
        """获取未完成的评教"""
        result = []
        for evaluation in self.evaluations:
            if evaluation['student_id'] == student_id and evaluation['status'] == 'pending':
                for selection in self.course_selections:
                    if selection['id'] == evaluation['selection_id']:
                        schedule = self.get_schedule_by_id(selection['schedule_id'])
                        course = self.get_course_by_id(schedule['course_id']) if schedule else None
                        teacher = self.get_teacher_by_id(course['teacher_id']) if course else None
                        teacher_user = self.get_user_by_id(teacher['user_id']) if teacher else None
                        result.append({
                            **evaluation,
                            'course': course,
                            'teacher_name': teacher_user['name'] if teacher_user else ''
                        })
        return result
    
    def get_available_courses(self, semester):
        """获取可选课程"""
        result = []
        for schedule in self.schedules:
            if schedule['semester'] == semester:
                course = self.get_course_by_id(schedule['course_id'])
                teacher = self.get_teacher_by_id(course['teacher_id']) if course else None
                teacher_user = self.get_user_by_id(teacher['user_id']) if teacher else None
                result.append({
                    **schedule,
                    'course': course,
                    'teacher_name': teacher_user['name'] if teacher_user else ''
                })
        return result
    
    def get_all_approvals(self):
        """获取所有待审批项目"""
        approvals = []
        
        # 学籍异动
        for item in self.status_changes:
            if item['status'] == 'pending':
                student = self.get_student_by_id(item['student_id'])
                user = self.get_user_by_id(student['user_id']) if student else None
                approvals.append({
                    'id': item['id'],
                    'type': 'status_change',
                    'type_name': '学籍异动',
                    'subtype': item['type'],
                    'applicant': user['name'] if user else '',
                    'reason': item['reason'],
                    'created_at': item['created_at'],
                    'status': item['status']
                })
        
        # 重修申请
        for item in self.retake_applications:
            if item['status'] == 'pending':
                student = self.get_student_by_id(item['student_id'])
                user = self.get_user_by_id(student['user_id']) if student else None
                course = self.get_course_by_id(item['course_id'])
                approvals.append({
                    'id': item['id'],
                    'type': 'retake',
                    'type_name': '重修申请',
                    'subtype': course['name'] if course else '',
                    'applicant': user['name'] if user else '',
                    'reason': item['reason'],
                    'created_at': item['created_at'],
                    'status': item['status']
                })
        
        # 成绩复核
        for item in self.grade_reviews:
            if item['status'] == 'pending':
                student = self.get_student_by_id(item['student_id'])
                user = self.get_user_by_id(student['user_id']) if student else None
                approvals.append({
                    'id': item['id'],
                    'type': 'grade_review',
                    'type_name': '成绩复核',
                    'subtype': '',
                    'applicant': user['name'] if user else '',
                    'reason': item['reason'],
                    'created_at': item['created_at'],
                    'status': item['status']
                })
        
        # 毕设选题
        for item in self.topic_applications:
            if item['status'] == 'pending':
                student = self.get_student_by_id(item['student_id'])
                user = self.get_user_by_id(student['user_id']) if student else None
                topic = self.get_topic_by_id(item['topic_id'])
                approvals.append({
                    'id': item['id'],
                    'type': 'topic_application',
                    'type_name': '毕设选题',
                    'subtype': topic['title'] if topic else '',
                    'applicant': user['name'] if user else '',
                    'reason': '',
                    'created_at': item['created_at'],
                    'status': item['status']
                })
        
        # 借教室
        for item in self.classroom_borrow_records:
            if item['status'] == 'pending':
                classroom = self.get_classroom_by_id(item['classroom_id'])
                approvals.append({
                    'id': item['id'],
                    'type': 'classroom_borrow',
                    'type_name': '借教室',
                    'subtype': classroom['room_no'] if classroom else '',
                    'applicant': item['applicant'],
                    'reason': item['purpose'],
                    'created_at': item['date'],
                    'status': item['status']
                })
        
        return approvals
    
    def get_student_by_id(self, student_id):
        """根据ID查找学生"""
        for student in self.students:
            if student['id'] == student_id:
                return student
        return None
    
    def get_topic_by_id(self, topic_id):
        """根据ID查找课题"""
        for topic in self.graduation_topics:
            if topic['id'] == topic_id:
                return topic
        return None
    
    def get_classroom_by_id(self, classroom_id):
        """根据ID查找教室"""
        for classroom in self.classrooms:
            if classroom['id'] == classroom_id:
                return classroom
        return None
    
    def get_exams_by_teacher(self, teacher_id):
        """获取教师的监考安排"""
        result = []
        for assignment in self.invigilator_assignments:
            if assignment['teacher_id'] == teacher_id:
                exam = None
                for e in self.exam_arrangements:
                    if e['id'] == assignment['exam_id']:
                        exam = e
                        break
                if exam:
                    schedule = self.get_schedule_by_id(exam['schedule_id'])
                    course = self.get_course_by_id(schedule['course_id']) if schedule else None
                    result.append({
                        **assignment,
                        'exam': exam,
                        'course': course
                    })
        return result
    
    def get_topics_by_teacher(self, teacher_id):
        """获取教师的毕设课题"""
        result = []
        for topic in self.graduation_topics:
            if topic['teacher_id'] == teacher_id:
                # 统计已选学生数
                selected_count = sum(1 for app in self.topic_applications 
                                    if app['topic_id'] == topic['id'] and app['status'] == 'approved')
                result.append({
                    **topic,
                    'selected_count': selected_count
                })
        return result
    
    def get_students_by_teacher(self, teacher_id):
        """获取教师指导的学生"""
        result = []
        for relation in self.instructor_relations:
            if relation['teacher_id'] == teacher_id:
                student = self.get_student_by_id(relation['student_id'])
                user = self.get_user_by_id(student['user_id']) if student else None
                topic = self.get_topic_by_id(relation['topic_id'])
                result.append({
                    'student': student,
                    'student_name': user['name'] if user else '',
                    'topic': topic,
                    'status': relation['status']
                })
        return result
    
    def get_grade_reviews_by_teacher(self, teacher_id):
        """获取教师相关的成绩复核申请"""
        result = []
        for review in self.grade_reviews:
            grade = None
            for g in self.grades:
                if g['id'] == review['grade_id']:
                    grade = g
                    break
            if grade:
                selection = None
                for s in self.course_selections:
                    if s['id'] == grade['selection_id']:
                        selection = s
                        break
                if selection:
                    schedule = self.get_schedule_by_id(selection['schedule_id'])
                    course = self.get_course_by_id(schedule['course_id']) if schedule else None
                    if course and course['teacher_id'] == teacher_id:
                        student = self.get_student_by_id(selection['student_id'])
                        user = self.get_user_by_id(student['user_id']) if student else None
                        result.append({
                            **review,
                            'grade': grade,
                            'course': course,
                            'student_name': user['name'] if user else ''
                        })
        return result
    
    def get_course_students(self, schedule_id):
        """获取课程的学生列表及成绩"""
        result = []
        for selection in self.course_selections:
            if selection['schedule_id'] == schedule_id:
                student = self.get_student_by_id(selection['student_id'])
                user = self.get_user_by_id(student['user_id']) if student else None
                grade = None
                for g in self.grades:
                    if g['selection_id'] == selection['id']:
                        grade = g
                        break
                result.append({
                    'selection_id': selection['id'],
                    'student': student,
                    'student_name': user['name'] if user else '',
                    'grade': grade
                })
        return result


# 全局模拟数据库实例
db = MockDatabase()
