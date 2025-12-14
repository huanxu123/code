import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue')
    },
    // 学生端路由
    {
        path: '/student',
        component: () => import('../views/student/Layout.vue'),
        children: [
            {
                path: '',
                redirect: '/student/home'
            },
            {
                path: 'home',
                name: 'StudentHome',
                component: () => import('../views/student/Home.vue')
            },
            {
                path: 'schedule',
                name: 'StudentSchedule',
                component: () => import('../views/student/Schedule.vue')
            },
            {
                path: 'grades',
                name: 'StudentGrades',
                component: () => import('../views/student/Grades.vue')
            },
            {
                path: 'evaluation',
                name: 'StudentEvaluation',
                component: () => import('../views/student/Evaluation.vue')
            },
            {
                path: 'applications',
                name: 'StudentApplications',
                component: () => import('../views/student/Applications.vue')
            },
            {
                path: 'thesis',
                name: 'StudentThesis',
                component: () => import('../views/student/Thesis.vue')
            }
        ]
    },
    // 教师端路由
    {
        path: '/teacher',
        component: () => import('../views/teacher/Layout.vue'),
        children: [
            {
                path: '',
                redirect: '/teacher/home'
            },
            {
                path: 'home',
                name: 'TeacherHome',
                component: () => import('../views/teacher/Home.vue')
            },
            {
                path: 'grades',
                name: 'TeacherGrades',
                component: () => import('../views/teacher/Grades.vue')
            },
            {
                path: 'reviews',
                name: 'TeacherReviews',
                component: () => import('../views/teacher/Reviews.vue')
            },
            {
                path: 'thesis',
                name: 'TeacherThesis',
                component: () => import('../views/teacher/Thesis.vue')
            },
            {
                path: 'exams',
                name: 'TeacherExams',
                component: () => import('../views/teacher/Exams.vue')
            }
        ]
    },
    // 教务端路由
    {
        path: '/admin',
        component: () => import('../views/admin/Layout.vue'),
        children: [
            {
                path: '',
                redirect: '/admin/home'
            },
            {
                path: 'home',
                name: 'AdminHome',
                component: () => import('../views/admin/Home.vue')
            },
            {
                path: 'students',
                name: 'AdminStudents',
                component: () => import('../views/admin/Students.vue')
            },
            {
                path: 'teachers',
                name: 'AdminTeachers',
                component: () => import('../views/admin/Teachers.vue')
            },
            {
                path: 'courses',
                name: 'AdminCourses',
                component: () => import('../views/admin/Courses.vue')
            },
            {
                path: 'schedule',
                name: 'AdminSchedule',
                component: () => import('../views/admin/Schedule.vue')
            },
            {
                path: 'exams',
                name: 'AdminExams',
                component: () => import('../views/admin/Exams.vue')
            },
            {
                path: 'approvals',
                name: 'AdminApprovals',
                component: () => import('../views/admin/Approvals.vue')
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
