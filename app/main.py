import logging
from fastapi import FastAPI, HTTPException
from slowapi.middleware import SlowAPIMiddleware

from .utils.rate_limiter import limiter # Limiter instance from utility module
from .schemas.config_schema import settings
from .endpoints import auth_endpoints, user_endpoints
from .utils.error_handlers import http_exception_handler
from .middleware.cors_config import setup_cors

# Configure the logging system based on settings
logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)

# Create an instance of FastAPI with conditional documentation URLs
app = FastAPI(
    title="Secure Fast API",
    docs_url="/docs" if settings.enable_docs else None,
    redoc_url="/redoc" if settings.enable_docs else None,
    openapi_url="/openapi.json" if settings.enable_docs else None
)

# Ensure the limiter instance is correctly attached to the FastAPI app
app.state.limiter = limiter
# Add the SlowAPI middleware to the app correctly
app.add_middleware(SlowAPIMiddleware)

# Configure CORS settings
setup_cors(app)

# Include routers
app.include_router(auth_endpoints.router)
app.include_router(user_endpoints.router)

# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)