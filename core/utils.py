

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.settings import settings



security = HTTPBearer()

def env_isAvailable():
    """
    Verify into env file if settings is defined
    """
        
    if not settings.XRAY_API:
        raise RuntimeError("XRAY_API missing in .env")
    if not settings.API_TOKEN:
        raise RuntimeError("API_TOKEN missing in .env")
    if not settings.CONFIG_PATH:
        raise RuntimeError("CONFIG_PATH missing in .env")


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Verify if token is available
    
    """
    token = credentials.credentials

    if token != settings.API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return True