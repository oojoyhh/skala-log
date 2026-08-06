"""
Python Practice 1 - Sales 데이터 분석

작성자: 판교캠퍼스 8반 P253 김효주

sales(딕셔너리 리스트) 데이터를 갖고 아래 4가지를 실습한다.
1) 리스트/딕셔너리 컴프리헨션 - amount 필터링, 지역별 총매출 집계
2) Counter + defaultdict - 지역별 거래건수, 카테고리별 amount 리스트
3) 제너레이터 - list와의 메모리 사용량 비교
4) 종합 - 월/카테고리별 매출 집계 및 top3 정렬

예외처리는 필드 성격에 따라 다르게 처리하였다.
- region/category/month는 거래를 식별하는 필드라서,
없으면 기본값으로 채우지 않고 그 레코드 자체를 제외했다 (is_valid_record 함수).
- amount는 수치 필드라서 없거나 숫자가 아니면 0으로 간주하여도
매출없음 정도로 해석이 가능해 s.get('amount', 0)을 썼다.
- 파일 로딩(open/json.loads) 또한 실패할 수 있어 try/except로 감쌌다.

변경 내역
- v1) 최초 작성
- v2) .get('amount', 0) 일괄 적용 -> 필드 성격별 예외처리 방식 재설계
"""

import json
import os
import sys
from collections import Counter, defaultdict

# 데이터 로드
# [예외처리]
#   - 파일이 존재하지 않는 경우 (FileNotFoundError)
#   - 데이터에 '=' 구분자가 없어 split 결과가 기대와 다른 경우 (IndexError)
#   - JSON 형식이 깨진 경우 (json.JSONDecodeError)
#   위 세 가지를 모두 대비해 프로그램이 예기치 않게 죽지 않고,
#   어떤 문제인지 안내 메시지를 출력한 뒤 종료하도록 처리했다.
BASE_DIR = os.getcwd()
DATA_PATH = os.path.join(BASE_DIR, 'sk-log', 'data-project', 'data', 'Python_Practice1_Data.json')

try:
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    sales = json.loads(content.split('=', 1)[1].strip())
except FileNotFoundError:
    raise SystemExit(f"[오류] 데이터 파일을 찾을 수 없습니다: {DATA_PATH}")
except IndexError:
    raise SystemExit("[오류] 데이터 형식이 예상과 다릅니다 ('=' 구분자를 찾을 수 없음).")
except json.JSONDecodeError as e:
    raise SystemExit(f"[오류] JSON 파싱 실패: {e}")


# 데이터 검증 — 식별 필드(region/category/month) 누락 레코드 제외
# [기능 설명]
#   is_valid_record : region, category, month가 모두 존재하고,
#                      amount가 숫자 타입인 레코드만 True를 반환.
#                      식별 필드는 기본값으로 채워 넣으면 분석 결과가 왜곡되므로,
#                      기본값 대체 대신 레코드 자체를 걸러내는 방식을 택함.
def is_valid_record(s):
    has_required_keys = all(key in s for key in ('region', 'category', 'month'))
    has_valid_amount = isinstance(s.get('amount'), (int, float))
    return has_required_keys and has_valid_amount

raw_count = len(sales)
sales = [s for s in sales if is_valid_record(s)]
dropped = raw_count - len(sales)
if dropped > 0:
    print(f"필수 필드 누락/타입 오류로 {dropped}건 제외됨 (전체 {raw_count}건 중)")

# 1) 리스트/딕셔너리 컴프리헨션
# [기능 설명]
#   up1000       : amount가 1000 이상인 거래(딕셔너리)만 걸러낸 리스트
#   region_total : 지역(region)별 총매출을 담은 dict
#                  {지역명: 해당 지역 amount 합계}
# [예외처리]
#   위 검증 단계를 통과한 데이터만 남아있으므로
#   s['region'], s['amount']를 직접 인덱싱해도 안전하다.
up1000 = [s for s in sales if s['amount'] >= 1000]

regions = {s['region'] for s in sales}
region_total = {
    r: sum(s['amount'] for s in sales if s['region'] == r)
    for r in regions
}

# 2) Counter + defaultdict
# [기능 설명]
#   region_count      : 지역별 거래 건수를 세는 Counter
#   category_amounts  : 카테고리별 amount 리스트를 모으는 defaultdict(list)
region_count = Counter([s['region'] for s in sales])

category_amounts = defaultdict(list)
for s in sales:
    category_amounts[s['category']].append(s['amount'])


# 3) 제너레이터 — 메모리 비교
# [기능 설명]
#   amount_generator : amount가 1000을 초과하는 행(딕셔너리)만 하나씩
#                       yield하는 제너레이터 함수.
#   gen              : 제너레이터 객체
#   list_ver         : 동일한 조건의 리스트 컴프리헨션 버전 (비교 대상)
def amount_generator(sales):
    for s in sales:
        if s['amount'] > 1000:
            yield s

gen = amount_generator(sales)
list_ver = [s for s in sales if s['amount'] > 1000]

gen_size = sys.getsizeof(gen)
list_size = sys.getsizeof(list_ver)

# 4) 종합 — 월별 카테고리 매출 집계
# [기능 설명]
#   total_amount            : (month, category) 튜플을 키로, 해당 조합의
#                              amount 리스트를 값으로 갖는 defaultdict(list)
#   monthly_category_total  : total_amount의 각 리스트를 sum()으로 합산해
#                              (month, category) → 총매출(int) 형태로
#                              완성한 최종 dict (컴프리헨션 + defaultdict 조합)
#   top3                    : monthly_category_total에서 총매출 기준
#                              내림차순 정렬 후 상위 3개 조합
total_amount = defaultdict(list)
for s in sales:
    total_amount[s['month'], s['category']].append(s['amount'])

monthly_category_total = {key: sum(total_amount[key]) for key in total_amount}

top3 = sorted(monthly_category_total.items(), key=lambda x: x[1], reverse=True)[:3]

# 결과 확인 (Checkpoint 검증)
if __name__ == "__main__":
    # 1) region_total 값 검증
    seoul_manual = sum(s['amount'] for s in sales if s['region'] == '서울')
    assert seoul_manual == region_total['서울']
    print("[1] region_total 검증 통과:", region_total)
    print("    up1000 개수:", len(up1000))
    print()

    # 2) Counter.most_common() 순서 확인
    print("[2] region_count.most_common():")
    for region, cnt in region_count.most_common():
        print(f"    {region}: {cnt}건")
    print("    category_amounts 키:", list(category_amounts.keys()))
    print()

    # 3) generator < list 메모리 검증
    assert gen_size < list_size
    print(f"[3] 제너레이터 크기: {gen_size} bytes / 리스트 크기: {list_size} bytes (검증 통과)")
    print()

    # 4) top3 내림차순 정렬 검증
    vals = [v for _, v in top3]
    assert vals == sorted(vals, reverse=True)
    print("[4] monthly_category_total:", monthly_category_total)
    print("    top3 (내림차순):")
    for key, total in top3:
        print(f"    {key}: {total}")