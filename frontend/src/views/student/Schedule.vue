<template>
  <div class="schedule-page">
    <h1 class="page-title">课表 / 选课</h1>
    
    <el-tabs v-model="activeTab" class="schedule-tabs">
      <!-- 我的课表 -->
      <el-tab-pane label="我的课表" name="schedule">
        <el-card>
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
                >
                  <div class="course-name">{{ course.course_name }}</div>
                  <div class="course-info">{{ course.classroom }}</div>
                  <div class="course-info">{{ course.teacher_name }}</div>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-tab-pane>
      
      <!-- 选课 -->
      <el-tab-pane label="选课" name="select">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>可选课程列表</span>
              <el-tag type="info">2024-2025 学年第一学期</el-tag>
            </div>
          </template>
          
          <el-table :data="availableCourses" stripe>
            <el-table-column prop="course_code" label="课程代码" width="120" />
            <el-table-column prop="course_name" label="课程名称" />
            <el-table-column prop="credit" label="学分" width="80" align="center" />
            <el-table-column prop="teacher_name" label="授课教师" width="120" />
            <el-table-column label="上课时间" width="150">
              <template #default="{ row }">
                {{ weekdayMap[row.weekday] }} 第{{ row.start_period }}-{{ row.end_period }}节
              </template>
            </el-table-column>
            <el-table-column prop="classroom" label="教室" width="100" />
            <el-table-column label="操作" width="120" align="center">
              <template #default="{ row }">
                <el-button 
                  v-if="!isSelected(row.schedule_id)"
                  type="primary" 
                  size="small"
                  @click="handleSelect(row)"
                >
                  选课
                </el-button>
                <el-button 
                  v-else
                  type="danger" 
                  size="small"
                  @click="handleDrop(row)"
                >
                  退课
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { studentApi } from '../../api'

const activeTab = ref('schedule')
const mySchedule = ref([])
const availableCourses = ref([])

const weekdays = [
  { value: 1, label: '周一' },
  { value: 2, label: '周二' },
  { value: 3, label: '周三' },
  { value: 4, label: '周四' },
  { value: 5, label: '周五' }
]

const weekdayMap = {
  1: '周一', 2: '周二', 3: '周三', 4: '周四', 5: '周五', 6: '周六', 7: '周日'
}

const periods = [1, 2, 3, 4, 5, 6, 7, 8]

const getCoursesAt = (weekday, period) => {
  return mySchedule.value.filter(
    c => c.weekday === weekday && c.start_period === period
  )
}

const isSelected = (scheduleId) => {
  return mySchedule.value.some(s => s.id === scheduleId)
}

const handleSelect = async (course) => {
  try {
    await ElMessageBox.confirm(
      `确定要选择课程「${course.course_name}」吗？`,
      '选课确认',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'info' }
    )
    
    await studentApi.selectCourse(course.schedule_id)
    ElMessage.success('选课成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Select course error:', error)
    }
  }
}

const handleDrop = async (course) => {
  try {
    await ElMessageBox.confirm(
      `确定要退选课程「${course.course_name}」吗？`,
      '退课确认',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
    )
    
    await studentApi.dropCourse(course.schedule_id)
    ElMessage.success('退课成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Drop course error:', error)
    }
  }
}

const loadData = async () => {
  try {
    const [scheduleRes, coursesRes] = await Promise.all([
      studentApi.getSchedule(),
      studentApi.getAvailableCourses()
    ])
    mySchedule.value = scheduleRes.data
    availableCourses.value = coursesRes.data
  } catch (error) {
    console.error('Error loading data:', error)
  }
}

onMounted(loadData)
</script>

<style scoped>
.schedule-page {
  animation: fadeIn 0.3s ease;
}

.schedule-tabs :deep(.el-tabs__header) {
  margin-bottom: 20px;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 6px;
  padding: 8px;
  color: white;
  font-size: 12px;
  overflow: hidden;
  z-index: 1;
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
