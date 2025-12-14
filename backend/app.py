"""
学生教务管理系统 - Flask 后端主入口
"""

import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from config import config
from routes.auth import auth_bp
from routes.student import student_bp
from routes.teacher import teacher_bp
from routes.admin import admin_bp


def create_app(config_name='default'):
    """创建 Flask 应用"""
    app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 启用 CORS
    CORS(app, supports_credentials=True)
    
    # 设置 session
    app.secret_key = app.config['SECRET_KEY']
    
    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(admin_bp)
    
    # 前端路由 - 处理 SPA
    @app.route('/')
    def serve():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')
    
    # 健康检查
    @app.route('/api/health')
    def health_check():
        return {'status': 'ok', 'message': '服务运行正常'}
    
    return app


if __name__ == '__main__':
    app = create_app('development')
    print('=' * 50)
    print('学生教务管理系统')
    print('=' * 50)
    print('服务地址: http://localhost:5555')
    print('=' * 50)
    print('测试账号:')
    print('  学生: student1 / 123456')
    print('  教师: teacher1 / 123456')
    print('  教务: admin1 / 123456')
    print('=' * 50)
    app.run(host='0.0.0.0', port=5555, debug=True)
