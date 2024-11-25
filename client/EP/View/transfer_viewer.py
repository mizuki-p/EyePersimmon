from flask import Flask, Response, request, send_from_directory
import socketio
from flask_cors import CORS
from ..configs import Config

class TransferViewer:
    def __init__(self, put_action):
        self.put_action = put_action
        
        self.app = Flask('EP') # 第一个参数填啥我也不清楚，姑且先填个'EP'
        self.ws = socketio.Client(reconnection=True)
        CORS(self.app, supports_credentials=True, responses={r"*": {"origins": "*"}})
        
        self.ws.connect(Config.API_BASE)
        self.register_interaction()
        

    def register_interaction(self):
        
        self.app.route('/')
        def index():
            return send_from_directory('static', 'index.html')
        
        
        @self.ws.on('connect')
        def on_connect():
            print('connected')
        
        
        @self.ws.on('disconnect')
        def on_disconnect():
            print('disconnected')
            
            
        @self.ws.on('action')
        def action(action):
            self.put_action(action)
        
        
    def send_observation(self, observation):
        self.ws.emit('query_', observation)