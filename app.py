from fastapi import FastAPI
from routes.client import router as service_router

app = FastAPI(
    title="LUS API",
    version="1.0.0",
    description="Private dashboard API for Xray management"
)


app.include_router(service_router)


