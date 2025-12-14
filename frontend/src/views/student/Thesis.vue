<template>
  <div class="thesis-page">
    <h1 class="page-title">毕业设计</h1>
    
    <el-tabs v-model="activeTab">
      <!-- 我的课题 -->
      <el-tab-pane label="我的课题" name="my">
        <el-card>
          <div v-if="myTopic" class="my-topic">
            <div class="topic-header">
              <el-tag :type="myTopic.status === 'confirmed' ? 'success' : 'warning'">
                {{ myTopic.status === 'confirmed' ? '已确认' : '待审批' }}
              </el-tag>
            </div>
            
            <h2>{{ myTopic.topic?.title }}</h2>
            <p class="description">{{ myTopic.topic?.description }}</p>
            
            <div class="topic-info">
              <div class="info-item">
                <span class="label">指导教师</span>
                <span class="value">{{ myTopic.teacher_name }}</span>
              </div>
            </div>
          </div>
          
          <el-empty v-else description="您还未选择毕设课题">
            <el-button type="primary" @click="activeTab = 'topics'">
              浏览课题
            </el-button>
          </el-empty>
        </el-card>
        
        <!-- 过程文档 -->
        <el-card v-if="myTopic?.status === 'confirmed'" class="documents-card">
          <template #header>
            <div class="card-header">
              <span>过程文档</span>
              <el-button type="primary" size="small" @click="openDocDialog">
                <el-icon><Upload /></el-icon>
                上传文档
              </el-button>
            </div>
          </template>
          
          <el-table :data="documents" stripe>
            <el-table-column prop="type" label="文档类型" width="150" />
            <el-table-column prop="file_name" label="文件名" />
            <el-table-column prop="submitted_at" label="提交时间" width="120" />
            <el-table-column label="状态" width="100" align="center">
              <template #default="{ row }">
                <el-tag type="success">{{ row.status === 'submitted' ? '已提交' : row.status }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
          
          <el-empty v-if="documents.length === 0" description="暂无文档" />
        </el-card>
      </el-tab-pane>
      
      <!-- 课题列表 -->
      <el-tab-pane label="课题列表" name="topics">
        <el-card>
          <div class="topics-list">
            <div v-for="topic in topics" :key="topic.id" class="topic-item">
              <div class="topic-content">
                <h3>{{ topic.title }}</h3>
                <p class="description">{{ topic.description }}</p>
                <div class="topic-meta">
                  <span>
                    <el-icon><User /></el-icon>
                    {{ topic.teacher_name }}
                  </span>
                  <span>
                    <el-icon><OfficeBuilding /></el-icon>
                    {{ topic.department }}
                  </span>
                  <span>
                    <el-icon><UserFilled /></el-icon>
                    限 {{ topic.max_students }} 人
                  </span>
                </div>
              </div>
              <div class="topic-action">
                <el-button 
                  v-if="!topic.applied"
                  type="primary" 
                  @click="applyTopic(topic)"
                >
                  申请课题
                </el-button>
                <el-tag v-else type="info">已申请</el-tag>
              </div>
            </div>
          </div>
          
          <el-empty v-if="topics.length === 0" description="暂无可选课题" />
        </el-card>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 上传文档对话框 -->
    <el-dialog v-model="docDialogVisible" title="上传过程文档" width="500px">
      <el-form :model="docForm" label-width="80px">
        <el-form-item label="文档类型">
          <el-select v-model="docForm.type" placeholder="请选择">
            <el-option label="开题报告" value="开题报告" />
            <el-option label="中期报告" value="中期报告" />
            <el-option label="毕业论文" value="毕业论文" />
            <el-option label="答辩PPT" value="答辩PPT" />
          </el-select>
        </el-form-item>
        <el-form-item label="文件名">
          <el-input v-model="docForm.file_name" placeholder="例如: 开题报告_张三.pdf" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="docDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitDocument">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, OfficeBuilding, UserFilled, Upload } from '@element-plus/icons-vue'
import { studentApi } from '../../api'

const activeTab = ref('my')
const myTopic = ref(null)
const topics = ref([])
const documents = ref([])
const docDialogVisible = ref(false)

const docForm = reactive({
  type: '',
  file_name: ''
})

const applyTopic = async (topic) => {
  try {
    await ElMessageBox.confirm(
      `确定要申请课题「${topic.title}」吗？`,
      '申请确认',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'info' }
    )
    
    await studentApi.applyTopic(topic.id)
    ElMessage.success('申请已提交')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Apply topic error:', error)
    }
  }
}

const openDocDialog = () => {
  docForm.type = ''
  docForm.file_name = ''
  docDialogVisible.value = true
}

const submitDocument = async () => {
  if (!docForm.type || !docForm.file_name) {
    ElMessage.warning('请填写完整信息')
    return
  }
  
  try {
    await studentApi.submitDocument(docForm.type, docForm.file_name)
    ElMessage.success('文档提交成功')
    docDialogVisible.value = false
    loadDocuments()
  } catch (error) {
    console.error('Submit document error:', error)
  }
}

const loadData = async () => {
  try {
    const [topicRes, topicsRes] = await Promise.all([
      studentApi.getMyTopic(),
      studentApi.getTopics()
    ])
    myTopic.value = topicRes.data
    topics.value = topicsRes.data
    
    if (myTopic.value?.status === 'confirmed') {
      loadDocuments()
    }
  } catch (error) {
    console.error('Error loading data:', error)
  }
}

const loadDocuments = async () => {
  try {
    const res = await studentApi.getDocuments()
    documents.value = res.data
  } catch (error) {
    console.error('Error loading documents:', error)
  }
}

onMounted(loadData)
</script>

<style scoped>
.thesis-page {
  animation: fadeIn 0.3s ease;
}

.my-topic {
  padding: 20px;
}

.my-topic h2 {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 16px 0 12px;
}

.my-topic .description {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 20px;
}

.topic-info {
  display: flex;
  gap: 32px;
}

.topic-info .info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.topic-info .label {
  font-size: 12px;
  color: #909399;
}

.topic-info .value {
  font-weight: 500;
  color: #2c3e50;
}

.documents-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.topics-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.topic-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  transition: all 0.3s;
}

.topic-item:hover {
  background: #f0f2f5;
}

.topic-content h3 {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.topic-content .description {
  font-size: 14px;
  color: #606266;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.topic-meta {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: #909399;
}

.topic-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.topic-action {
  flex-shrink: 0;
  margin-left: 20px;
}
</style>
