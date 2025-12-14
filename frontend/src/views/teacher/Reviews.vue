<template>
  <div class="reviews-page">
    <h1 class="page-title">成绩复核</h1>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>待处理的复核申请</span>
        </div>
      </template>
      
      <el-table :data="reviews" stripe>
        <el-table-column prop="student_name" label="学生姓名" width="100" />
        <el-table-column prop="course_name" label="课程" />
        <el-table-column prop="original_score" label="原成绩" width="100" align="center" />
        <el-table-column prop="reason" label="申请原因" />
        <el-table-column prop="created_at" label="申请时间" width="120" />
        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template #default="{ row }">
            <template v-if="row.status === 'pending'">
              <el-button type="success" size="small" @click="openApproveDialog(row)">
                通过
              </el-button>
              <el-button type="danger" size="small" @click="rejectReview(row)">
                拒绝
              </el-button>
            </template>
            <span v-else class="text-muted">已处理</span>
          </template>
        </el-table-column>
      </el-table>
      
      <el-empty v-if="reviews.length === 0" description="暂无复核申请" />
    </el-card>
    
    <!-- 通过对话框 -->
    <el-dialog v-model="approveDialogVisible" title="通过复核申请" width="500px">
      <el-form :model="approveForm" label-width="100px">
        <el-form-item label="学生">
          <el-input :value="currentReview?.student_name" disabled />
        </el-form-item>
        <el-form-item label="课程">
          <el-input :value="currentReview?.course_name" disabled />
        </el-form-item>
        <el-form-item label="原成绩">
          <el-input :value="currentReview?.original_score" disabled />
        </el-form-item>
        <el-form-item label="修改后成绩">
          <el-input-number 
            v-model="approveForm.newScore" 
            :min="0" 
            :max="100" 
            :precision="0"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="approveDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="approveReview">确认通过</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { teacherApi } from '../../api'

const reviews = ref([])
const approveDialogVisible = ref(false)
const currentReview = ref(null)
const approveForm = reactive({
  newScore: 0
})

const getStatusType = (status) => {
  if (status === 'approved') return 'success'
  if (status === 'rejected') return 'danger'
  return 'warning'
}

const getStatusText = (status) => {
  const map = {
    pending: '待处理',
    approved: '已通过',
    rejected: '已拒绝'
  }
  return map[status] || status
}

const openApproveDialog = (review) => {
  currentReview.value = review
  approveForm.newScore = review.original_score
  approveDialogVisible.value = true
}

const approveReview = async () => {
  try {
    await teacherApi.processReview(currentReview.value.id, 'approve', approveForm.newScore)
    ElMessage.success('复核已通过')
    approveDialogVisible.value = false
    loadReviews()
  } catch (error) {
    console.error('Approve review error:', error)
  }
}

const rejectReview = async (review) => {
  try {
    await ElMessageBox.confirm(
      '确定要拒绝此复核申请吗？',
      '确认拒绝',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
    )
    
    await teacherApi.processReview(review.id, 'reject')
    ElMessage.success('已拒绝复核申请')
    loadReviews()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Reject review error:', error)
    }
  }
}

const loadReviews = async () => {
  try {
    const res = await teacherApi.getReviews()
    reviews.value = res.data
  } catch (error) {
    console.error('Error loading reviews:', error)
  }
}

onMounted(loadReviews)
</script>

<style scoped>
.reviews-page {
  animation: fadeIn 0.3s ease;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text-muted {
  color: #909399;
}
</style>
