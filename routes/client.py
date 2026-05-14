
#api/routes/client.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from core.helper import get_user_usage
from core.utils import verify_token
from core.helper import(
    add_client_to_xray,
    delete_client_from_xray, 
    list_clients,
    restart_client
    )

import logging
from core.settings import settings
from schemas.schemas import CustomersResponse, DefineStatuts, EmailRequest, ResponseAddUser, StandardResponse, UsageResponse, UserActionRequest, UserActionService

#define router about service
router = APIRouter()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


@router.get("/")
def home():
    return {
        "status": "ok",
        "message": "LUS API online"
    }


@router.get(
        "/usage/{email}",
        response_model=UsageResponse)
def usage(
    email: str,
    auth=Depends(verify_token)
):
    try:
        quotas =  get_user_usage(email)

        return JSONResponse(
            status_code=200,
            content= quotas
        )

    except Exception as e:
        logging.error(f"usage error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.post(
        "/add",
        response_model=ResponseAddUser)
def add_user(
    data: EmailRequest,
    auth=Depends(verify_token)
):
    try:

        _uuid = add_client_to_xray(settings.CONFIG_PATH, data.email)

       
        return JSONResponse(
            status_code=200,
            content={
                "status": "Ok",
                 "uuid": _uuid
                }
        )

    except Exception as e:
        logging.error(f"add error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.post(
        "/delete",
        response_model=StandardResponse)
def delete_user(
    data: EmailRequest,
    auth=Depends(verify_token)
):
    try:
        
        delete_client_from_xray(settings.CONFIG_PATH, data.email)

        return JSONResponse(
            status_code=200,
            content={"status": "Ok"}
        )

    except Exception as e:
        logging.error(f"delete error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.post("/stop", response_model=StandardResponse)
def stop_user(
    data: EmailRequest,
    auth=Depends(verify_token)
):
    try:
        
        delete_client_from_xray(settings.CONFIG_PATH, data.email)
        return JSONResponse(
            status_code=200,
            content={"status": "Ok"}
        )

    except Exception as e:
        logging.error(f"stop error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.post("/restart", response_model=StandardResponse)
def restart_user(
    data: UserActionRequest,
    auth=Depends(verify_token)
):
    try:
        restart_client(settings.CONFIG_PATH,data.email, data.uuid)

        return JSONResponse(
                status_code=200,
                content={"status": "Ok"}
            )

    except Exception as e:
        logging.error(f"restart error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get("/clients", response_model=CustomersResponse)
def get_clients(auth=Depends(verify_token)):
    try:
        customers =  list_clients(settings.CONFIG_PATH)
        return JSONResponse(
            status_code=200,
            content={
                "status": "Ok",
                "response":customers
                }
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.post("/service", response_model=StandardResponse)
def service(
    data : UserActionService,
    auth    =   Depends(verify_token)):
    try:
        action = data.action

        if not action :
            raise HTTPException(
            status_code=401,
            detail="Invalid structure"
            )
        if action == DefineStatuts.STOP.value:
            delete_client_from_xray(
                settings.CONFIG_PATH,
                data.email 
            )

        return JSONResponse(
            status_code=200,
            content={"status": "Ok"}
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )