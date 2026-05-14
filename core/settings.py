import os
from dotenv import load_dotenv
from schemas.schemas import Settings

# load environment file
load_dotenv()

#define settings params
settings =Settings(
    API_TOKEN= os.getenv("API_TOKEN"),
    XRAY_API= os.getenv("XRAY_API"),
    CONFIG_PATH=os.getenv("CONFIG_PATH")
)


