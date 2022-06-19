import requests
import uvicorn
from fastapi import FastAPI
import os

app = FastAPI()
API_KEY = "4e8423dc93a20d3569a89fbedde07252"
BASE_URL = "http://api.openweathermap.org/data/2.5/"


@app.get("/v1/current")
async def current_weather(city: str):
    response = requests.get(BASE_URL + f"weather?units=metric&appid={API_KEY}&q={city}").json()
    return {
        "name": response["name"],
        "temperature": response["main"]["temp"],
        "units": "celsius",
    }


@app.get("/v1/forecast")
async def forecast_weather(city: str, dt: int):
    response = requests.get(BASE_URL + f"forecast?units=metric&appid={API_KEY}&q={city}").json()
    return {
        "name": response["city"]["name"],
        "temperature": find_nearest_forecast(response["list"], dt),
        "units": "celsius",
    }


def find_nearest_forecast(forecasts: list, dt: int) -> float:
    for forecast in forecasts:
        if forecast["dt"] > dt:
            return forecast["main"]["temp"]
    return 0.0


if __name__ == "__main__":
    port = os.environ.get("weather_port", 8000)
    uvicorn.run(app, host="0.0.0.0", port=port)
