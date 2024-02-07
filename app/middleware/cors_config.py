from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

def setup_cors(app: FastAPI):
    cors_origins_str = os.getenv("CORS_ORIGINS", "*")  # Default to allowing all if not set
    cors_origins = cors_origins_str.split(",") if cors_origins_str != "*" else ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )