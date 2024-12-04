import torch
from typing import Tuple
import asyncio
from random import randint
from ..configs import Config

class wss_io:
    def __init__(self):
        self.connected = False
    
    async def init(self):
        await asyncio.sleep(2)
        self.connected = True
    
    async def register(self, client_id, env_id, scene_name) -> Tuple[bool, str]:
        if not self.connected:
            return False, 'Websocket not connected'
        
        try: 
            response = await asyncio.wait_for(asyncio.sleep(randint(1, 11), {
                'state': True,
                'msg': 'register success'
            }), timeout=10)
        except TimeoutError as e:
            return False, 'timeout'
        
        state, msg = response['state'], response['msg']
        if state:
            return True, 'Register success'
        else:
            return False, msg


    async def request_action(self, client_id, observation, instruction):
        if not self.connected:
            return False, 'Websocket not connected'
        
        try:
            response = await asyncio.wait_for(asyncio.sleep(0.5, {
                'state': True,
                'action': randint(0, 10)
            }), timeout=30)
        except TimeoutError as e:
            return False, 'timeout'
        
        state = response['state']
        if state:
            # return True, response['action']
            return True, 2 * (torch.rand(1, 1, 21) - 0.5)
        else:
            return False, response['msg']
        
    async def close(self):
        if not self.connected:
            return False, 'Websocket not connected'
        await asyncio.sleep(2)
        self.connected = False
        return True, 'Websocket closed'
