from fastapi import APIRouter, HTTPException, Query
from app.services.weather_service import weather_service

router = APIRouter()

@router.get("/weather")
def get_weather(city: str = Query(..., description="City name e.g. Mumbai")):
    if not city or len(city) < 2:
        raise HTTPException(
            status_code=400,
            detail="City name must be at least 2 characters"
        )

    weather = weather_service.get_weather(city)

    if not weather:
        raise HTTPException(
            status_code=404,
            detail=f"City '{city}' not found"
        )

    return {
        "success": True,
        "data": weather
    }

@router.get("/weather/multiple")
def get_multiple_cities(
    cities: str = Query(..., description="Comma separated cities e.g. Mumbai,Delhi,Pune")
):
    city_list = [c.strip() for c in cities.split(",")]

    if len(city_list) > 5:
        raise HTTPException(
            status_code=400,
            detail="Maximum 5 cities allowed per request"
        )

    results = []
    for city in city_list:
        try:
            weather = weather_service.get_weather(city)
            if weather:
                results.append(weather)
        except Exception as e:
            results.append({"city": city, "error": str(e)})

    return {
        "success": True,
        "count": len(results),
        "data": results
    }