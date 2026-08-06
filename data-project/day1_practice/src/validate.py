"""
검증 파이프라인

collect_all()로 수집한 {"weather": ..., "country": ..., "ip": ...}를
각 소스에 맞는 Pydantic 모델로 검증해 valid(성공)/errors(실패)로 분리한다.
"""

from pydantic import ValidationError

from schemas import CountryRecord, IPRecord, WeatherRecord

SCHEMA_MAP = {
    "weather": WeatherRecord,
    "country": CountryRecord,
    "ip": IPRecord,
}


def validate_all(raw_results):
    """raw_results를 소스별로 맞는 모델에 넣어 검증한다.
    성공 -> valid[소스이름] = 검증된 모델 객체
    실패 -> errors 리스트에 {source, error} 형태로 추가 (어느 소스에서
    왜 실패했는지 바로 확인 가능)
    """
    valid = {}
    errors = []
    for name, payload in raw_results.items():
        model_class = SCHEMA_MAP[name]
        try:
            record = model_class(**payload)
            valid[name] = record
        except ValidationError as e:
            errors.append({"source": name, "error": str(e)})
    return valid, errors


if __name__ == "__main__":
    import asyncio

    from collect import collect_all

    raw_results = asyncio.run(collect_all())
    valid, errors = validate_all(raw_results)

    print(f"valid: {list(valid.keys())}")
    print(f"errors: {len(errors)}건")
    for e in errors:
        print(f"  - {e['source']}: {e['error'].splitlines()[0]}")
