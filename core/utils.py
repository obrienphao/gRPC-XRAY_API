# api/core/utils.py

from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)

from core.settings import settings

# ==================================================
# SECURITY
# ==================================================

security = HTTPBearer()

# ==================================================
# ENV VALIDATION
# ==================================================

def env_is_available():
    """
    Verify required environment variables
    """

    required_settings = {
        "XRAY_API": settings.XRAY_API,
        "API_TOKEN": settings.API_TOKEN,
        "CONFIG_PATH": settings.CONFIG_PATH
    }

    missing = [
        key for key, value in required_settings.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            f"Missing environment variables: {', '.join(missing)}"
        )

# ==================================================
# AUTH
# ==================================================

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Verify bearer token
    """

    token = credentials.credentials

    if token != settings.API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return token