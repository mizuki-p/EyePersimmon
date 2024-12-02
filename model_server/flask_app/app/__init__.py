from flask import Flask
from app.route import register_routes  # 导入 route.py 中的路由注册函数




def create_app():
    """创建 Flask 应用实例"""
    # 初始化并配置 Flask 应用（从 config.py 导入配置）
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # 注册路由
    register_routes(app)
    
    return app

'''

/app
    __init__.py
    model.py
    route.py
config.py
run.py
'''