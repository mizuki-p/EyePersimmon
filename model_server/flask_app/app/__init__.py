from fastapi import FastAPI
from app.route import register_routes


def create_app() -> FastAPI:
    """
    工厂方法，用于创建 FastAPI 应用实例。
    :return: 配置完成的 FastAPI 应用实例。
    """
    app = FastAPI(title="WebSocket Application", version="1.0.0")

    # 注册路由
    register_routes(app)

    return app


"""

/app
    __init__.py
    model.py
    route.py
config.py
run.py
"""
