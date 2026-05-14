

from enum import Enum
from typing import Any

from pydantic import BaseModel


class Settings(BaseModel):
    XRAY_API : str = None
    API_TOKEN : str = None
    CONFIG_PATH : str = None

# ==================================================
# MODELS
# ==================================================

class EmailRequest(BaseModel):
    email: str


class UserActionRequest(BaseModel):
    email: str
    uuid: str


class DefineStatuts(str, Enum):
    STOP = "STOP"
    RESTART = "RESTART"
    

class UserActionService(BaseModel):
    email: str
    uuid: str
    action : DefineStatuts = None

class StandardResponse(BaseModel):
    status : str = "ok"

class CustomersResponse(BaseModel):
    status: StandardResponse
    customer : dict[str, Any]


class UsageResponse(BaseModel):
    status: StandardResponse
    uplink: int  = 0,
    downlink: int = 0,
    total: int =0

class ResponseAddUser(BaseModel):
    status: StandardResponse
    uui : str = None

