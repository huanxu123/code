<template>
  <div class="teachers-page">
    <h1 class="page-title">教师管理</h1>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>教师列表</span>
          <el-button type="primary" @click="openDialog">
            <el-icon><Plus /></el-icon>
            添加教师
          </el-button>
        </div>
      </template>
      
      <el-table :data="teachers" stripe>
        <el-table-column prop="teacher_no" label="工号" width="120" />
        <el-table-column prop="name" label="姓名" width="100" />
        <el-table-column prop="department" label="院系" />
        <el-table-column prop="title" label="职称" width="100" />
      </el-table>
    </el-card>
    
    <el-dialog v-model="dialogVisible" title="添加教师" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="工号">
          <el-input v-model="form.teacher_no" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="院系">
          <el-input v-model="form.department" />
        </el-form-item>
        <el-form-item label="职称">
          <el-select v-model="form.title">
            <el-option label="教授" value="教授" />
            <el-option label="副教授" value="副教授" />
            <el-option label="讲师" value="讲师" />
            <el-option label="助教" value="助教" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveTeacher">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { adminApi } from '../../api'

const teachers = ref([])
const dialogVisible = ref(false)
const form = reactive({ teacher_no: '', name: '', department: '', title: '讲师' })

const openDialog = () => {
  Object.assign(form, { teacher_no: '', name: '', department: '', title: '讲师' })
  dialogVisible.value = true
}

const saveTeacher = async () => {
  try {
    await adminApi.createTeacher(form)
    ElMessage.success('教师添加成功')
    dialogVisible.value = false
    loadTeachers()
  } catch (error) {
    console.error('Save error:', error)
  }
}

const loadTeachers = async () => {
  try {
    const res = await adminApi.getTeachers()
    teachers.value = res.data
  } catch (error) {
    console.error('Error loading teachers:', error)
  }
}

onMounted(loadTeachers)
</script>

<style scoped>
.teachers-page { animation: fadeIn 0.3s ease; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
