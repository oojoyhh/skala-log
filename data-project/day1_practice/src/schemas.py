"""
Pydantic v2 스키마 정의

수집한 3개 API 응답(weather, country, ip)에서 필요한 필드만 뽑아
타입과 범위를 검증하는 모델들을 정의한다.
"""

from pydantic import BaseModel, Field


class HourlyData(BaseModel):
    """날씨 API의 hourly 중첩 데이터."""
    time: list[str]
    temperature_2m: list[float]
    precipitation_probability: list[int]


class WeatherRecord(BaseModel):
    """open-meteo 응답 검증 모델.
    latitude는 -90~90 범위여야 한다 (위도의 물리적 범위).
    """
    latitude: float = Field(ge=-90, le=90)
    longitude: float
    hourly: HourlyData


class CountryRecord(BaseModel):
    """countries.dev 응답 검증 모델.
    population은 0보다 커야 한다 (음수 인구는 말이 안 됨).
    """
    name: str
    capital: str
    region: str
    population: int = Field(gt=0)


class IPRecord(BaseModel):
    """ip-api 응답 검증 모델."""
    status: str
    country: str
    city: str