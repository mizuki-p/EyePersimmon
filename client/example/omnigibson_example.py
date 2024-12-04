import os
import sys
os.environ['OMNIGIBSON_REMOTE_STREAMING'] = 'webrtc'
os.environ['OMNIGIBSON_GPU_ID'] = '9'
os.environ['CUDA_VISIBLE_DEVICES'] = '9'
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
sys.path[0] = os.getcwd()

import torch
from omnigibson.macros import gm
from omnigibson.utils.asset_utils import get_available_g_scenes, get_available_og_scenes
from omnigibson.utils.ui_utils import choose_from_options
from omnigibson.sensors import VisionSensor
import omnigibson as og

from EP.View.transfer_viewer import TransferViewer
from EP.Environment.omnigibson_env import get_env
from EP.manager import BaseClient

# gm.ASSET_PATH = "/home/wanghan/data/agent/behavior_datasets/data/assets"
# gm.DATASET_PATH = "/home/wanghan/data/agent/behavior_datasets/data/og_dataset"
# gm.KEY_PATH = "/home/wanghan/data/agent/behavior_datasets/data/omnigibson.key"


scene_options = {
    "InteractiveTraversableScene": "Procedurally generated scene with fully interactive objects",
}
scene_type = choose_from_options(
    options=scene_options, name="scene type", random_selection=True
)

# Choose the scene model to load
scenes = (
    get_available_og_scenes()
    if scene_type == "InteractiveTraversableScene"
    else get_available_g_scenes()
)
scene_model = choose_from_options(
    options=scenes, name="scene model", random_selection=True
)

scene_cfg = dict(type="Scene")
robot0_cfg = dict(
    type="FrankaPanda",
    obs_modalities=[
        "rgb"
    ],  # we're just doing a grasping demo so we don't need all observation modalities
    action_type="continuous",
    action_normalize="sticky",
)

table_cfg = dict(
    type="DatasetObject",
    name="table",
    category="breakfast_table",
    model="lcsizg",
    bounding_box=[0.5, 0.5, 0.8],
    fixed_base=True,
    position=[0.7, -0.1, 0.6],
    orientation=[0, 0, 0.707, 0.707],
)

chair_cfg = dict(
    type="DatasetObject",
    name="chair",
    category="straight_chair",
    model="amgwaw",
    bounding_box=None,
    fixed_base=False,
    position=[0.45, 0.65, 0.425],
    orientation=[0, 0, -0.9990215, -0.0442276],
)

box_cfg = dict(
    type="PrimitiveObject",
    name="box",
    primitive_type="Cube",
    rgba=[1.0, 0, 0, 1.0],
    size=0.05,
    position=[0.53, -0.1, 0.97],
)

# Compile config
cfg = dict(
    scene=scene_cfg, robots=[robot0_cfg], objects=[table_cfg, chair_cfg, box_cfg]
)

env = og.Environment(configs=cfg)

# Reset the robot
robot = env.robots[0]
robot.set_position_orientation(position=[0, 0, 0])
robot.reset()
robot.keep_still()

for sensor in robot.sensors.values():
    if isinstance(sensor, VisionSensor):
        sensor.image_height = 256
        sensor.image_width = 256


env, proxy_env = get_env(env)
invoker = BaseClient(proxy_env)
viewer = TransferViewer(invoker)

viewer.run()

try:
    while True:
        action = proxy_env.get_action()
        env.step(action)
        proxy_env.do_sth()
except KeyboardInterrupt:
    pass

viewer.close()
env.close()