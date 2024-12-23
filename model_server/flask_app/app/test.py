import websocket
import json


def on_message(ws, message):
    print("Received:", message)


def on_open(ws):
    print("Connection opened")
    # 发送注册请求
    register_payload = {
        "action": "register_client",
        "data": {
            "client_id": "test_client1",
            "env_id": "env_003",
            "env_name": "Test Environment",
        },
    }
    print("Sending register_client payload...")
    ws.send(json.dumps(register_payload))

    # 发送动作请求
    action_payload = {
        "action": "get_action",
        "data": {
            "client_id": "test_client1",
            "instruction": "describe the image",
            "observation": "/home/zhangshuai/data/boundless/demo.jpeg",
        },
    }
    print("Sending get_action payload...")
    ws.send(json.dumps(action_payload))


def on_close(ws, close_status_code, close_msg):
    print("Connection closed")


ws = websocket.WebSocketApp(
    "ws://127.0.0.1:5001/ws", on_message=on_message, on_open=on_open, on_close=on_close
)

ws.run_forever()
