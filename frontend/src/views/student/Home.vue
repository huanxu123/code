<template>
  <div class="home-page">
    <h1 class="page-title">首页</h1>
    
    <!-- 个人信息卡片 -->
    <el-card class="profile-card">
      <div class="profile-content">
        <div class="avatar-section">
          <el-avatar :size="80" class="avatar">
            {{ profile?.name?.charAt(0) }}
          </el-avatar>
          <el-tag :type="statusTagType" size="large" class="status-tag">
            {{ profile?.status_text }}
          </el-tag>
        </div>
        
        <div class="info-section">
          <h2>{{ profile?.name }}</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">学号</span>
              <span class="value">{{ profile?.student_no }}</span>
            </div>
            <div class="info-item">
              <span class="label">班级</span>
              <span class="value">{{ profile?.class_name }}</span>
            </div>
            <div class="info-item">
              <span class="label">专业</span>
              <span class="value">{{ profile?.major }}</span>
            </div>
            <div class="info-item">
              <span class="label">年级</span>
              <span class="value">{{ profile?.grade }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-card>
    
    <!-- 快捷入口 -->
    <div class="quick-links">
      <div class="quick-link-card" @click="$router.push('/student/schedule')">
        <div class="icon-wrapper primary">
          <el-icon :size="28"><Calendar /></el-icon>
        </div>
        <span>我的课表</span>
      </div>
      
      <div class="quick-link-card" @click="$router.push('/student/grades')">
        <div class="icon-wrapper success">
          <el-icon :size="28"><Document /></el-icon>
        </div>
        <span>成绩查询</span>
      </div>
      
      <div class="quick-link-card" @click="$router.push('/student/evaluation')">
        <div class="icon-wrapper warning">
          <el-icon :size="28"><Star /></el-icon>
        </div>
        <span>评教</span>
      </div>
      
      <div class="quick-link-card" @click="$router.push('/student/thesis')">
        <div class="icon-wrapper info">
          <el-icon :size="28"><Reading /></el-icon>
        </div>
        <span>毕业设计</span>
      </div>
    </div>
    
    <!-- 今日课程 -->
    <el-card class="today-card">
      <template #header>
        <div class="card-header">
          <span>今日课程</span>
          <el-button text @click="$router.push('/student/schedule')">查看全部</el-button>
        </div>
      </template>
      
      <div v-if="todayCourses.length > 0" class="course-list">
        <div v-for="course in todayCourses" :key="course.id" class="course-item">
          <div class="course-time">
            <span class="period">第 {{ course.start_period }}-{{ course.end_period }} 节</span>
          </div>
          <div class="course-info">
            <h4>{{ course.course_name }}</h4>
            <p>
              <el-icon><Location /></el-icon>
              {{ course.classroom }}
              <el-icon style="margin-left: 12px"><User /></el-icon>
              {{ course.teacher_name }}
            </p>
          </div>
        </div>
      </div>
      <el-empty v-else description="今日没有课程" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Calendar, Document, Star, Reading, Location, User } from '@element-plus/icons-vue'
import { studentApi } from '../../api'

const profile = ref(null)
const schedule = ref([])

const statusTagType = computed(() => {
  const status = profile.value?.status
  if (status === 'normal') return 'success'
  if (status === 'suspended') return 'warning'
  return 'info'
})

const todayCourses = computed(() => {
  const today = new Date().getDay() || 7 // 0 = Sunday -> 7
  return schedule.value.filter(s => s.weekday === today)
})

onMounted(async () => {
  try {
    const [profileRes, scheduleRes] = await Promise.all([
      studentApi.getProfile(),
      studentApi.getSchedule()
    ])
    profile.value = profileRes.data
    schedule.value = scheduleRes.data
  } catch (error) {
    console.error('Error loading data:', error)
  }
})
</script>

<style scoped>
.home-page {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.profile-card {
  margin-bottom: 24px;
}

.profile-content {
  display: flex;
  gap: 32px;
  align-items: center;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 32px;
  font-weight: 600;
}

.status-tag {
  font-weight: 500;
}

.info-section h2 {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 16px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item .label {
  font-size: 12px;
  color: #909399;
}

.info-item .value {
  font-size: 15px;
  font-weight: 500;
  color: #2c3e50;
}

.quick-links {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.quick-link-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.quick-link-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.icon-wrapper.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.icon-wrapper.success {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.icon-wrapper.warning {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.icon-wrapper.info {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.quick-link-card span {
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
}

.today-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.course-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
  transition: all 0.3s;
}

.course-item:hover {
  background: #f0f2f5;
}

.course-time {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 100px;
  padding: 8px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
}

.course-time .period {
  font-size: 14px;
  font-weight: 500;
}

.course-info h4 {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.course-info p {
  font-size: 14px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 4px;
}

@media (max-width: 768px) {
  .profile-content {
    flex-direction: column;
    text-align: center;
  }
  
  .quick-links {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
