from .base_model import BaseModel
from .model_impl.random_model import RandomModel
from .dummy_model import DummyModel
from typing import Dict, Union, Literal

Models : Dict[Union[Literal['Virtual'], Literal['Reality'], Literal['Drone']], Dict[str, Dict[str, BaseModel]]] = {
    'Virtual': {
        'Omnigibson': {
            'dummy': DummyModel,
            'RandomOmnigibson': RandomModel
        },
        'dummy': {
            'dummyModel': DummyModel,
        }
    },
    'Reality': {
        'Unkown': {
            'dummy': DummyModel,
        }
    },
    'Drone': {
        'Unkown': {
            'dummy': DummyModel,
        }
    }
}