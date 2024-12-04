from EP.View.transfer_viewer import TransferViewer
from EP.manager import BaseClient
from EP.Environment.fake_env import get_env

class Envrionment:
    def step(slef, action):
        pass
    
    def close(self):
        pass

proxy_env = get_env()
invoker = BaseClient(proxy_env)
viewer = TransferViewer(invoker)

viewer.run()

env = Envrionment()
while True:
    action = proxy_env.get_action()
    env.step(action)
    
viewer.close()
env.close()

