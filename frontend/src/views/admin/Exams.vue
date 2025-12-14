<template>
  <div class="exams-page">
    <h1 class="page-title">考试安排</h1>
    
    <el-tabs v-model="activeTab">
      <!-- 考试安排 -->
      <el-tab-pane label="考试安排" name="exams">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>考试列表</span>
              <el-button type="primary" @click="openExamDialog">
                <el-icon><Plus /></el-icon>
                新建考试
              </el-button>
            </div>
          </template>
          
          <el-table :data="exams" stripe>
            <el-table-column prop="course_code" label="课程代码" width="120" />
            <el-table-column prop="course_name" label="课程名称" />
            <el-table-column prop="date" label="日期" width="120" />
            <el-table-column label="时间" width="150">
              <template #default="{ row }">
                {{ row.start_time }} - {{ row.end_time }}
              </template>
            </el-table-column>
            <el-table-column prop="classroom" label="教室" width="100" />
          </el-table>
        </el-card>
      </el-tab-pane>
      
      <!-- 监考安排 -->
      <el-tab-pane label="监考安排" name="invigilators">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>监考列表</span>
              <el-button type="primary" @click="openInvigilatorDialog">
                <el-icon><Plus /></el-icon>
                新建监考
              </el-button>
            </div>
          </template>
          
          <el-table :data="invigilators" stripe>
            <el-table-column prop="course_name" label="课程" />
            <el-table-column prop="exam_date" label="日期" width="120" />
            <el-table-column prop="exam_time" label="时间" width="150" />
            <el-table-column prop="classroom" label="教室" width="100" />
            <el-table-column prop="teacher_name" label="监考教师" width="100" />
            <el-table-column prop="role" label="角色" width="100" />
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 新建考试对话框 -->
    <el-dialog v-model="examDialogVisible" title="新建考试" width="500px">
      <el-form :model="examForm" label-width="80px">
        <el-form-item label="课程">
          <el-select v-model="examForm.schedule_id">
            <el-option v-for="s in schedules" :key="s.id" :label="s.course_name" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker v-model="examForm.date" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="时间">
          <el-col :span="11">
            <el-time-select v-model="examForm.start_time" start="08:00" step="00:30" end="20:00" />
          </el-col>
          <el-col :span="2" style="text-align: center">-</el-col>
          <el-col :span="11">
            <el-time-select v-model="examForm.end_time" start="08:00" step="00:30" end="22:00" />
          </el-col>
        </el-form-item>
        <el-form-item label="教室">
          <el-select v-model="examForm.classroom">
            <el-option v-for="r in classrooms" :key="r.id" :label="r.room_no" :value="r.room_no" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="examDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveExam">保存</el-button>
      </template>
    </el-dialog>
    
    <!-- 新建监考对话框 -->
    <el-dialog v-model="invigilatorDialogVisible" title="新建监考" width="500px">
      <el-form :model="invigilatorForm" label-width="80px">
        <el-form-item label="考试">
          <el-select v-model="invigilatorForm.exam_id">
            <el-option v-for="e in exams" :key="e.id" :label="`${e.course_name} (${e.date})`" :value="e.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="教师">
          <el-select v-model="invigilatorForm.teacher_id">
            <el-option v-for="t in teachers" :key="t.id" :label="t.name" :value="t.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="invigilatorForm.role">
            <el-option label="主监考" value="主监考" />
            <el-option label="副监考" value="副监考" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="invigilatorDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveInvigilator">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { adminApi } from '../../api'

const activeTab = ref('exams')
const exams = ref([])
const invigilators = ref([])
const schedules = ref([])
const classrooms = ref([])
const teachers = ref([])

const examDialogVisible = ref(false)
const invigilatorDialogVisible = ref(false)

const examForm = reactive({ schedule_id: null, date: '', start_time: '09:00', end_time: '11:00', classroom: '' })
const invigilatorForm = reactive({ exam_id: null, teacher_id: null, role: '主监考' })

const openExamDialog = () => {
  Object.assign(examForm, { schedule_id: null, date: '', start_time: '09:00', end_time: '11:00', classroom: '' })
  examDialogVisible.value = true
}

const openInvigilatorDialog = () => {
  Object.assign(invigilatorForm, { exam_id: null, teacher_id: null, role: '主监考' })
  invigilatorDialogVisible.value = true
}

const saveExam = async () => {
  try {
    await adminApi.createExam(examForm)
    ElMessage.success('考试安排创建成功')
    examDialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('Save error:', error)
  }
}

const saveInvigilator = async () => {
  try {
    await adminApi.createInvigilator(invigilatorForm)
    ElMessage.success('监考安排创建成功')
    invigilatorDialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('Save error:', error)
  }
}

const loadData = async () => {
  try {
    const [examsRes, invigilatorsRes, schedulesRes, classroomsRes, teachersRes] = await Promise.all([
      adminApi.getExams(),
      adminApi.getInvigilators(),
      adminApi.getSchedule(),
      adminApi.getClassrooms(),
      adminApi.getTeachers()
    ])
    exams.value = examsRes.data
    invigilators.value = invigilatorsRes.data
    schedules.value = schedulesRes.data
    classrooms.value = classroomsRes.data
    teachers.value = teachersRes.data
  } catch (error) {
    console.error('Error loading data:', error)
  }
}

onMounted(loadData)
</script>

<style scoped>
.exams-page { animation: fadeIn 0.3s ease; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
