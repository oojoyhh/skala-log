"""
비동기 수집 모듈

open-meteo(날씨), countries.dev(국가 정보), ip-api(IP 위치) 3개를
httpx + asyncio.gather()로 동시에 비동기 호출한다.
"""

import asyncio

import httpx

WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=37.55&longitude=127"
    "&hourly=temperature_2m,precipitation_probability"
    "&timezone=Asia/Seoul&forecast_days=3"
)
COUNTRY_URL = "https://countries.dev/alpha/KOR"
IP_URL = "http://ip-api.com/json/"


async def fetch_json(client, name, url):
    """실제 HTTP GET 요청을 비동기로 보내고 (이름, JSON) 튜플로 반환한다.
    실패 시 예외를 그대로 올리지 않고 {"error": ...} 형태로 담아 반환해,
    한 API가 실패해도 gather() 전체가 멈추지 않도록 한다.
    """
    try:
        response = await client.get(url, timeout=10)
        response.raise_for_status()
        return name, response.json()
    except httpx.HTTPError as e:
        return name, {"error": str(e)}


async def collect_all():
    """3개 소스를 asyncio.gather()로 동시에 수집해 dict로 반환한다.
    {"weather": {...}, "country": {...}, "ip": {...}}
    """
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            fetch_json(client, "weather", WEATHER_URL),
            fetch_json(client, "country", COUNTRY_URL),
            fetch_json(client, "ip", IP_URL),
        )
    return dict(results)


if __name__ == "__main__":
    data = asyncio.run(collect_all())
    for name, payload in data.items():
        print(f"[{name}] {str(payload)[:100]}...")
