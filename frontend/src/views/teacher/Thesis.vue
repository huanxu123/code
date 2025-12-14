<template>
  <div class="thesis-page">
    <h1 class="page-title">毕设管理</h1>
    
    <el-tabs v-model="activeTab">
      <!-- 课题管理 -->
      <el-tab-pane label="我的课题" name="topics">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>课题列表</span>
              <el-button type="primary" @click="openTopicDialog">
                <el-icon><Plus /></el-icon>
                新建课题
              </el-button>
            </div>
          </template>
          
          <el-table :data="topics" stripe>
            <el-table-column prop="title" label="课题名称" />
            <el-table-column prop="description" label="课题描述" show-overflow-tooltip />
            <el-table-column prop="max_students" label="限选人数" width="100" align="center" />
            <el-table-column prop="selected_count" label="已选人数" width="100" align="center" />
            <el-table-column label="状态" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="row.status === 'open' ? 'success' : 'info'">
                  {{ row.status === 'open' ? '开放中' : '已关闭' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" align="center">
              <template #default="{ row }">
                <el-button type="primary" size="small" text @click="editTopic(row)">
                  编辑
                </el-button>
                <el-button 
                  :type="row.status === 'open' ? 'warning' : 'success'" 
                  size="small" 
                  text
                  @click="toggleTopicStatus(row)"
                >
                  {{ row.status === 'open' ? '关闭' : '开放' }}
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
      
      <!-- 申请审批 -->
      <el-tab-pane label="申请审批" name="applications">
        <el-card>
          <el-table :data="applications" stripe>
            <el-table-column prop="topic_title" label="课题名称" />
            <el-table-column prop="student_name" label="申请学生" width="100" />
            <el-table-column prop="student_no" label="学号" width="120" />
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
                  <el-button type="success" size="small" @click="approveApplication(row)">
                    通过
                  </el-button>
                  <el-button type="danger" size="small" @click="rejectApplication(row)">
                    拒绝
                  </el-button>
                </template>
                <span v-else class="text-muted">已处理</span>
              </template>
            </el-table-column>
          </el-table>
          
          <el-empty v-if="applications.length === 0" description="暂无申请" />
        </el-card>
      </el-tab-pane>
      
      <!-- 指导学生 -->
      <el-tab-pane label="指导学生" name="students">
        <el-card>
          <el-table :data="students" stripe>
            <el-table-column prop="student_no" label="学号" width="120" />
            <el-table-column prop="student_name" label="姓名" width="100" />
            <el-table-column prop="topic_title" label="课题名称" />
            <el-table-column label="状态" width="100" align="center">
              <template #default="{ row }">
                <el-tag type="success">进行中</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="过程文档" width="200">
              <template #default="{ row }">
                <el-tag 
                  v-for="doc in row.documents" 
                  :key="doc.id" 
                  size="small" 
                  style="margin-right: 4px"
                >
                  {{ doc.type }}
                </el-tag>
                <span v-if="!row.documents?.length" class="text-muted">暂无</span>
              </template>
            </el-table-column>
          </el-table>
          
          <el-empty v-if="students.length === 0" description="暂无指导学生" />
        </el-card>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 课题编辑对话框 -->
    <el-dialog v-model="topicDialogVisible" :title="isEdit ? '编辑课题' : '新建课题'" width="600px">
      <el-form :model="topicForm" label-width="100px">
        <el-form-item label="课题名称">
          <el-input v-model="topicForm.title" placeholder="请输入课题名称" />
        </el-form-item>
        <el-form-item label="课题描述">
          <el-input 
            v-model="topicForm.description" 
            type="textarea" 
            :rows="4"
            placeholder="请输入课题描述"
          />
        </el-form-item>
        <el-form-item label="限选人数">
          <el-input-number v-model="topicForm.max_students" :min="1" :max="10" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="topicDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveTopic">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { teacherApi } from '../../api'

const activeTab = ref('topics')
const topics = ref([])
const applications = ref([])
const students = ref([])
const topicDialogVisible = ref(false)
const isEdit = ref(false)
const editingTopicId = ref(null)

const topicForm = reactive({
  title: '',
  description: '',
  max_students: 1
})

const getStatusType = (status) => {
  if (status === 'approved') return 'success'
  if (status === 'rejected') return 'danger'
  return 'warning'
}

const getStatusText = (status) => {
  const map = {
    pending: '待审批',
    approved: '已通过',
    rejected: '已拒绝'
  }
  return map[status] || status
}

const openTopicDialog = () => {
  isEdit.value = false
  topicForm.title = ''
  topicForm.description = ''
  topicForm.max_students = 1
  topicDialogVisible.value = true
}

const editTopic = (topic) => {
  isEdit.value = true
  editingTopicId.value = topic.id
  topicForm.title = topic.title
  topicForm.description = topic.description
  topicForm.max_students = topic.max_students
  topicDialogVisible.value = true
}

const saveTopic = async () => {
  if (!topicForm.title || !topicForm.description) {
    ElMessage.warning('请填写完整信息')
    return
  }
  
  try {
    if (isEdit.value) {
      await teacherApi.updateTopic(editingTopicId.value, topicForm)
      ElMessage.success('课题更新成功')
    } else {
      await teacherApi.createTopic(topicForm.title, topicForm.description, topicForm.max_students)
      ElMessage.success('课题创建成功')
    }
    topicDialogVisible.value = false
    loadTopics()
  } catch (error) {
    console.error('Save topic error:', error)
  }
}

const toggleTopicStatus = async (topic) => {
  try {
    const newStatus = topic.status === 'open' ? 'closed' : 'open'
    await teacherApi.updateTopic(topic.id, { status: newStatus })
    ElMessage.success('状态更新成功')
    loadTopics()
  } catch (error) {
    console.error('Toggle status error:', error)
  }
}

const approveApplication = async (app) => {
  try {
    await ElMessageBox.confirm(
      `确定要通过 ${app.student_name} 的申请吗？`,
      '确认通过',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'info' }
    )
    
    await teacherApi.processTopicApplication(app.id, 'approve')
    ElMessage.success('已通过申请')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Approve error:', error)
    }
  }
}

const rejectApplication = async (app) => {
  try {
    await ElMessageBox.confirm(
      `确定要拒绝 ${app.student_name} 的申请吗？`,
      '确认拒绝',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
    )
    
    await teacherApi.processTopicApplication(app.id, 'reject')
    ElMessage.success('已拒绝申请')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Reject error:', error)
    }
  }
}

const loadTopics = async () => {
  try {
    const res = await teacherApi.getTopics()
    topics.value = res.data
  } catch (error) {
    console.error('Error loading topics:', error)
  }
}

const loadData = async () => {
  try {
    const [topicsRes, appsRes, studentsRes] = await Promise.all([
      teacherApi.getTopics(),
      teacherApi.getTopicApplications(),
      teacherApi.getThesisStudents()
    ])
    topics.value = topicsRes.data
    applications.value = appsRes.data
    students.value = studentsRes.data
  } catch (error) {
    console.error('Error loading data:', error)
  }
}

onMounted(loadData)
</script>

<style scoped>
.thesis-page {
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
