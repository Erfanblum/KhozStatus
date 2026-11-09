import aiohttp
from typing import Any

CITIES = {
    "اهواز": (31.32, 48.67),
    "آبادان": (30.34, 48.30),
    "خرمشهر": (30.43, 48.18),
    "دزفول": (32.38, 48.40),
    "بهبهان": (30.60, 50.24),
    "ماهشهر": (30.56, 49.19),
}

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
AIR_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

async def fetch_city(session: aiohttp.ClientSession, name: str, lat: float, lon: float) -> dict[str, Any]:
    w_params = {
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,precipitation,weather_code",
        "timezone": "auto",
    }
    a_params = {
        "latitude": lat, "longitude": lon,
        "current": "european_aqi,pm2_5,pm10",
        "timezone": "auto",
    }
    async with session.get(WEATHER_URL, params=w_params) as r:
        w = await r.json()
    async with session.get(AIR_URL, params=a_params) as r:
        a = await r.json()
    return {
        "city": name,
        "temp": w.get("current", {}).get("temperature_2m"),
        "precip": w.get("current", {}).get("precipitation"),
        "weather_code": w.get("current", {}).get("weather_code"),
        "aqi": a.get("current", {}).get("european_aqi"),
        "pm2_5": a.get("current", {}).get("pm2_5"),
    }

async def fetch_all() -> list[dict]:
    async with aiohttp.ClientSession() as s:
        tasks = [fetch_city(s, n, la, lo) for n, (la, lo) in CITIES.items()]
        return await asyncio.gather(*tasks)