import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app: FastAPI):
    logger = logging.getLogger(__name__)
    environment = os.getenv("ENVIRONMENT", "production")
    
    if environment == "development":
        # Allow all origins in development mode
        cors_origins = ["*"]
        logger.info("CORS configured to allow all origins (development mode)")
    else:
        # Production settings or stricter CORS policy
        cors_origins_str = os.getenv("CORS_ORIGINS", "")
        cors_origins = cors_origins_str.split(",") if cors_origins_str else []
        logger.info(f"CORS configured for production mode with origins: {cors_origins}")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
