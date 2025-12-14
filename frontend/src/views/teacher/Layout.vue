<template>
  <el-container class="layout-container">
    <el-aside width="240px" class="sidebar">
      <div class="sidebar-header">
        <el-icon :size="32"><School /></el-icon>
        <span>教师端</span>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/teacher/home">
          <el-icon><HomeFilled /></el-icon>
          <span>我的排课</span>
        </el-menu-item>
        <el-menu-item index="/teacher/grades">
          <el-icon><Edit /></el-icon>
          <span>成绩录入</span>
        </el-menu-item>
        <el-menu-item index="/teacher/reviews">
          <el-icon><Document /></el-icon>
          <span>成绩复核</span>
        </el-menu-item>
        <el-menu-item index="/teacher/thesis">
          <el-icon><Reading /></el-icon>
          <span>毕设管理</span>
        </el-menu-item>
        <el-menu-item index="/teacher/exams">
          <el-icon><Calendar /></el-icon>
          <span>监考安排</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/teacher/home' }">教师端</el-breadcrumb-item>
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
  School, HomeFilled, Edit, Document, Reading, 
  Calendar, ArrowDown 
} from '@element-plus/icons-vue'
import { authApi } from '../../api'

const router = useRouter()
const route = useRoute()
const user = ref(null)

const activeMenu = computed(() => route.path)

const pageTitles = {
  '/teacher/home': '我的排课',
  '/teacher/grades': '成绩录入',
  '/teacher/reviews': '成绩复核',
  '/teacher/thesis': '毕设管理',
  '/teacher/exams': '监考安排'
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
  background: linear-gradient(180deg, #0f3460 0%, #16213e 100%);
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
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
