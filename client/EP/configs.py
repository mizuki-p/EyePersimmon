from dataclasses import dataclass

@dataclass
class _Config:
    API_BASE = 'http://localhost:5000'
    

Config = _Config()