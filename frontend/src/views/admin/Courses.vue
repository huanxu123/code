<template>
  <div class="courses-page">
    <h1 class="page-title">课程管理</h1>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>课程列表</span>
          <el-button type="primary" @click="openDialog">
            <el-icon><Plus /></el-icon>
            添加课程
          </el-button>
        </div>
      </template>
      
      <el-table :data="courses" stripe>
        <el-table-column prop="code" label="课程代码" width="120" />
        <el-table-column prop="name" label="课程名称" />
        <el-table-column prop="credit" label="学分" width="80" align="center" />
        <el-table-column prop="hours" label="学时" width="80" align="center" />
        <el-table-column prop="teacher_name" label="授课教师" width="120" />
        <el-table-column label="操作" width="100" align="center">
          <template #default="{ row }">
            <el-button type="primary" size="small" text @click="editCourse(row)">
              编辑
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑课程' : '添加课程'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="课程代码">
          <el-input v-model="form.code" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="课程名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="学分">
          <el-input-number v-model="form.credit" :min="1" :max="10" />
        </el-form-item>
        <el-form-item label="学时">
          <el-input-number v-model="form.hours" :min="16" :max="128" :step="16" />
        </el-form-item>
        <el-form-item label="授课教师">
          <el-select v-model="form.teacher_id">
            <el-option v-for="t in teachers" :key="t.id" :label="t.name" :value="t.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveCourse">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { adminApi } from '../../api'

const courses = ref([])
const teachers = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref(null)

const form = reactive({ code: '', name: '', credit: 3, hours: 48, teacher_id: null })

const openDialog = () => {
  isEdit.value = false
  Object.assign(form, { code: '', name: '', credit: 3, hours: 48, teacher_id: null })
  dialogVisible.value = true
}

const editCourse = (course) => {
  isEdit.value = true
  editingId.value = course.id
  Object.assign(form, course)
  dialogVisible.value = true
}

const saveCourse = async () => {
  try {
    if (isEdit.value) {
      await adminApi.updateCourse(editingId.value, form)
      ElMessage.success('课程更新成功')
    } else {
      await adminApi.createCourse(form)
      ElMessage.success('课程添加成功')
    }
    dialogVisible.value = false
    loadCourses()
  } catch (error) {
    console.error('Save error:', error)
  }
}

const loadCourses = async () => {
  try {
    const [coursesRes, teachersRes] = await Promise.all([
      adminApi.getCourses(),
      adminApi.getTeachers()
    ])
    courses.value = coursesRes.data
    teachers.value = teachersRes.data
  } catch (error) {
    console.error('Error loading data:', error)
  }
}

onMounted(loadCourses)
</script>

<style scoped>
.courses-page { animation: fadeIn 0.3s ease; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
