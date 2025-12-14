<template>
  <div class="schedule-page">
    <h1 class="page-title">排课管理</h1>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>排课列表</span>
          <el-button type="primary" @click="openDialog">
            <el-icon><Plus /></el-icon>
            新建排课
          </el-button>
        </div>
      </template>
      
      <el-table :data="schedules" stripe>
        <el-table-column prop="course_code" label="课程代码" width="120" />
        <el-table-column prop="course_name" label="课程名称" />
        <el-table-column prop="teacher_name" label="教师" width="100" />
        <el-table-column prop="weekday_name" label="星期" width="80" />
        <el-table-column label="节次" width="100">
          <template #default="{ row }">
            第{{ row.start_period }}-{{ row.end_period }}节
          </template>
        </el-table-column>
        <el-table-column prop="classroom" label="教室" width="100" />
        <el-table-column prop="weeks" label="周次" width="80" />
        <el-table-column label="操作" width="100" align="center">
          <template #default="{ row }">
            <el-button type="primary" size="small" text @click="editSchedule(row)">
              调课
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <el-dialog v-model="dialogVisible" :title="isEdit ? '调课' : '新建排课'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item v-if="!isEdit" label="课程">
          <el-select v-model="form.course_id">
            <el-option v-for="c in courses" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="星期">
          <el-select v-model="form.weekday">
            <el-option v-for="d in weekdays" :key="d.value" :label="d.label" :value="d.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="节次">
          <el-col :span="11">
            <el-input-number v-model="form.start_period" :min="1" :max="12" />
          </el-col>
          <el-col :span="2" style="text-align: center">-</el-col>
          <el-col :span="11">
            <el-input-number v-model="form.end_period" :min="1" :max="12" />
          </el-col>
        </el-form-item>
        <el-form-item label="教室">
          <el-select v-model="form.classroom">
            <el-option v-for="r in classrooms" :key="r.id" :label="r.room_no" :value="r.room_no" />
          </el-select>
        </el-form-item>
        <el-form-item label="周次">
          <el-input v-model="form.weeks" placeholder="例如: 1-16" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveSchedule">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { adminApi } from '../../api'

const schedules = ref([])
const courses = ref([])
const classrooms = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref(null)

const weekdays = [
  { value: 1, label: '周一' }, { value: 2, label: '周二' }, { value: 3, label: '周三' },
  { value: 4, label: '周四' }, { value: 5, label: '周五' }, { value: 6, label: '周六' }, { value: 7, label: '周日' }
]

const form = reactive({
  course_id: null, weekday: 1, start_period: 1, end_period: 2, classroom: '', weeks: '1-16'
})

const openDialog = () => {
  isEdit.value = false
  Object.assign(form, { course_id: null, weekday: 1, start_period: 1, end_period: 2, classroom: '', weeks: '1-16' })
  dialogVisible.value = true
}

const editSchedule = (schedule) => {
  isEdit.value = true
  editingId.value = schedule.id
  Object.assign(form, schedule)
  dialogVisible.value = true
}

const saveSchedule = async () => {
  try {
    if (isEdit.value) {
      await adminApi.updateSchedule(editingId.value, form)
      ElMessage.success('调课成功')
    } else {
      await adminApi.createSchedule(form)
      ElMessage.success('排课成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('Save error:', error)
  }
}

const loadData = async () => {
  try {
    const [schedulesRes, coursesRes, classroomsRes] = await Promise.all([
      adminApi.getSchedule(),
      adminApi.getCourses(),
      adminApi.getClassrooms()
    ])
    schedules.value = schedulesRes.data
    courses.value = coursesRes.data
    classrooms.value = classroomsRes.data
  } catch (error) {
    console.error('Error loading data:', error)
  }
}

onMounted(loadData)
</script>

<style scoped>
.schedule-page { animation: fadeIn 0.3s ease; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
