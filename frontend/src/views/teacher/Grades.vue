<template>
  <div class="grades-page">
    <h1 class="page-title">成绩录入</h1>
    
    <!-- 课程选择 -->
    <el-card class="course-select-card">
      <el-form :inline="true">
        <el-form-item label="选择课程">
          <el-select v-model="selectedScheduleId" placeholder="请选择课程" @change="loadStudents">
            <el-option 
              v-for="item in schedule" 
              :key="item.id" 
              :label="`${item.course_name} (${item.weekday_name} ${item.start_period}-${item.end_period}节)`" 
              :value="item.id" 
            />
          </el-select>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 学生成绩列表 -->
    <el-card v-if="selectedScheduleId">
      <template #header>
        <div class="card-header">
          <span>{{ currentCourse?.course_name }} - 学生成绩</span>
          <el-button type="primary" @click="saveGrades" :loading="saving">
            <el-icon><Check /></el-icon>
            保存成绩
          </el-button>
        </div>
      </template>
      
      <el-table :data="students" stripe>
        <el-table-column prop="student_no" label="学号" width="140" />
        <el-table-column prop="student_name" label="姓名" width="100" />
        <el-table-column prop="class_name" label="班级" width="150" />
        <el-table-column label="成绩" width="150">
          <template #default="{ row }">
            <el-input-number 
              v-model="row.score" 
              :min="0" 
              :max="100" 
              :precision="0"
              size="small"
              controls-position="right"
            />
          </template>
        </el-table-column>
        <el-table-column label="绩点" width="100">
          <template #default="{ row }">
            <span>{{ calculateGpa(row.score) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.grade_status === 'final'" type="success">已录入</el-tag>
            <el-tag v-else type="info">未录入</el-tag>
          </template>
        </el-table-column>
      </el-table>
      
      <el-empty v-if="students.length === 0" description="暂无学生选修此课程" />
    </el-card>
    
    <el-empty v-else description="请先选择课程" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Check } from '@element-plus/icons-vue'
import { teacherApi } from '../../api'

const route = useRoute()
const schedule = ref([])
const students = ref([])
const selectedScheduleId = ref(null)
const saving = ref(false)

const currentCourse = computed(() => {
  return schedule.value.find(s => s.id === selectedScheduleId.value)
})

const calculateGpa = (score) => {
  if (!score && score !== 0) return '-'
  if (score >= 90) return '4.0'
  if (score >= 85) return '3.7'
  if (score >= 80) return '3.3'
  if (score >= 75) return '3.0'
  if (score >= 70) return '2.7'
  if (score >= 65) return '2.3'
  if (score >= 60) return '2.0'
  return '0.0'
}

const loadStudents = async () => {
  if (!selectedScheduleId.value) return
  
  try {
    const res = await teacherApi.getCourseStudents(selectedScheduleId.value)
    students.value = res.data.students
  } catch (error) {
    console.error('Error loading students:', error)
  }
}

const saveGrades = async () => {
  const grades = students.value
    .filter(s => s.score !== null && s.score !== undefined)
    .map(s => ({
      selection_id: s.selection_id,
      score: s.score
    }))
  
  if (grades.length === 0) {
    ElMessage.warning('请至少录入一个学生的成绩')
    return
  }
  
  saving.value = true
  try {
    await teacherApi.enterGrades(grades)
    ElMessage.success('成绩保存成功')
    loadStudents()
  } catch (error) {
    console.error('Save grades error:', error)
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  try {
    const res = await teacherApi.getSchedule()
    schedule.value = res.data
    
    // 如果从URL带了参数
    if (route.query.schedule_id) {
      selectedScheduleId.value = parseInt(route.query.schedule_id)
      loadStudents()
    }
  } catch (error) {
    console.error('Error loading schedule:', error)
  }
})
</script>

<style scoped>
.grades-page {
  animation: fadeIn 0.3s ease;
}

.course-select-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
