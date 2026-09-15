"""
ResearchAtlas - Main FastAPI Application

Entry point for the backend API server.
Configures middleware, routes, and lifecycle events.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.database.database import connect_to_mongodb, close_mongodb_connection
from app.database.init_db import initialize_database

# Import routers
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.faculty import router as faculty_router
from app.routes.citations import router as citations_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📊 Environment: {'DEBUG' if settings.DEBUG else 'PRODUCTION'}")
    
    try:
        await connect_to_mongodb()
        await initialize_database()
        print(f"✅ {settings.APP_NAME} started successfully")
    except Exception as e:
        print(f"❌ Failed to start {settings.APP_NAME}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    
    yield
    
    # Shutdown
    try:
        await close_mongodb_connection()
        print(f"👋 {settings.APP_NAME} shutdown complete")
    except Exception as e:
        print(f"❌ Error during shutdown: {str(e)}")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Automated Research & Development Information Management System API",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unhandled exceptions gracefully."""
    import traceback
    print(f"[ERROR] Unhandled exception: {str(exc)}")
    print(traceback.format_exc())
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"An internal server error occurred: {str(exc)}"
        },
    )


# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(faculty_router)
app.include_router(citations_router)


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
    }
