import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

# Test 1 — Health check
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# Test 2 — Weather endpoint exists
def test_weather_endpoint_exists():
    response = client.get("/api/weather")
    # 422 = missing required parameter (city)
    # This proves endpoint EXISTS but needs city parameter
    assert response.status_code == 422

# Test 3 — City too short
def test_city_too_short():
    response = client.get("/api/weather?city=A")
    assert response.status_code == 400

# Test 4 — Too many cities
def test_too_many_cities():
    response = client.get(
        "/api/weather/multiple?cities=Mumbai,Delhi,Pune,Chennai,Kolkata,Bangalore"
    )
    assert response.status_code == 400

# Test 5 — Mock weather API call
# We mock the external API so tests don't need real API key
@patch("app.services.weather_service.requests.get")
def test_get_weather_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "Mumbai",
        "sys": {"country": "IN"},
        "main": {
            "temp": 32.5,
            "feels_like": 35.0,
            "humidity": 80
        },
        "weather": [{"description": "partly cloudy"}],
        "wind": {"speed": 4.5}
    }
    mock_get.return_value = mock_response

    response = client.get("/api/weather?city=Mumbai")
    assert response.status_code == 200
    assert response.json()["data"]["city"] == "Mumbai"
    assert response.json()["data"]["temperature"] == 32.5

# Test 6 — Mock 404 from weather API
@patch("app.services.weather_service.requests.get")
def test_city_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    response = client.get("/api/weather?city=FakeCity123")
    assert response.status_code == 404

# Test 7 — Root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["app"] == "WeatherWatch API"