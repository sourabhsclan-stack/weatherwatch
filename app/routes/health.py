from fastapi import APIRouter
from datetime import datetime
from app.services.cache_service import cache
import os

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": os.getenv("APP_NAME", "WeatherWatch"),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "timestamp": datetime.utcnow().isoformat(),
        "redis_connected": cache.connected
    }