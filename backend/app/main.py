from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db, close_db
from app.middleware.rate_limit import RateLimitMiddleware
from app.routers import auth, booths, alerts, analytics, chat

app = FastAPI(
    title="Election Assistant System",
    description="Production-ready API for election management with real-time booth tracking, alerts, and AI assistance",
    version="2.0.0"
)

# Rate limiting middleware
app.add_middleware(
    RateLimitMiddleware,
    max_requests=settings.rate_limit_max_requests,
    window_seconds=settings.rate_limit_window_seconds,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(booths.router)
app.include_router(alerts.router)
app.include_router(analytics.router)
app.include_router(chat.router)


@app.on_event("startup")
async def startup():
    """Initialize database connection"""
    await init_db()


@app.on_event("shutdown")
async def shutdown():
    """Close database connection"""
    await close_db()


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "version": "2.0.0"}
