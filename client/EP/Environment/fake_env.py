from .base_env import BaseEnv
from ..types import ViewMode

def get_env():
    env = BaseEnv(
        env_name='FakeEnv',
        scene_name='FakeScene',
        
        nop_code=1145141919,
        
        observation_captor=lambda : None,
        action_executor=lambda x: None,
        check_init=lambda : True,
        
        view_mode=ViewMode.SelfHost,
        get_view_url=lambda : 'http://127.0.0.1:5500/index.html',
    )
    return env