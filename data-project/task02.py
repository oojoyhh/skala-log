"""
Python Practice - 예외 처리 + Pydantic 검증 파이프라인

원본 JSON 데이터를 안전하게 불러온 뒤, Pydantic으로 각 레코드를
검증하여 정상 데이터(valid)와 오류 데이터(errors)로 분리하고,
그 결과를 각각 CSV/JSON으로 저장한 뒤 다시 읽어 건수를 확인한다.

1) safe_load_csv() - 파일 로딩 (성공/실패/종료를 로깅으로 구분)
2) SalesRecord - Pydantic 스키마 (필수값, amount > 0 규칙)
3) 검증 파이프라인 - raw_data를 순회하며 valid/errors로 분리
4) 결과 저장 - valid는 CSV, errors는 JSON으로 저장 후 재로딩 검증

변경 내역
- v1: json.loads() -> json.load(f) 수정
- v2: SalesRecord 스키마 정의 (region/month min_length=1, amount gt=0, category Optional)
- v3: model_dump(record) -> record.model_dump() 수정
- v4: json.dump에 ensure_ascii=False 적용
- v5: CSV 재로딩 검증 추가 (len(reloaded) == len(valid))
- v6: 예외 처리 보완 - JSONDecodeError 추가 처리, valid 0건 시 IndexError 방지

"""

import csv
import json
import logging
from typing import Optional

from pydantic import BaseModel, Field, ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_PATH = "Python_Practice1_Data.json"

# 1) 예외 처리 + 파일 읽기
# safe_load_csv : JSON 파일을 읽어 dict 리스트를 반환한다.
#   성공 시 - dict 리스트 반환, logger.info로 기록
#   파일 없음 / JSON 형식 오류 - None 반환, logger.error로 기록
#   finally - 성공/실패와 무관하게 항상 '로딩 종료' 출력
def safe_load_csv(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info("파일 로딩 성공")
        return data
    except FileNotFoundError:
        logger.error("파일을 찾을 수 없습니다")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON 형식이 올바르지 않습니다: {e}")
        return None
    finally:
        print('로딩 종료')

# 2) Pydantic v2 스키마 정의
# SalesRecord : 한 건의 판매 레코드가 갖춰야 할 형태를 정의한다.
#   region, month - 비어있으면 안 됨 (min_length=1)
#   amount        - 0보다 커야 함 (gt=0)
#   category      - 없어도 됨 (Optional)
class SalesRecord(BaseModel):
    region: str = Field(min_length=1)
    month: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: Optional[str] = None

# 3) 검증 파이프라인
# raw_data를 한 건씩 SalesRecord로 변환 시도한다.
#   성공 -> valid 리스트에 model_dump() 결과(순수 dict)로 저장
#   실패 -> errors 리스트에 {row: 원본, error: 에러 메시지} 형태로 저장
def build_validation_pipeline(raw_data):
    valid = []
    errors = []
    for row in raw_data:
        try:
            record = SalesRecord(**row)
            valid.append(record.model_dump())
        except ValidationError as e:
            errors.append({"row": row, "error": str(e)})
    return valid, errors

# 4) 결과 파일 저장 + 재로딩 확인
# valid는 CSV로, errors는 JSON으로 저장한 뒤
# CSV를 다시 읽어 건수가 저장 전과 같은지 확인한다.
# [예외처리] valid가 0건인 경우 valid[0]으로 컬럼명을 가져올 수 없어
#   IndexError가 나므로, 그때는 SalesRecord의 필드 목록을 대신 사용해
#   헤더만 있는 CSV를 저장하도록 처리한다 (프로그램이 죽지 않도록 함).
def save_and_reload(valid, errors):
    fieldnames = valid[0].keys() if valid else SalesRecord.model_fields.keys()

    with open('valid_output.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(valid)

    with open('errors_output.json', 'w', encoding='utf-8') as f:
        json.dump(errors, f, ensure_ascii=False, indent=2)

    with open('valid_output.csv', 'r', encoding='utf-8') as f:
        reloaded = list(csv.DictReader(f))

    return reloaded

if __name__ == "__main__":
    # 1) 파일 로딩 checkpoint
    raw_data = safe_load_csv(DATA_PATH)
    assert safe_load_csv("존재하지_않는_파일.json") is None
    print(f"[1] 로딩 성공: {len(raw_data)}건 / 없는 파일 -> None 확인")
    print()

    # 2), 3) 검증 파이프라인 checkpoint
    valid, errors = build_validation_pipeline(raw_data)
    print(f"[2-3] valid: {len(valid)}건 / errors: {len(errors)}건")
    if errors:
        print("      오류 예시:")
        print("     ", errors[0]["error"].splitlines()[0])
    print()

    # 4) 저장 + 재로딩 checkpoint
    reloaded = save_and_reload(valid, errors)
    assert len(reloaded) == len(valid)
    print(f"[4] 재로딩 건수: {len(reloaded)} (valid와 일치 확인)")