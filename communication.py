'''
Entity: Client, Model Server

Client compose of:
    - Client ID
    - View Server (functions):
        - Query Available Models (with Environment ID)
        - Register Model
        - Send Image
        - Receive Action
        - Execute Action
    - Environment:
        - Environment ID
        - Environment Name
        - Environment Scene
        - Environment UI
        - Environment Captor
        - Environment Action Executor

Model Server compose of:
    - Model:
        - Model ID
        - Request Looper
        - Request Executor
    - Server (functions):
        - Launch Model
        - Find suitable model for environment
        - Register Client
        - Receive Observation
        - Compute Action
        - Send Action
'''

'''
如何确认环境和模型匹配与否？
对比发过来的环境名称就行，后台维护一个环境名称和模型名称的对应表

为什么Client要先注册才能请求Action？
其实来一个请求就返回一个Action也是可行的，只是<我觉得>之后很有可能需要限制同时访问的用户数量，需要事先留个接口

可能需要处理的，简单但是繁琐的问题：
1. 未注册的用户请求Action
2. 已注册的用户重复注册
3. 注册后的用户掉线
'''

'''
相关接口(websocket接口)：
/register_client
    request:
        - client_id
        - env_id
        - env_name
    success response:
        - text: 'register success'
    fail response:
        - text: 'register fail'
        - text: fail_reason

/get_action
    request:
        - client_id
        - observation (image)
        - instruction (text)
    success response:
        - action
    fail response:
        - text: 'get action fail'
        - text: fail_reason
'''


'''
该方案并不要求Client事先安装对应库，使用时按需引入
考虑到用户用户自定义场景的需求，Client端需要提供最基本的接口
Client的预期使用方式：

```python 
# 使用预先定义的示例
python -m NotBorder.example.omnigibson_example
```

```python
# 使用自定义场景
from NotBorder import omnigibson_proxy

# init environment
env = omnigibson.OmniGibsonEnv()

### init client 
env, client = omnigibson_proxy.Client(
    client_id = 'client_1',
)

# render loop
while True:
    # action = get_action()
    # obs = env.step(action)
    action = client.get_action(obs)
    obs = env.step(action)
```

```python
# 使用自定义模拟器
from NotBorder import NBClient

# init environment
env = Unreal.Env()

client = NBClient(
    client_id = 'client_1',
    env_id = 'env_1',
    env_name = 'Unreal',
    env_action_executor = lambda action : env.step(action), # if env supports executing action in non-main thread
    # env_action_executor = lambda action : actions_queue.add(action), # if env only supports executing action in main thread
    
    view_mode = 'image_to_live',
    view_dataflow = 'active', # 'active' or 'passive'
    env_captor = lambda : env.get_observation(),
)

# render loop
while True:
    obs = env.get_observation()
    client.render(obs)
```
'''