<template>
  <div class="exams-page">
    <h1 class="page-title">监考安排</h1>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>我的监考任务</span>
        </div>
      </template>
      
      <div v-if="exams.length > 0" class="exams-list">
        <div v-for="exam in exams" :key="exam.id" class="exam-item">
          <div class="exam-date">
            <div class="date-day">{{ getDay(exam.date) }}</div>
            <div class="date-month">{{ getMonth(exam.date) }}</div>
          </div>
          
          <div class="exam-info">
            <h3>{{ exam.course_name }}</h3>
            <p class="course-code">{{ exam.course_code }}</p>
            <div class="exam-meta">
              <span>
                <el-icon><Clock /></el-icon>
                {{ exam.start_time }} - {{ exam.end_time }}
              </span>
              <span>
                <el-icon><Location /></el-icon>
                {{ exam.classroom }}
              </span>
            </div>
          </div>
          
          <div class="exam-role">
            <el-tag :type="exam.role === '主监考' ? 'primary' : 'success'" size="large">
              {{ exam.role }}
            </el-tag>
          </div>
        </div>
      </div>
      
      <el-empty v-else description="暂无监考安排" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Clock, Location } from '@element-plus/icons-vue'
import { teacherApi } from '../../api'

const exams = ref([])

const getDay = (dateStr) => {
  const date = new Date(dateStr)
  return date.getDate()
}

const getMonth = (dateStr) => {
  const date = new Date(dateStr)
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  return months[date.getMonth()]
}

onMounted(async () => {
  try {
    const res = await teacherApi.getExams()
    exams.value = res.data
  } catch (error) {
    console.error('Error loading exams:', error)
  }
})
</script>

<style scoped>
.exams-page {
  animation: fadeIn 0.3s ease;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.exams-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.exam-item {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  transition: all 0.3s;
}

.exam-item:hover {
  background: #f0f2f5;
}

.exam-date {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.date-day {
  font-size: 28px;
  font-weight: 700;
  line-height: 1;
}

.date-month {
  font-size: 14px;
  margin-top: 4px;
}

.exam-info {
  flex: 1;
}

.exam-info h3 {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.course-code {
  font-size: 13px;
  color: #909399;
  margin-bottom: 8px;
}

.exam-meta {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: #606266;
}

.exam-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.exam-role {
  flex-shrink: 0;
}
</style>
