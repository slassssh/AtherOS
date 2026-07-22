from contextlib import asynccontextmanager
import time
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.api.deps import get_db, get_engine
from backend.app.api.schemas import ApiErrorResponse
from backend.app.api.v1.router import router as v1_router
from backend.app.config.config import settings
from backend.app.utils.exceptions import AtherOSError
from backend.app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for resource initialization and cleanup."""
    logger.info("Initializing AtherOS API server resources...")
    db = get_db()
    try:
        db.connect()
    except Exception as err:
        logger.warning(f"Database auto-connect skipped during startup: {err}")
    get_engine()
    yield
    logger.info("Cleaning up AtherOS API server resources...")
    try:
        db.disconnect()
    except Exception as err:
        logger.warning(f"Database disconnect error during shutdown: {err}")


def create_app() -> FastAPI:
    """FastAPI application factory."""
    app = FastAPI(
        title=f"{settings.app_name} API",
        version=settings.version,
        description="Production REST API layer for AtherOS AI Operating System.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )

    # 1. CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Middleware for Request ID, Logging, and Process Timing
    @app.middleware("http")
    async def request_context_middleware(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        request.state.request_id = request_id
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"

        logger.info(
            f"API Request | ID: {request_id} | {request.method} {request.url.path} "
            f"| Status: {response.status_code} | Duration: {process_time:.4f}s"
        )
        return response

    # 3. Global Exception Handler: AtherOSError
    @app.exception_handler(AtherOSError)
    async def handle_atheros_error(request: Request, exc: AtherOSError):
        req_id = getattr(request.state, "request_id", "")
        error_resp = ApiErrorResponse(
            success=False,
            error_code=exc.__class__.__name__,
            message=str(exc),
            detail=str(exc),
            request_id=req_id
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(error_resp)
        )

    # 4. Global Exception Handler: HTTPException
    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        req_id = getattr(request.state, "request_id", "")
        error_resp = ApiErrorResponse(
            success=False,
            error_code="HTTP_ERROR",
            message=str(exc.detail),
            detail=str(exc.detail),
            request_id=req_id
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(error_resp)
        )

    # 5. Global Exception Handler: RequestValidationError
    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        req_id = getattr(request.state, "request_id", "")
        error_resp = ApiErrorResponse(
            success=False,
            error_code="VALIDATION_ERROR",
            message="Request body payload failed validation",
            detail=jsonable_encoder(exc.errors()),
            request_id=req_id
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(error_resp)
        )

    # 6. Global Exception Handler: General Uncaught Exception
    @app.exception_handler(Exception)
    async def handle_generic_exception(request: Request, exc: Exception):
        req_id = getattr(request.state, "request_id", "")
        logger.exception(f"Unhandled Exception on {request.url.path}: {exc}")
        error_resp = ApiErrorResponse(
            success=False,
            error_code="INTERNAL_SERVER_ERROR",
            message="An unexpected server error occurred",
            detail=str(exc),
            request_id=req_id
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(error_resp)
        )

    # Include Versioned Routers
    app.include_router(v1_router, prefix="/api")

    return app


app = create_app()
