<template>
  <div class="students-page">
    <h1 class="page-title">学生管理</h1>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>学生列表</span>
          <el-button type="primary" @click="openDialog">
            <el-icon><Plus /></el-icon>
            添加学生
          </el-button>
        </div>
      </template>
      
      <el-table :data="students" stripe>
        <el-table-column prop="student_no" label="学号" width="140" />
        <el-table-column prop="name" label="姓名" width="100" />
        <el-table-column prop="class_name" label="班级" width="150" />
        <el-table-column prop="major" label="专业" />
        <el-table-column prop="grade" label="年级" width="100" />
        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center">
          <template #default="{ row }">
            <el-button type="primary" size="small" text @click="editStudent(row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" text @click="deleteStudent(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑学生' : '添加学生'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="学号">
          <el-input v-model="form.student_no" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="班级">
          <el-input v-model="form.class_name" />
        </el-form-item>
        <el-form-item label="专业">
          <el-input v-model="form.major" />
        </el-form-item>
        <el-form-item label="年级">
          <el-input v-model="form.grade" />
        </el-form-item>
        <el-form-item v-if="isEdit" label="状态">
          <el-select v-model="form.status">
            <el-option label="正常" value="normal" />
            <el-option label="休学" value="suspended" />
            <el-option label="已毕业" value="graduated" />
            <el-option label="退学" value="withdrawn" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveStudent">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { adminApi } from '../../api'

const students = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref(null)

const form = reactive({
  student_no: '',
  name: '',
  class_name: '',
  major: '',
  grade: '',
  status: 'normal'
})

const getStatusType = (status) => {
  const map = { normal: 'success', suspended: 'warning', graduated: 'info', withdrawn: 'danger' }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = { normal: '正常', suspended: '休学', graduated: '已毕业', withdrawn: '退学' }
  return map[status] || status
}

const openDialog = () => {
  isEdit.value = false
  Object.assign(form, { student_no: '', name: '', class_name: '', major: '', grade: '', status: 'normal' })
  dialogVisible.value = true
}

const editStudent = (student) => {
  isEdit.value = true
  editingId.value = student.id
  Object.assign(form, student)
  dialogVisible.value = true
}

const saveStudent = async () => {
  try {
    if (isEdit.value) {
      await adminApi.updateStudent(editingId.value, form)
      ElMessage.success('学生信息更新成功')
    } else {
      await adminApi.createStudent(form)
      ElMessage.success('学生添加成功')
    }
    dialogVisible.value = false
    loadStudents()
  } catch (error) {
    console.error('Save error:', error)
  }
}

const deleteStudent = async (student) => {
  try {
    await ElMessageBox.confirm(`确定要删除学生 ${student.name} 吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await adminApi.deleteStudent(student.id)
    ElMessage.success('删除成功')
    loadStudents()
  } catch (error) {
    if (error !== 'cancel') console.error('Delete error:', error)
  }
}

const loadStudents = async () => {
  try {
    const res = await adminApi.getStudents()
    students.value = res.data
  } catch (error) {
    console.error('Error loading students:', error)
  }
}

onMounted(loadStudents)
</script>

<style scoped>
.students-page { animation: fadeIn 0.3s ease; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
