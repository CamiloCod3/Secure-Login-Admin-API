from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

def setup_cors(app: FastAPI):
    environment = os.getenv("ENVIRONMENT", "production")
    
    if environment == "development":
        # Allow all origins in development mode
        cors_origins = ["*"]
    else:
        # Production settings or stricter CORS policy
        cors_origins_str = os.getenv("CORS_ORIGINS", "")
        cors_origins = cors_origins_str.split(",") if cors_origins_str else []
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )