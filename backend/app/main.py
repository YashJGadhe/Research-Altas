"""
ResearchAtlas Backend API

Main FastAPI application with unified researcher/publication fetching.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.database import connect_to_mongodb, close_mongodb_connection
from app.database.indexes import create_indexes
from app.database.init_db import initialize_database
from app.routes.researchers import router as researchers_router
from app.routes.auth import router as auth_router
from app.routes.citations import router as citations_router
from app.routes.faculty import router as faculty_router
from app.routes.research_papers import router as research_papers_router
from app.routes.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongodb()
    await initialize_database()
    yield
    # Shutdown
    await close_mongodb_connection()


app = FastAPI(
    title="ResearchAtlas API",
    description="Unified Research & Development Information Management System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(faculty_router)
app.include_router(citations_router)
app.include_router(research_papers_router)
app.include_router(researchers_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ResearchAtlas API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ResearchAtlas API"
    }
