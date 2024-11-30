from typing import Tuple

import socketio
from ..configs import Config

class wss_io:
    def __init__(self):
        self.sio = socketio.AsyncClient()
    
    async def init(self):
        await self.sio.connect(Config.API_BASE)
    
    async def register(self, client_id, env_id, scene_name) -> Tuple[bool, str]:
        if not self.sio.connected:
            return False, 'Websocket not connected'
        
        try: 
            response = await self.sio.call('register_client', {
                'client_id': client_id,
                'env_id': env_id,
                'scene_name': scene_name
            }, namespace='/', timeout=10)
        except TimeoutError as e:
            return False, 'timeout'
        
        status, msg = response['status'], response['msg']
        if status:
            return True, 'Register success'
        else:
            return False, msg


    async def request_action(self, client_id, observation, instruction):
        if not self.sio.connected:
            return False, 'Websocket not connected'
        
        try:
            response = await self.sio.call('get_action', {
                'client_id': client_id,
                'observation': observation, 
                'instruction': instruction
            }, namespace='/', timeout=30)
        except TimeoutError as e:
            return False, 'timeout'
            
        
        status = response['status']
        if status:
            return True, response['action']
        else:
            return False, response['msg']

    async def close(self):
        if not self.sio.connected:
            return False, 'Websocket not connected'
        await self.sio.disconnect()
        self.sio = None
        return True, 'Websocket closed'