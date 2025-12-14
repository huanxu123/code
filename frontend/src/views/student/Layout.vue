<template>
  <el-container class="layout-container">
    <el-aside width="240px" class="sidebar">
      <div class="sidebar-header">
        <el-icon :size="32"><School /></el-icon>
        <span>学生端</span>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/student/home">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/student/schedule">
          <el-icon><Calendar /></el-icon>
          <span>课表/选课</span>
        </el-menu-item>
        <el-menu-item index="/student/grades">
          <el-icon><Document /></el-icon>
          <span>成绩查询</span>
        </el-menu-item>
        <el-menu-item index="/student/evaluation">
          <el-icon><Star /></el-icon>
          <span>评教</span>
        </el-menu-item>
        <el-menu-item index="/student/applications">
          <el-icon><EditPen /></el-icon>
          <span>学籍/重修申请</span>
        </el-menu-item>
        <el-menu-item index="/student/thesis">
          <el-icon><Reading /></el-icon>
          <span>毕业设计</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/student/home' }">学生端</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentPageTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <div class="user-info">
              <el-avatar :size="36" class="avatar">
                {{ user?.name?.charAt(0) }}
              </el-avatar>
              <span class="username">{{ user?.name }}</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  School, HomeFilled, Calendar, Document, Star, EditPen, 
  Reading, ArrowDown 
} from '@element-plus/icons-vue'
import { authApi } from '../../api'

const router = useRouter()
const route = useRoute()
const user = ref(null)

const activeMenu = computed(() => route.path)

const pageTitles = {
  '/student/home': '首页',
  '/student/schedule': '课表/选课',
  '/student/grades': '成绩查询',
  '/student/evaluation': '评教',
  '/student/applications': '学籍/重修申请',
  '/student/thesis': '毕业设计'
}

const currentPageTitle = computed(() => pageTitles[route.path] || '')

onMounted(() => {
  const userData = localStorage.getItem('user')
  if (userData) {
    user.value = JSON.parse(userData)
  }
})

const handleCommand = async (command) => {
  if (command === 'logout') {
    try {
      await authApi.logout()
      localStorage.removeItem('user')
      ElMessage.success('已退出登录')
      router.push('/login')
    } catch (error) {
      console.error('Logout error:', error)
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: white;
  font-size: 18px;
  font-weight: 600;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-menu {
  background: transparent;
  border: none;
  padding: 16px 12px;
  flex: 1;
}

.sidebar-menu .el-menu-item {
  color: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  margin-bottom: 4px;
  height: 48px;
  transition: all 0.3s;
}

.sidebar-menu .el-menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.sidebar-menu .el-menu-item.is-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header {
  background: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  height: 64px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s;
}

.user-info:hover {
  background: #f5f7fa;
}

.avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.username {
  font-weight: 500;
  color: #2c3e50;
}

.main-content {
  background: #f5f7fa;
  padding: 24px;
  overflow-y: auto;
}
</style>
