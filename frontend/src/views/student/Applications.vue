<template>
  <div class="applications-page">
    <h1 class="page-title">学籍异动 / 重修申请</h1>
    
    <el-tabs v-model="activeTab">
      <!-- 学籍异动 -->
      <el-tab-pane label="学籍异动" name="status">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>学籍异动申请</span>
              <el-button type="primary" @click="openStatusDialog">
                <el-icon><Plus /></el-icon>
                新建申请
              </el-button>
            </div>
          </template>
          
          <el-table :data="statusChanges" stripe>
            <el-table-column prop="type" label="类型" width="120" />
            <el-table-column prop="reason" label="申请原因" />
            <el-table-column prop="created_at" label="申请时间" width="120" />
            <el-table-column label="状态" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status_text }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
          
          <el-empty v-if="statusChanges.length === 0" description="暂无申请记录" />
        </el-card>
      </el-tab-pane>
      
      <!-- 重修申请 -->
      <el-tab-pane label="重修申请" name="retake">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>重修申请</span>
              <el-button type="primary" @click="openRetakeDialog">
                <el-icon><Plus /></el-icon>
                新建申请
              </el-button>
            </div>
          </template>
          
          <el-table :data="retakes" stripe>
            <el-table-column prop="course_code" label="课程代码" width="120" />
            <el-table-column prop="course_name" label="课程名称" />
            <el-table-column prop="reason" label="申请原因" />
            <el-table-column prop="created_at" label="申请时间" width="120" />
            <el-table-column label="状态" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status_text }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
          
          <el-empty v-if="retakes.length === 0" description="暂无申请记录" />
        </el-card>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 学籍异动申请对话框 -->
    <el-dialog v-model="statusDialogVisible" title="学籍异动申请" width="500px">
      <el-form :model="statusForm" label-width="80px">
        <el-form-item label="异动类型">
          <el-select v-model="statusForm.type" placeholder="请选择">
            <el-option label="休学" value="休学" />
            <el-option label="复学" value="复学" />
            <el-option label="转专业" value="转专业" />
            <el-option label="退学" value="退学" />
          </el-select>
        </el-form-item>
        <el-form-item label="申请原因">
          <el-input 
            v-model="statusForm.reason" 
            type="textarea" 
            :rows="4"
            placeholder="请详细说明申请原因"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="statusDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitStatusChange">提交申请</el-button>
      </template>
    </el-dialog>
    
    <!-- 重修申请对话框 -->
    <el-dialog v-model="retakeDialogVisible" title="重修申请" width="500px">
      <el-form :model="retakeForm" label-width="80px">
        <el-form-item label="课程">
          <el-select v-model="retakeForm.course_id" placeholder="请选择课程">
            <el-option 
              v-for="course in courses" 
              :key="course.id" 
              :label="course.name" 
              :value="course.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="申请原因">
          <el-input 
            v-model="retakeForm.reason" 
            type="textarea" 
            :rows="4"
            placeholder="请说明重修原因"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="retakeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitRetake">提交申请</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { studentApi } from '../../api'

const activeTab = ref('status')
const statusChanges = ref([])
const retakes = ref([])
const courses = ref([
  { id: 1, name: '程序设计基础' },
  { id: 2, name: '数据结构' },
  { id: 3, name: '操作系统' },
  { id: 4, name: '计算机网络' },
  { id: 5, name: '数据库原理' }
])

const statusDialogVisible = ref(false)
const retakeDialogVisible = ref(false)

const statusForm = reactive({
  type: '',
  reason: ''
})

const retakeForm = reactive({
  course_id: null,
  reason: ''
})

const getStatusType = (status) => {
  if (status === 'approved') return 'success'
  if (status === 'rejected') return 'danger'
  return 'warning'
}

const openStatusDialog = () => {
  statusForm.type = ''
  statusForm.reason = ''
  statusDialogVisible.value = true
}

const openRetakeDialog = () => {
  retakeForm.course_id = null
  retakeForm.reason = ''
  retakeDialogVisible.value = true
}

const submitStatusChange = async () => {
  if (!statusForm.type || !statusForm.reason) {
    ElMessage.warning('请填写完整信息')
    return
  }
  
  try {
    await studentApi.submitStatusChange(statusForm.type, statusForm.reason)
    ElMessage.success('申请已提交')
    statusDialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('Submit error:', error)
  }
}

const submitRetake = async () => {
  if (!retakeForm.course_id || !retakeForm.reason) {
    ElMessage.warning('请填写完整信息')
    return
  }
  
  try {
    await studentApi.submitRetake(retakeForm.course_id, retakeForm.reason)
    ElMessage.success('申请已提交')
    retakeDialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('Submit error:', error)
  }
}

const loadData = async () => {
  try {
    const [statusRes, retakeRes] = await Promise.all([
      studentApi.getStatusChanges(),
      studentApi.getRetakes()
    ])
    statusChanges.value = statusRes.data
    retakes.value = retakeRes.data
  } catch (error) {
    console.error('Error loading data:', error)
  }
}

onMounted(loadData)
</script>

<style scoped>
.applications-page {
  animation: fadeIn 0.3s ease;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
