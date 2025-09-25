import secrets
import time
from typing import TypedDict


class WeatherResponse(TypedDict):
    city: str
    temperature: float
    humidity: int


def fetch_weather_data(city: str) -> WeatherResponse:
    time.sleep(2)

    if secrets.randbelow(10) == 0:
        raise TimeoutError(f"Timeout for city {city}")

    return {
        "city": city,
        "temperature": (secrets.randbelow(251) + 150) / 10,
        "humidity": secrets.randbelow(101),
    }
