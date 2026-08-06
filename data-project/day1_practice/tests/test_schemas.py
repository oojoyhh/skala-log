"""
schemas.py의 Pydantic 모델 검증 로직을 확인하는 테스트.

pytest는 이름이 test_로 시작하는 함수를 자동으로 찾아 실행한다.
"""

import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from schemas import CountryRecord, IPRecord, WeatherRecord


def test_weather_record_valid_data_passes():
    """정상 범위의 날씨 데이터는 검증을 통과해야 한다."""
    record = WeatherRecord(
        latitude=37.55,
        longitude=127.0,
        hourly={
            "time": ["2026-08-06T00:00"],
            "temperature_2m": [28.3],
            "precipitation_probability": [18],
        },
    )
    assert record.latitude == 37.55
    assert record.hourly.temperature_2m == [28.3]


def test_weather_record_latitude_out_of_range_fails():
    """위도는 -90~90 범위를 벗어나면 ValidationError가 나야 한다."""
    with pytest.raises(ValidationError):
        WeatherRecord(
            latitude=200,
            longitude=127.0,
            hourly={
                "time": ["2026-08-06T00:00"],
                "temperature_2m": [28.3],
                "precipitation_probability": [18],
            },
        )


def test_country_record_negative_population_fails():
    """인구는 0보다 커야 하므로, 음수면 ValidationError가 나야 한다."""
    with pytest.raises(ValidationError):
        CountryRecord(name="Korea", capital="Seoul", region="Asia", population=-100)


def test_ip_record_missing_required_field_fails():
    """status 필드가 없으면 ValidationError가 나야 한다."""
    with pytest.raises(ValidationError):
        IPRecord(city="Ashburn")
