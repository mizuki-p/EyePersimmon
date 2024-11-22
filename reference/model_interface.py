import pickle
import socketio
from argparse import ArgumentParser
from models.base_model import BaseModel
from models import Models
from Config import Config


class ModelProxy:
    def __init__(self, env_type, env_platform, model_name):
        self.env_type = env_type
        self.env_platform = env_platform
        self.model_name = model_name
        self.model: BaseModel = Models[env_type][env_platform][model_name]()
        
        self.running = False
        
        self.server_socket = socketio.Client()
        self.register_server_socket_event()
        self.server_socket.connect(Config.base_url)

        
    def register_server_socket_event(self):
        @self.server_socket.on('connect')
        def on_connect():
            self.server_socket.emit('register_model', {
                'situation': self.env_type,
                'platform': self.env_platform,
                'model': self.model_name
            })
        
        @self.server_socket.on('create_model')
        def on_receive_creating_model():
            self.model.create_model()
            self.running = True
        
        @self.server_socket.on('create_task')
        def on_receive_creating_task(instruction):
            self.model.create_task(instruction)
            self.request_for_envrionment()
        
        @self.server_socket.on('observation')
        def on_receive_observation(observation):
            observation = pickle.loads(observation)
            action = self.model.predict_action(observation)
            action = pickle.dumps(action)
            self.server_socket.emit('action', action)
            
        @self.server_socket.on('action_impact')
        def on_receive_action_impact(impact):
            # print(f'action impact: {impact}')
            self.request_for_envrionment()
            
        @self.server_socket.on('task_finsihed')
        def on_receive_task_finished():
            self.model.reset()
            
        @self.server_socket.on('is_running')
        def on_receive_is_running():
            self.server_socket.emit('running', self.running)
    
    
    def request_for_envrionment(self):
        assert self.server_socket.connected, 'envrionment socket is not connected'
        self.server_socket.emit('request_envrionment')


    def run(self):
        while self.server_socket is not None and self.server_socket.connected:
            self.server_socket.wait()
            # self.server_socket.connect(Config.base_url)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--env_type', type=str, required=True)
    parser.add_argument('--env_platform', type=str, required=True)
    parser.add_argument('--model_name', type=str, required=True)
    args = parser.parse_args()
    
    model_proxy = ModelProxy(args.env_type, args.env_platform, args.model_name)
    model_proxy.run()