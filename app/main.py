import logging
# Related third-party imports
from fastapi import FastAPI, HTTPException
# Local application/library specific imports
from .schemas.config_schema import settings
from .endpoints import auth_endpoints
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

# Configure CORS settings
setup_cors(app)

# Include routers
app.include_router(auth_endpoints.router)

# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)