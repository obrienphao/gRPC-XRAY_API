# api/app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.utils import env_is_available
from routes.client import router as service_router

# ==================================================
# APP
# ==================================================

app = FastAPI(
    title="LUS API",
    version="1.0.0",
    description="Private dashboard API for Xray management"
)

# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================================
# ROUTES
# ==================================================

app.include_router(
    service_router,
    prefix="/api/v1"
)

# ==================================================
# HEALTH CHECK
# ==================================================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# ==================================================
# STARTUP EVENT
# ==================================================

@app.on_event("startup")
async def startup_event():

    env_is_available()

    print("LUS API started successfully")