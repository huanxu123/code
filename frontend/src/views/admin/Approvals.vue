<template>
  <div class="approvals-page">
    <h1 class="page-title">审批中心</h1>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>待审批事项</span>
          <el-tag type="warning">{{ approvals.length }} 项待处理</el-tag>
        </div>
      </template>
      
      <el-table :data="approvals" stripe>
        <el-table-column prop="type_name" label="类型" width="100" />
        <el-table-column prop="subtype" label="详情" width="150" />
        <el-table-column prop="applicant" label="申请人" width="100" />
        <el-table-column prop="reason" label="原因/描述" />
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
              <el-button type="success" size="small" @click="approve(row)">
                通过
              </el-button>
              <el-button type="danger" size="small" @click="reject(row)">
                拒绝
              </el-button>
            </template>
            <span v-else class="text-muted">已处理</span>
          </template>
        </el-table-column>
      </el-table>
      
      <el-empty v-if="approvals.length === 0" description="暂无待审批事项" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminApi } from '../../api'

const approvals = ref([])

const getStatusType = (status) => {
  const map = { pending: 'warning', approved: 'success', rejected: 'danger' }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = { pending: '待审批', approved: '已通过', rejected: '已拒绝' }
  return map[status] || status
}

const approve = async (item) => {
  try {
    await ElMessageBox.confirm(`确定要通过此 ${item.type_name} 申请吗？`, '确认通过', {
      confirmButtonText: '确定', cancelButtonText: '取消', type: 'info'
    })
    await adminApi.processApproval(item.type, item.id, 'approve')
    ElMessage.success('已通过')
    loadApprovals()
  } catch (error) {
    if (error !== 'cancel') console.error('Approve error:', error)
  }
}

const reject = async (item) => {
  try {
    await ElMessageBox.confirm(`确定要拒绝此 ${item.type_name} 申请吗？`, '确认拒绝', {
      confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'
    })
    await adminApi.processApproval(item.type, item.id, 'reject')
    ElMessage.success('已拒绝')
    loadApprovals()
  } catch (error) {
    if (error !== 'cancel') console.error('Reject error:', error)
  }
}

const loadApprovals = async () => {
  try {
    const res = await adminApi.getApprovals()
    approvals.value = res.data
  } catch (error) {
    console.error('Error loading approvals:', error)
  }
}

onMounted(loadApprovals)
</script>

<style scoped>
.approvals-page { animation: fadeIn 0.3s ease; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.text-muted { color: #909399; }
</style>
