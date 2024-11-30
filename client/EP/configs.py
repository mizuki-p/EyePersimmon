from dataclasses import dataclass

@dataclass
class _Config:
    API_BASE = 'http://localhost:5000'
    VIEWER_PORT = 33601
    

Config = _Config()