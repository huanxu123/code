<template>
  <div class="home-page">
    <h1 class="page-title">数据概览</h1>
    
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="icon primary">
          <el-icon :size="28"><User /></el-icon>
        </div>
        <div class="info">
          <h3>{{ stats.student_count }}</h3>
          <p>学生总数</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="icon success">
          <el-icon :size="28"><UserFilled /></el-icon>
        </div>
        <div class="info">
          <h3>{{ stats.teacher_count }}</h3>
          <p>教师总数</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="icon info">
          <el-icon :size="28"><Reading /></el-icon>
        </div>
        <div class="info">
          <h3>{{ stats.course_count }}</h3>
          <p>课程总数</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="icon warning">
          <el-icon :size="28"><Location /></el-icon>
        </div>
        <div class="info">
          <h3>{{ stats.classroom_count }}</h3>
          <p>教室总数</p>
        </div>
      </div>
      
      <div class="stat-card pending">
        <div class="icon danger">
          <el-icon :size="28"><Bell /></el-icon>
        </div>
        <div class="info">
          <h3>{{ stats.pending_approvals }}</h3>
          <p>待审批事项</p>
        </div>
        <el-button type="primary" size="small" @click="$router.push('/admin/approvals')">
          去处理
        </el-button>
      </div>
    </div>
    
    <!-- 快捷操作 -->
    <el-card class="quick-actions">
      <template #header>
        <span>快捷操作</span>
      </template>
      
      <div class="actions-grid">
        <div class="action-item" @click="$router.push('/admin/students')">
          <el-icon :size="32"><User /></el-icon>
          <span>学生管理</span>
        </div>
        <div class="action-item" @click="$router.push('/admin/teachers')">
          <el-icon :size="32"><UserFilled /></el-icon>
          <span>教师管理</span>
        </div>
        <div class="action-item" @click="$router.push('/admin/courses')">
          <el-icon :size="32"><Reading /></el-icon>
          <span>课程管理</span>
        </div>
        <div class="action-item" @click="$router.push('/admin/schedule')">
          <el-icon :size="32"><Calendar /></el-icon>
          <span>排课管理</span>
        </div>
        <div class="action-item" @click="$router.push('/admin/exams')">
          <el-icon :size="32"><Document /></el-icon>
          <span>考试安排</span>
        </div>
        <div class="action-item" @click="$router.push('/admin/approvals')">
          <el-icon :size="32"><Checked /></el-icon>
          <span>审批中心</span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { User, UserFilled, Reading, Location, Bell, Calendar, Document, Checked } from '@element-plus/icons-vue'
import { adminApi } from '../../api'

const stats = ref({
  student_count: 0,
  teacher_count: 0,
  course_count: 0,
  classroom_count: 0,
  pending_approvals: 0
})

onMounted(async () => {
  try {
    const res = await adminApi.getStatistics()
    stats.value = res.data
  } catch (error) {
    console.error('Error loading stats:', error)
  }
})
</script>

<style scoped>
.home-page {
  animation: fadeIn 0.3s ease;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-card.pending {
  flex-wrap: wrap;
}

.stat-card.pending .el-button {
  margin-left: auto;
}

.stat-card .icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.stat-card .icon.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card .icon.success {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.stat-card .icon.info {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-card .icon.warning {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-card .icon.danger {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
}

.stat-card .info h3 {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
}

.stat-card .info p {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: #f8f9fa;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  gap: 12px;
}

.action-item:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-item span {
  font-size: 14px;
  font-weight: 500;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .actions-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
