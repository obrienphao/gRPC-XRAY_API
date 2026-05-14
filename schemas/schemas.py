# schemas/schemas.py

from enum import Enum
from typing import Any

from pydantic import BaseModel, EmailStr

# ==================================================
# SETTINGS
# ==================================================

class Settings(BaseModel):
    XRAY_API: str | None = None
    API_TOKEN: str | None = None
    CONFIG_PATH: str | None = None

# ==================================================
# REQUESTS
# ==================================================

class EmailRequest(BaseModel):
    email: EmailStr


class UserActionRequest(BaseModel):
    email: EmailStr
    uuid: str


class ActionType(str, Enum):
    STOP = "STOP"
    RESTART = "RESTART"
    OK = "ok"


class UserActionService(BaseModel):
    email: EmailStr
    uuid: str | None = None
    action: ActionType

# ==================================================
# RESPONSES
# ==================================================

class StandardResponse(BaseModel):
    status: str = ActionType.OK.value


class ResponseAddUser(StandardResponse):
    uuid: str


class UsageResponse(StandardResponse):
    uplink: int = 0
    downlink: int = 0
    total: int = 0


class CustomerModel(BaseModel):
    uuid: str
    email: EmailStr
    level: int = 0


class CustomersResponse(StandardResponse):
    count: int = 0
    clients: list[CustomerModel] = []