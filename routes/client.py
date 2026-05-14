# api/routes/client.py

from fastapi import APIRouter, Depends, HTTPException
from core.helper import (
    get_user_usage,
    add_client_to_xray,
    delete_client_from_xray,
    list_clients,
    restart_client
)

from core.utils import verify_token
from core.settings import settings

from schemas.schemas import (
    CustomersResponse,
    ActionType,
    EmailRequest,
    ResponseAddUser,
    StandardResponse,
    UsageResponse,
    UserActionRequest,
    UserActionService
)

import logging

# ==================================================
# LOGGER
# ==================================================

logger = logging.getLogger(__name__)

# ==================================================
# ROUTER
# ==================================================

router = APIRouter(
    prefix="/client",
    tags=["Clients"]
)

# ==================================================
# HOME
# ==================================================

@router.get("/")
def home():
    return {
        "status": ActionType.OK.value,
        "message": "LUS API online"
    }

# ==================================================
# USAGE
# ==================================================

@router.get(
    "/usage/{email}",
    response_model=UsageResponse
)
def usage(
    email: str,
    auth=Depends(verify_token)
):
    try:
        quotas = get_user_usage(email)

        return quotas

    except Exception:
        logger.exception("usage error")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# ==================================================
# ADD CLIENT
# ==================================================

@router.post(
    "/add",
    response_model=ResponseAddUser
)
def add_user(
    data: EmailRequest,
    auth=Depends(verify_token)
):
    try:

        generated_uuid = add_client_to_xray(
            settings.CONFIG_PATH,
            data.email
        )

        return {
            "status": ActionType.OK.value,
            "uuid": generated_uuid
        }

    except Exception as e:

        logger.exception("add client error")

        if "already exists" in str(e):
            raise HTTPException(
                status_code=409,
                detail="Client already exists"
            )

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# ==================================================
# DELETE CLIENT
# ==================================================

@router.post(
    "/delete",
    response_model=StandardResponse
)
def delete_user(
    data: EmailRequest,
    auth=Depends(verify_token)
):
    try:

        delete_client_from_xray(
            settings.CONFIG_PATH,
            data.email
        )

        return {
            "status": ActionType.OK.value
        }

    except Exception as e:

        logger.exception("delete client error")

        if "not found" in str(e):
            raise HTTPException(
                status_code=404,
                detail="Client not found"
            )

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# ==================================================
# STOP CLIENT
# ==================================================

@router.post(
    "/stop",
    response_model=StandardResponse
)
def stop_user(
    data: EmailRequest,
    auth=Depends(verify_token)
):
    try:

        delete_client_from_xray(
            settings.CONFIG_PATH,
            data.email
        )

        return {
            "status": ActionType.OK.value
        }

    except Exception as e:

        logger.exception("stop client error")

        if "not found" in str(e):
            raise HTTPException(
                status_code=404,
                detail="Client not found"
            )

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# ==================================================
# RESTART CLIENT
# ==================================================

@router.post(
    "/restart",
    response_model=StandardResponse
)
def restart_user(
    data: UserActionRequest,
    auth=Depends(verify_token)
):
    try:

        restart_client(
            settings.CONFIG_PATH,
            data.email,
            data.uuid
        )

        return {
            "status": ActionType.OK.value
        }

    except Exception as e:

        logger.exception("restart client error")

        if "already active" in str(e):
            raise HTTPException(
                status_code=409,
                detail="Client already active"
            )

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# ==================================================
# LIST CLIENTS
# ==================================================

@router.get(
    "/clients",
    response_model=CustomersResponse
)
def get_clients(
    auth=Depends(verify_token)
):
    try:

        customers = list_clients(
            settings.CONFIG_PATH
        )

        return {
            "status": ActionType.OK.value,
            "response": customers
        }

    except Exception:

        logger.exception("list clients error")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# ==================================================
# SERVICE ACTION
# ==================================================

@router.post(
    "/service",
    response_model=StandardResponse
)
def service(
    data: UserActionService,
    auth=Depends(verify_token)
):
    try:

        action = data.action

        if action == ActionType.STOP.value:

            delete_client_from_xray(
                settings.CONFIG_PATH,
                data.email
            )

        elif action == ActionType.RESTART.value:

            restart_client(
                settings.CONFIG_PATH,
                data.email,
                data.uuid
            )

        else:

            raise HTTPException(
                status_code=400,
                detail="Invalid action"
            )

        return {
            "status": ActionType.OK.value
        }

    except HTTPException:
        raise

    except Exception:

        logger.exception("service action error")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )