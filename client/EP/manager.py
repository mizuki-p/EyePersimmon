import asyncio
from uuid import uuid4

# from .Controller.wss_io import wss_io
from .Controller.fake_io import wss_io
from .Environment.base_env import BaseEnv


class ClientIDMixin:
    def get_client_id(self):
        if not hasattr(self, "m_client_id"):
            self.m_client_id = uuid4().hex
        return self.m_client_id


class BaseClient(ClientIDMixin):
    def __init__(self, env: BaseEnv):
        self.env = env
        self.inited = False
        self.registered = False

        self.task_running = False
        self.instruction = ""

    async def init(self):
        self.io = wss_io()
        await self.io.init()
        self.inited = True

    async def register(self):
        if not self.inited:
            return False, "Client not inited"
        
        if self.registered:
            return False, "Client already registered"
        
        state, msg = await self.io.register(
            self.get_client_id(), self.env.env_name, self.env.scene_name
        )
        
        if state:
            self.registered = True
        
        return state, msg

    async def get_action(self, instruction):
        if not self.inited:
            return False, "Client not inited"
        
        if not self.registered:
            return False, "Client not registered"
        
        status, msg = await self.io.request_action(
            self.get_client_id(), self.env.get_observation(), instruction
        )
        if status:
            self.env.step(msg)
        return status, msg

    def start_task(self, instruction):
        if not self.inited:
            return False, "Client not inited"
        
        if not self.registered:
            return False, "Client not registered"

        if self.task_running:
            return False, "Task already running"

        self.instruction = instruction
        self.task_running = True

        async def task():
            while self.task_running:
                await self.get_action(self.instruction)

        asyncio.create_task(task())
        return True, "Task started"

    def stop_task(self):
        if not self.inited:
            return False, "Client not inited"
        
        if not self.registered:
            return False, "Client not registered"

        if not self.task_running:
            return False, "Task not running"

        self.task_running = False
        self.instruction = ""
        return True, "Task stopped"

    def get_live_url(self):
        if not self.inited:
            return False, "Client not inited"
        return True, self.env.get_view_url()

    def check_init(self):
        return self.inited, self.env.check_init()

    def get_env_info(self):
        if not all(self.check_init()):
            return False, "Not inited"
        return True, {
            "client_id": self.get_client_id(),
            "env_name": self.env.env_name,
            "scene_name": self.env.scene_name,
        }
        
    async def reset_scene(self):
        await asyncio.get_event_loop().run_in_executor(None, self.env.reset)
        return True, "Scene reset"
        
    async def close(self):
        await self.io.close()
        self.inited = False
