from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest
from prometheus_fastapi_instrumentator import Instrumentator
import os

app = FastAPI(
    title="WeatherWatch API",
    description="Real-time weather data with caching",
    version="1.0.0"
)

from app.routes import health, weather

app.include_router(health.router)
app.include_router(weather.router, prefix="/api")

Instrumentator().instrument(app)

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return PlainTextResponse(generate_latest())

@app.get("/")
def root():
    return {
        "app": "WeatherWatch API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "weather": "/api/weather?city=Mumbai",
            "multiple": "/api/weather/multiple?cities=Mumbai,Delhi",
            "metrics": "/metrics"
        }
    }