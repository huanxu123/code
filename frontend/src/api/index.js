import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
    baseURL: '/api',
    timeout: 10000,
    withCredentials: true
})

// 响应拦截器
api.interceptors.response.use(
    response => {
        const res = response.data
        if (res.success === false) {
            ElMessage.error(res.message || '请求失败')
            return Promise.reject(new Error(res.message || '请求失败'))
        }
        return res
    },
    error => {
        console.error('API Error:', error)
        ElMessage.error(error.response?.data?.message || '网络错误')
        return Promise.reject(error)
    }
)

export default api

// ==================== 认证相关 ====================

export const authApi = {
    login(username, password) {
        return api.post('/login', { username, password })
    },
    logout() {
        return api.post('/logout')
    },
    getUserInfo() {
        return api.get('/user/info')
    }
}

// ==================== 学生端 API ====================

export const studentApi = {
    getProfile() {
        return api.get('/student/profile')
    },
    getSchedule() {
        return api.get('/student/schedule')
    },
    getAvailableCourses(semester = '2024-2025-1') {
        return api.get('/student/courses', { params: { semester } })
    },
    selectCourse(scheduleId) {
        return api.post('/student/select-course', { schedule_id: scheduleId })
    },
    dropCourse(scheduleId) {
        return api.post('/student/drop-course', { schedule_id: scheduleId })
    },
    getGrades() {
        return api.get('/student/grades')
    },
    submitGradeReview(gradeId, reason) {
        return api.post('/student/grade-review', { grade_id: gradeId, reason })
    },
    getEvaluations() {
        return api.get('/student/evaluations')
    },
    submitEvaluation(evaluationId, rating, comment) {
        return api.post('/student/evaluate', { evaluation_id: evaluationId, rating, comment })
    },
    getStatusChanges() {
        return api.get('/student/status-changes')
    },
    submitStatusChange(type, reason) {
        return api.post('/student/status-changes', { type, reason })
    },
    getRetakes() {
        return api.get('/student/retakes')
    },
    submitRetake(courseId, reason) {
        return api.post('/student/retakes', { course_id: courseId, reason })
    },
    getTopics() {
        return api.get('/student/topics')
    },
    applyTopic(topicId) {
        return api.post('/student/apply-topic', { topic_id: topicId })
    },
    getMyTopic() {
        return api.get('/student/my-topic')
    },
    getDocuments() {
        return api.get('/student/documents')
    },
    submitDocument(type, fileName) {
        return api.post('/student/documents', { type, file_name: fileName })
    }
}

// ==================== 教师端 API ====================

export const teacherApi = {
    getProfile() {
        return api.get('/teacher/profile')
    },
    getSchedule() {
        return api.get('/teacher/schedule')
    },
    getCourses() {
        return api.get('/teacher/courses')
    },
    getCourseStudents(scheduleId) {
        return api.get(`/teacher/students/${scheduleId}`)
    },
    enterGrades(grades) {
        return api.post('/teacher/grades', { grades })
    },
    getReviews() {
        return api.get('/teacher/reviews')
    },
    processReview(reviewId, action, newScore) {
        return api.put(`/teacher/reviews/${reviewId}`, { action, new_score: newScore })
    },
    getTopics() {
        return api.get('/teacher/topics')
    },
    createTopic(title, description, maxStudents) {
        return api.post('/teacher/topics', { title, description, max_students: maxStudents })
    },
    updateTopic(topicId, data) {
        return api.put(`/teacher/topics/${topicId}`, data)
    },
    getTopicApplications() {
        return api.get('/teacher/topic-applications')
    },
    processTopicApplication(appId, action) {
        return api.put(`/teacher/topic-applications/${appId}`, { action })
    },
    getThesisStudents() {
        return api.get('/teacher/students-thesis')
    },
    getExams() {
        return api.get('/teacher/exams')
    }
}

// ==================== 教务端 API ====================

export const adminApi = {
    getStatistics() {
        return api.get('/admin/statistics')
    },
    // 学生管理
    getStudents() {
        return api.get('/admin/students')
    },
    createStudent(data) {
        return api.post('/admin/students', data)
    },
    updateStudent(studentId, data) {
        return api.put(`/admin/students/${studentId}`, data)
    },
    deleteStudent(studentId) {
        return api.delete(`/admin/students/${studentId}`)
    },
    // 教师管理
    getTeachers() {
        return api.get('/admin/teachers')
    },
    createTeacher(data) {
        return api.post('/admin/teachers', data)
    },
    // 课程管理
    getCourses() {
        return api.get('/admin/courses')
    },
    createCourse(data) {
        return api.post('/admin/courses', data)
    },
    updateCourse(courseId, data) {
        return api.put(`/admin/courses/${courseId}`, data)
    },
    // 教室管理
    getClassrooms() {
        return api.get('/admin/classrooms')
    },
    createClassroom(data) {
        return api.post('/admin/classrooms', data)
    },
    // 排课管理
    getSchedule() {
        return api.get('/admin/schedule')
    },
    createSchedule(data) {
        return api.post('/admin/schedule', data)
    },
    updateSchedule(scheduleId, data) {
        return api.put(`/admin/schedule/${scheduleId}`, data)
    },
    // 考试安排
    getExams() {
        return api.get('/admin/exams')
    },
    createExam(data) {
        return api.post('/admin/exams', data)
    },
    // 监考安排
    getInvigilators() {
        return api.get('/admin/invigilators')
    },
    createInvigilator(data) {
        return api.post('/admin/invigilators', data)
    },
    // 借教室审批
    getClassroomBorrow() {
        return api.get('/admin/classroom-borrow')
    },
    processClassroomBorrow(recordId, action) {
        return api.put(`/admin/classroom-borrow/${recordId}`, { action })
    },
    // 审批中心
    getApprovals() {
        return api.get('/admin/approvals')
    },
    processApproval(type, id, action) {
        return api.put('/admin/approve', { type, id, action })
    }
}
