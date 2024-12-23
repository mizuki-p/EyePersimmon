# from flask import request, jsonify
import os
os.environ["CUDA_VISIBLE_DEVICES"]="7"
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime, timedelta
from app.model import inference_engine
from PIL import Image

app = FastAPI()

system_prompt="You are an assistant helping me with the AirSim simulator for drone or car.When I ask you to do something, you are supposed to give me Python code that is needed to achieve that task using AirSim and then an explanation of what that code does. You are only allowed to use the functions I have defined for you.You are not to use any other hypothetical functions that you think might exist.You can use simple Python functions from libraries such as math and numpy."

# 模拟一个存储注册信息的数据库
registered_clients = {}
Max_num = 10  # 支持的最大并发用户数量
usr_timeout = timedelta(minutes=30)  # 超时时间

def process_image(observation):
    observation=Image.open(observation)
    size=observation.size
    if size[0]>1024 or size[1]>1024:
        observation=observation.resize((256,256))
    return observation

def cleanup_users():
    nowtime = datetime.now()
    for id, item in list(registered_clients.items()):
        if nowtime - item["last_active"] >= usr_timeout:
            del registered_clients[id]
    # return 0


def register_routes(app: FastAPI):
    """注册路由"""

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_json()
                action = data.get("action")
                if action == "register_client":
                    await register_client(websocket, data.get("data"))
                elif action == "get_action":
                    await get_action(websocket, data.get("data"))
                else:
                    await websocket.send_json({"error": "Unknown action"})
        except WebSocketDisconnect:
            print("Client disconnected")


async def register_client(websocket: WebSocket, data: dict):
    # 获取请求中的 JSON 数据
    # data = request.get_json()

    # 检查必需字段是否存在
    required_fields = ["client_id", "env_id", "env_name"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        # 如果有缺失字段，返回失败响应
        await websocket.send_json(
            {
                "text": "register fail",
                "fail_reason": f'Missing fields: {", ".join(missing_fields)}',
            }
        )
        return

    # 检查字典中有无超时用户
    cleanup_users()

    # 若当前用户过多，则注册失败
    usr_num = len(registered_clients)
    if usr_num >= Max_num:
        await websocket.send_json(
            {
                "text": "register fail",
                "fail_reason": "No place for a new user, please try again later!",
            }
        )
        return

    client_id = data["client_id"]
    env_id = data["env_id"]
    env_name = data["env_name"]

    # 检查是否已经注册
    if client_id in registered_clients:
        await websocket.send_json(
            {
                "text": "register fail",
                "fail_reason": "Client already registered",
            }
        )
        return

    # 进行注册
    registered_clients[client_id] = {
        "env_id": env_id,
        "env_name": env_name,
        "last_active": datetime.now(),  # registe time
    }

    # 返回成功响应
    await websocket.send_json({"text": "register success"})


# def model_inference(image,text):
#     return [1,2,3]  #action_vector


# @app.route("/get_action", methods=["POST"])
async def get_action(websocket: WebSocket, data: dict):
    # data = request.get_json()
    required_augs = ["client_id", "instruction", "observation"]
    missing_augs = [aug for aug in required_augs if aug not in data]
    if missing_augs:
        await websocket.send_json(
            {
                "text": "get action fail",
                "fail_reason": f"Missing augments:{','.join(missing_augs)}",
            }
        )
        return

    # if 'client_id' not in request.form or 'instruction' not in request.form or 'observation' not in request.form:
    #     return jsonify({
    #         'text': 'get action fail',
    #         'fail_reason': 'Missing client_id or instruction or observation'
    #     }), 400

    client_id = data["client_id"]
    instruction = data["instruction"]
    observation = data["observation"]
    observation=process_image(observation)
    # observation=Image.open(observation)
    # observation=observation.resize((1024,1024))
    # print(observation.size)

    if client_id not in registered_clients:
        await websocket.send_json(
            {"text": "get action fail", "fail_reason": "client not registered"}
        )
        return

    try:
        action = inference_engine.infer(observation, system_prompt,instruction)
        registered_clients[client_id]["last_active"] = datetime.now()
        await websocket.send_json({"action": action})
    except Exception as error:
        await websocket.send_json(
            {"text": "get action fail", "fail_reason": str(error)}
        )

    # if __name__ == "__main__":
    #     app.run(debug=True)
