from flask import Flask, Response, request, send_from_directory
from flask_cors import CORS
from ..manager import BaseClient
from ..configs import Config


class TransferViewer:
    def __init__(self, invoker: BaseClient):
        self.invoker = invoker

        self.app = Flask("EP")  # 第一个参数填啥我也不清楚，姑且先填个'EP'
        CORS(self.app, supports_credentials=True, responses={r"*": {"origins": "*"}})
        self.register_interaction()

    def register_interaction(self):
        @self.app.route("/")
        def index():
            return send_from_directory("static", "index.html")

        @self.app.route("/register", methods=["POST"])
        async def register():
            status, msg = await self.invoker.register_client()
            return {"status": status, "msg": msg}

        @self.app.route("/get_action", methods=["POST"])
        async def get_action():
            data = request.json
            instruction = data["instruction"]

            status, msg = await self.invoker.get_action(instruction)
            return {"status": status, "msg": msg}

        @self.app.route("/queryInited", methods=["GET"])
        def query_inited():
            ws, env = self.invoker.check_init()
            if not ws and not env:
                return {"status": False, "msg": "Both Not inited"}
            elif not ws:
                return {"status": False, "msg": "WS not inited"}
            elif not env:
                return {"status": False, "msg": "Env not inited"}
            else:
                return {"status": True, "msg": "Both inited"}

        @self.app.route("/queryEnvironment", methods=["GET"])
        def query_environment():
            return self.invoker.get_env_info()

        @self.app.route("/startTask", methods=["POST"])
        def start_task():
            data = request.json
            instruction = data["instruction"]

            return self.invoker.start_task(instruction)

        @self.app.route("/stopTask", methods=["POST"])
        def stop_task():
            return self.invoker.stop_task()

        @self.app.route("/queryTaskState", methods=["GET"])
        def query_task_state():
            return {
                "status": True,
                "msg": (
                    "Task running" if self.invoker.task_running else "Task not running"
                ),
            }

        @self.app.route("/queryIframeUrl", methods=["GET"])
        def query_iframe_url():
            return self.invoker.get_live_url()

    def run(self):
        self.app.run(port=Config.VIEWER_PORT)
        
    def close(self):
        self.invoker.close()
