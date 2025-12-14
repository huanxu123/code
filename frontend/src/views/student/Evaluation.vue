<template>
  <div class="evaluation-page">
    <h1 class="page-title">评教</h1>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>待评教课程</span>
          <el-tag type="warning">{{ evaluations.length }} 门待评</el-tag>
        </div>
      </template>
      
      <div v-if="evaluations.length > 0" class="evaluation-list">
        <div v-for="item in evaluations" :key="item.id" class="evaluation-item">
          <div class="course-info">
            <h3>{{ item.course_name }}</h3>
            <p>
              <el-icon><User /></el-icon>
              {{ item.teacher_name }}
              <span class="course-code">{{ item.course_code }}</span>
            </p>
          </div>
          <el-button type="primary" @click="openEvaluateDialog(item)">
            立即评教
          </el-button>
        </div>
      </div>
      
      <el-empty v-else description="暂无待评教课程" />
    </el-card>
    
    <!-- 评教对话框 -->
    <el-dialog v-model="dialogVisible" title="课程评教" width="600px">
      <div class="evaluate-form">
        <div class="course-header">
          <h3>{{ currentEvaluation?.course_name }}</h3>
          <p>授课教师：{{ currentEvaluation?.teacher_name }}</p>
        </div>
        
        <div class="rating-section">
          <label>总体评分</label>
          <div class="rating-wrapper">
            <el-rate 
              v-model="evaluateForm.rating" 
              :texts="['很差', '较差', '一般', '较好', '很好']"
              show-text
              size="large"
            />
          </div>
        </div>
        
        <div class="comment-section">
          <label>评价内容（可选）</label>
          <el-input
            v-model="evaluateForm.comment"
            type="textarea"
            :rows="4"
            placeholder="请输入您对该课程的评价和建议..."
          />
        </div>
      </div>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitEvaluation">提交评教</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'
import { studentApi } from '../../api'

const evaluations = ref([])
const dialogVisible = ref(false)
const currentEvaluation = ref(null)
const evaluateForm = reactive({
  rating: 5,
  comment: ''
})

const openEvaluateDialog = (item) => {
  currentEvaluation.value = item
  evaluateForm.rating = 5
  evaluateForm.comment = ''
  dialogVisible.value = true
}

const submitEvaluation = async () => {
  if (evaluateForm.rating === 0) {
    ElMessage.warning('请选择评分')
    return
  }
  
  try {
    await studentApi.submitEvaluation(
      currentEvaluation.value.id,
      evaluateForm.rating,
      evaluateForm.comment
    )
    ElMessage.success('评教提交成功')
    dialogVisible.value = false
    loadEvaluations()
  } catch (error) {
    console.error('Submit evaluation error:', error)
  }
}

const loadEvaluations = async () => {
  try {
    const res = await studentApi.getEvaluations()
    evaluations.value = res.data
  } catch (error) {
    console.error('Error loading evaluations:', error)
  }
}

onMounted(loadEvaluations)
</script>

<style scoped>
.evaluation-page {
  animation: fadeIn 0.3s ease;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.evaluation-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.evaluation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  transition: all 0.3s;
}

.evaluation-item:hover {
  background: #f0f2f5;
}

.course-info h3 {
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

.course-code {
  margin-left: 16px;
  color: #c0c4cc;
}

.evaluate-form {
  padding: 0 20px;
}

.course-header {
  text-align: center;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
  margin-bottom: 24px;
}

.course-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.course-header p {
  color: #909399;
}

.rating-section,
.comment-section {
  margin-bottom: 24px;
}

.rating-section label,
.comment-section label {
  display: block;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 12px;
}

.rating-wrapper {
  display: flex;
  justify-content: center;
}

.rating-wrapper :deep(.el-rate) {
  height: auto;
}

.rating-wrapper :deep(.el-rate__icon) {
  font-size: 32px !important;
}
</style>
