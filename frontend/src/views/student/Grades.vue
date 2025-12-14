<template>
  <div class="grades-page">
    <h1 class="page-title">成绩查询</h1>
    
    <!-- 成绩统计 -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="icon primary">
          <el-icon :size="24"><Document /></el-icon>
        </div>
        <div class="info">
          <h3>{{ gradesSummary.total_credits }}</h3>
          <p>已修学分</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="icon success">
          <el-icon :size="24"><TrendCharts /></el-icon>
        </div>
        <div class="info">
          <h3>{{ gradesSummary.avg_gpa }}</h3>
          <p>平均绩点</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="icon info">
          <el-icon :size="24"><Tickets /></el-icon>
        </div>
        <div class="info">
          <h3>{{ grades.length }}</h3>
          <p>课程数量</p>
        </div>
      </div>
    </div>
    
    <!-- 成绩列表 -->
    <el-card>
      <template #header>
        <div class="card-header">
          <span>成绩明细</span>
        </div>
      </template>
      
      <el-table :data="grades" stripe>
        <el-table-column prop="semester" label="学期" width="140" />
        <el-table-column prop="course_code" label="课程代码" width="120" />
        <el-table-column prop="course_name" label="课程名称" />
        <el-table-column prop="credit" label="学分" width="80" align="center" />
        <el-table-column label="成绩" width="100" align="center">
          <template #default="{ row }">
            <span :class="getScoreClass(row.score)">{{ row.score }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="gpa" label="绩点" width="80" align="center" />
        <el-table-column label="操作" width="120" align="center">
          <template #default="{ row }">
            <el-button 
              type="primary" 
              size="small" 
              text
              @click="openReviewDialog(row)"
            >
              申请复核
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 复核申请对话框 -->
    <el-dialog v-model="reviewDialogVisible" title="成绩复核申请" width="500px">
      <el-form :model="reviewForm" label-width="80px">
        <el-form-item label="课程">
          <el-input :value="selectedGrade?.course_name" disabled />
        </el-form-item>
        <el-form-item label="当前成绩">
          <el-input :value="selectedGrade?.score" disabled />
        </el-form-item>
        <el-form-item label="申请理由">
          <el-input 
            v-model="reviewForm.reason" 
            type="textarea" 
            :rows="4"
            placeholder="请详细说明申请复核的原因"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="reviewDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReview">提交申请</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, TrendCharts, Tickets } from '@element-plus/icons-vue'
import { studentApi } from '../../api'

const grades = ref([])
const gradesSummary = ref({ total_credits: 0, avg_gpa: 0 })
const reviewDialogVisible = ref(false)
const selectedGrade = ref(null)
const reviewForm = reactive({
  reason: ''
})

const getScoreClass = (score) => {
  if (score >= 90) return 'score-excellent'
  if (score >= 80) return 'score-good'
  if (score >= 60) return 'score-pass'
  return 'score-fail'
}

const openReviewDialog = (grade) => {
  selectedGrade.value = grade
  reviewForm.reason = ''
  reviewDialogVisible.value = true
}

const submitReview = async () => {
  if (!reviewForm.reason.trim()) {
    ElMessage.warning('请填写申请理由')
    return
  }
  
  try {
    await studentApi.submitGradeReview(selectedGrade.value.id, reviewForm.reason)
    ElMessage.success('复核申请已提交')
    reviewDialogVisible.value = false
  } catch (error) {
    console.error('Submit review error:', error)
  }
}

onMounted(async () => {
  try {
    const res = await studentApi.getGrades()
    grades.value = res.data.grades
    gradesSummary.value = res.data.summary
  } catch (error) {
    console.error('Error loading grades:', error)
  }
})
</script>

<style scoped>
.grades-page {
  animation: fadeIn 0.3s ease;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
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

.stat-card .icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
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

.score-excellent {
  color: #67c23a;
  font-weight: 600;
}

.score-good {
  color: #409eff;
  font-weight: 600;
}

.score-pass {
  color: #e6a23c;
  font-weight: 600;
}

.score-fail {
  color: #f56c6c;
  font-weight: 600;
}

@media (max-width: 768px) {
  .stats-row {
    grid-template-columns: 1fr;
  }
}
</style>
