from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import logging
from functools import wraps

logger = logging.getLogger(__name__)

# FastAPI HTTP exception handler
async def http_exception_handler(request: Request, exc: HTTPException):    
    logger.error(f"HTTP Exception: {exc.detail}", exc_info=True)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# CRUD operations exception handler decorator
def exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in {func.__name__}: {str(e)}", exc_info=True)
            raise
    return wrapper
