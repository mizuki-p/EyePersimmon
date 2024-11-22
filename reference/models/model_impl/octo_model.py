from .base_model import BaseModel

import jax
import cv2
import numpy as np
import torch
from octo.model.octo_model import OctoModel as OfficialOctoModel
# from octo.octo.model.octo_model import OctoModel as OfficialOctoModel

class OctoModel(BaseModel):
    def create_model(self) -> None:
        self.model = OfficialOctoModel.load_pretrained("hf://rail-berkeley/octo-small-1.5")
    
    def create_task(self, instruction: str) -> None:
        self.task = self.model.create_tasks(texts=[instruction])
        self.last_image = None

    def predict_action(self, observation) -> 'action': # type: ignore
        robot_name = list(observation[0].keys())[0]
        image = observation[0][robot_name][f'{robot_name}:wrist_eye:Camera:0']['rgb'][:, :, :3].numpy()
        image = cv2.resize(image, (256, 256))
        step_image = image[np.newaxis,np.newaxis,...]
        
        if self.last_image is None:
            self.last_image = step_image

        image = np.concatenate([self.last_image, step_image], axis = 1)
        pad_mask = np.full((1, image.shape[1]), True, dtype=bool)
        observation = {"image_primary": image, "timestep_pad_mask": pad_mask}

        action = self.model.sample_actions(observation, self.task, rng=jax.random.PRNGKey(0)) 
        action = torch.tensor(action.tolist())
        
        self.last_image = step_image
        return action
    
    def reset(self) -> None:
        self.task = None
        self.last_image = None