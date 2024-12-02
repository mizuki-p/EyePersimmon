from flask import request, jsonify
from datetime import datetime, timedelta
from app.model import model_inference

# app = Flask(__name__)

# 模拟一个存储注册信息的数据库
registered_clients = {}
Max_num = 10  # 支持的最大并发用户数量
usr_timeout = timedelta(minutes=30)  # 超时时间


def cleanup_users():
    nowtime = datetime.now()
    for id, time in list(registered_clients.items()):
        if nowtime - time >= usr_timeout:
            del registered_clients[id]
    # return 0


def register_routes(app):
    @app.route("/register_client", methods=["POST"])
    def register_client():
        # 获取请求中的 JSON 数据
        data = request.get_json()

        # 检查必需字段是否存在
        required_fields = ["client_id", "env_id", "env_name"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            # 如果有缺失字段，返回失败响应
            return (
                jsonify(
                    {
                        "text": "register fail",
                        "fail_reason": f'Missing fields: {", ".join(missing_fields)}',
                    }
                ),
                400,
            )

        # 检查字典中有无超时用户
        cleanup_users()

        # 若当前用户过多，则注册失败
        usr_num = len(registered_clients)
        if usr_num == Max_num:
            return (
                jsonify(
                    {
                        "text": "register fail",
                        "fail_reason": "there is no place for a new user, please try again later!",
                    }
                ),
                400,
            )

        client_id = data["client_id"]
        env_id = data["env_id"]
        env_name = data["env_name"]

        # 检查是否已经注册
        if client_id in registered_clients:
            return (
                jsonify(
                    {
                        "text": "register fail",
                        "fail_reason": "Client already registered",
                    }
                ),
                400,
            )

        # 进行注册
        registered_clients[client_id] = {
            "env_id": env_id,
            "env_name": env_name,
            "last_active": datetime.now(),  # registe time
        }

        # 返回成功响应
        return jsonify({"text": "register success"}), 200

    # def model_inference(image,text):
    #     return [1,2,3]  #action_vector

    @app.route("/get_action", methods=["POST"])
    def get_action():
        data = request.get_json()
        required_augs = ["client_id", "instruction", "observation"]
        missing_augs = [aug for aug in required_augs if aug not in data]
        if missing_augs:
            return (
                jsonify(
                    {
                        "text": "get action fail",
                        "fail_reason": f"Missing augments:{','.join(missing_augs)}",
                    }
                ),
                400,
            )
        # if 'client_id' not in request.form or 'instruction' not in request.form or 'observation' not in request.form:
        #     return jsonify({
        #         'text': 'get action fail',
        #         'fail_reason': 'Missing client_id or instruction or observation'
        #     }), 400

        client_id = request.form["client_id"]
        instruction = request.form["instruction"]
        observation = request.files.get("observation")

        if client_id not in registered_clients:
            return (
                jsonify(
                    {"text": "get action fail", "fail reason": "client not registered"}
                ),
                400,
            )

        try:
            action = model_inference(observation, instruction)
            registered_clients[client_id]["last_active"] = datetime.now()
            return jsonify({"action": action}), 200
        except Exception as error:
            return jsonify({"text": "get action fail", "fail_reason": str(error)}), 500

    # if __name__ == "__main__":
    #     app.run(debug=True)
