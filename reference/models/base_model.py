from abc import ABC
from typing import Any, NewType, Tuple, TypeAlias

Action : TypeAlias = Any


class BaseModel(ABC):
    def create_model(self) -> None:
        pass
    
    def create_task(self, instruction: str) -> None:
        pass

    def predict_action(self, observation) -> Action:
        pass
    
    def reset(self) -> None:
        pass