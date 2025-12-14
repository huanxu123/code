# 学生教务管理系统

基于 MySQL 的 Web 端教务管理应用，包含学生端、教师端和教务端三个角色入口。

## 技术栈

- **后端**: Python + Flask
- **前端**: Vue 3 + Vite + Element Plus
- **数据库**: MySQL（当前使用模拟数据）
- **端口**: 5555

## 项目结构

```
code/
├── backend/                 # Flask 后端
│   ├── app.py              # 主应用入口
│   ├── config.py           # 配置文件
│   ├── requirements.txt    # Python 依赖
│   ├── models/             # 数据模型
│   │   └── models.py
│   └── routes/             # API 路由
│       ├── auth.py         # 用户认证
│       ├── student.py      # 学生端
│       ├── teacher.py      # 教师端
│       └── admin.py        # 教务端
│
├── frontend/               # Vue 前端
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── api/            # API 封装
│       ├── router/         # 路由配置
│       ├── styles/         # 全局样式
│       └── views/          # 页面组件
│           ├── Login.vue
│           ├── student/    # 学生端页面
│           ├── teacher/    # 教师端页面
│           └── admin/      # 教务端页面
│
└── README.md
```

## 快速启动

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端将运行在 http://localhost:5555

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端将运行在 http://localhost:3000

### 3. 访问应用

打开浏览器访问 http://localhost:3000

## 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 学生 | student1 | 123456 |
| 学生 | student2 | 123456 |
| 教师 | teacher1 | 123456 |
| 教师 | teacher2 | 123456 |
| 教务 | admin1 | 123456 |

## 功能模块

### 学生端
- ✅ 首页：个人信息、学籍状态
- ✅ 课表/选课：查看课表、选课退课
- ✅ 成绩查询：成绩列表、成绩复核申请
- ✅ 评教：未完成评教列表、提交评教
- ✅ 学籍/重修申请：学籍异动、重修申请
- ✅ 毕业设计：课题浏览申请、过程文档

### 教师端
- ✅ 我的排课：课程表、课程列表
- ✅ 成绩录入：选择课程、批量录入
- ✅ 成绩复核：复核申请处理
- ✅ 毕设管理：课题管理、申请审批、指导学生
- ✅ 监考安排：查看监考任务

### 教务端
- ✅ 数据概览：统计信息、快捷操作
- ✅ 学生管理：增删改查
- ✅ 教师管理：添加教师
- ✅ 课程管理：课程信息维护
- ✅ 排课管理：排课、调课
- ✅ 考试安排：考试、监考安排
- ✅ 审批中心：统一审批入口

## 数据库配置

当前使用模拟数据，如需连接真实 MySQL 数据库，请修改 `backend/config.py`：

```python
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DATABASE = 'education_system'
USE_MOCK_DATA = False
```

## 注意事项

1. 当前版本使用模拟数据，数据保存在内存中，重启后会重置
2. 认证使用 Flask Session，无需 JWT 配置
3. 前端开发模式下通过 Vite 代理转发 API 请求到后端
