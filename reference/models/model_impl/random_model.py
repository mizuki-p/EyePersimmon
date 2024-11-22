from ..base_model import BaseModel

import torch
from random import randint
import time

class RandomModel(BaseModel):
    def create_model(self) -> None:
        pass
    
    def create_task(self, instruction: str) -> None:
        pass

    def predict_action(self, observation) -> 'action': # type: ignore
        return 2 * (torch.rand(1, 1, 21) - 0.5)
    
    def reset(self) -> None:
        pass