我目前要设计基于mysql数据库的web端应用，其中要包括功能
前端页面结构（最小可用版本 MVP）
学生端

首页：个人信息（Student）、学籍状态（status）。

设计文档

选课：学期课表（Schedule 列表）→ 选课（CourseSelection）

成绩：Grade 列表 + 复核入口（GradeReview）

评教：未完成评教列表（CourseEvaluation.status）

学籍异动/重修：申请列表（StatusChange/RetakeApplication）

毕设：课题浏览/申请（GraduationTopic/TopicApplication）、过程文档（ProcessDocument）

教师端

我的排课（Schedule）

成绩录入（CourseSelection → Grade）

复核处理（GradeReview）

毕设课题管理（GraduationTopic）、指导关系（InstructorRelation）

监考查看（InvigilatorAssignment）

教务端

基础数据管理（R1~R9）

排课/调课（Schedule）

考试安排/监考安排（ExamArrangement/InvigilatorAssignment）

借教室审批（ClassroomBorrowRecord）

审批中心：学籍异动/重修/成绩复核/毕设选题（统一列表）
而且这些数据都要与数据库已有数据挂钩，
软件挂载到端口5555