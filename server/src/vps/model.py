from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime, date


class vpsKind(str, Enum):
    cloud = 'Cloud'
    server = 'Server'
    pc = 'PC'


class vpsBase(BaseModel):
    hostname: str
    ip: str
    port: int
    username: str
    password: str
    cpu: str
    memory: str


class vpsBaseUpdateRequest(BaseModel):
    hostname: str = None
    ip: str = None
    port: int = None
    username: str = None
    password: str = None
    cpu: str = None
    memory: str = None