from .base_model import BaseModel
import torch
from PIL import Image
import torchvision
import io
import time

def convert_image_back(obs):
    # print(obs)
    robot_name = list(obs[1].keys())[0]
    image = obs[0][robot_name][f'{robot_name}:wrist_eye:Camera:0']['rgb']
    image = Image.open(io.BytesIO(image))
    image = torchvision.transforms.functional.to_tensor(image).permute(2, 0, 1)
    obs[0][robot_name][f'{robot_name}:wrist_eye:Camera:0']['rgb'] = image
    return obs

class DummyModel(BaseModel):
    def create_model(self) -> None:
        print(f'create model')
    
    def create_task(self, instruction: str) -> None:
        print(f'create task, instruction: {instruction}')
    
    def predict_action(self, observation) -> 'action': # type: ignore
        # observation = convert_image_back(observation)
        # print(f'predict action, observation: {observation}')
        
        action = 2 * (torch.rand(1, 1, 21) - 0.5)
        return action
    
    def reset(self) -> None:
        print(f'reset model')
    