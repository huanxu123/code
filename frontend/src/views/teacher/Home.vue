<template>
  <div class="home-page">
    <h1 class="page-title">我的排课</h1>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>本学期课程安排</span>
          <el-tag type="info">2024-2025 学年第一学期</el-tag>
        </div>
      </template>
      
      <div class="schedule-grid">
        <div class="time-column">
          <div class="header-cell">时间</div>
          <div v-for="period in periods" :key="period" class="time-cell">
            第 {{ period }} 节
          </div>
        </div>
        
        <div v-for="day in weekdays" :key="day.value" class="day-column">
          <div class="header-cell">{{ day.label }}</div>
          <div 
            v-for="period in periods" 
            :key="period" 
            class="schedule-cell"
          >
            <div 
              v-for="course in getCoursesAt(day.value, period)" 
              :key="course.id"
              class="course-block"
              :style="{ height: `${(course.end_period - course.start_period + 1) * 60}px` }"
              @click="viewCourseDetail(course)"
            >
              <div class="course-name">{{ course.course_name }}</div>
              <div class="course-info">{{ course.classroom }}</div>
              <div class="course-info">{{ course.weeks }}周</div>
            </div>
          </div>
        </div>
      </div>
    </el-card>
    
    <!-- 课程列表 -->
    <el-card class="course-list-card">
      <template #header>
        <span>课程列表</span>
      </template>
      
      <el-table :data="schedule" stripe>
        <el-table-column prop="course_code" label="课程代码" width="120" />
        <el-table-column prop="course_name" label="课程名称" />
        <el-table-column prop="credit" label="学分" width="80" align="center" />
        <el-table-column label="上课时间" width="150">
          <template #default="{ row }">
            {{ row.weekday_name }} 第{{ row.start_period }}-{{ row.end_period }}节
          </template>
        </el-table-column>
        <el-table-column prop="classroom" label="教室" width="100" />
        <el-table-column prop="weeks" label="周次" width="100" />
        <el-table-column label="操作" width="120" align="center">
          <template #default="{ row }">
            <el-button type="primary" size="small" text @click="goToGrades(row)">
              录入成绩
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { teacherApi } from '../../api'

const router = useRouter()
const schedule = ref([])

const weekdays = [
  { value: 1, label: '周一' },
  { value: 2, label: '周二' },
  { value: 3, label: '周三' },
  { value: 4, label: '周四' },
  { value: 5, label: '周五' }
]

const periods = [1, 2, 3, 4, 5, 6, 7, 8]

const getCoursesAt = (weekday, period) => {
  return schedule.value.filter(
    c => c.weekday === weekday && c.start_period === period
  )
}

const viewCourseDetail = (course) => {
  console.log('View course:', course)
}

const goToGrades = (course) => {
  router.push({
    path: '/teacher/grades',
    query: { schedule_id: course.id }
  })
}

onMounted(async () => {
  try {
    const res = await teacherApi.getSchedule()
    schedule.value = res.data
  } catch (error) {
    console.error('Error loading schedule:', error)
  }
})
</script>

<style scoped>
.home-page {
  animation: fadeIn 0.3s ease;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.schedule-grid {
  display: flex;
  gap: 1px;
  background: #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
}

.time-column,
.day-column {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.time-column {
  flex: 0 0 80px;
}

.header-cell {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  font-weight: 600;
  color: #2c3e50;
}

.time-cell {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  font-size: 12px;
  color: #909399;
}

.schedule-cell {
  height: 60px;
  background: white;
  position: relative;
}

.course-block {
  position: absolute;
  top: 2px;
  left: 2px;
  right: 2px;
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  border-radius: 6px;
  padding: 8px;
  color: white;
  font-size: 12px;
  overflow: hidden;
  z-index: 1;
  cursor: pointer;
  transition: all 0.3s;
}

.course-block:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4);
}

.course-name {
  font-weight: 600;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.course-info {
  opacity: 0.9;
  font-size: 11px;
}

.course-list-card {
  margin-top: 24px;
}
</style>
