import os
import sys
sys.path[0] = os.getcwd()

from EP.View.transfer_viewer import TransferViewer
from EP.Environment.stream_sender_env import get_env
from EP.manager import BaseClient


env = get_env()
invoker = BaseClient(env)
viewer = TransferViewer(invoker)

viewer.run()

try:
    while True:
        pass
except KeyboardInterrupt:
    pass

viewer.close()