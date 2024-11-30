import torch
from .base_env import BaseEnv
from ..types import ViewMode


def get_env(env):
    env_proxy = BaseEnv(
        env_name="OmniGibson",
        scene_name="TryOneTry",
        
        nop_code=torch.zeros(1, 1, 21),
        observation_captor=lambda : env.get_obs(),
        action_executor=lambda x: env.step(x),
        check_init=lambda : True,
        reset_env=lambda : env.reset(),
        
        view_mode=ViewMode.SelfHost,
        get_view_url=lambda : 'http://localhost:8080',
    )
    return env, env_proxy