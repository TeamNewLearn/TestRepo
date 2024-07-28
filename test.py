import dart_fss as dart
from dotenv import load_dotenv
import os
import json
import re
import pandas as pd

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
api_key = os.getenv('DART_API_KEY')
dart.set_api_key(api_key=api_key)

# 검색정보 쿼리
company = '삼성전자'
company_stock_code = '005930'

# DART 에 공시된 회사 리스트 불러오기
corp_list = dart.get_corp_list()

# 삼성전자 검색
corp_info = corp_list.find_by_stock_code(company_stock_code)

# 2020년부터 분기 연결재무제표 불러오기
fs = corp_info.extract_fs(bgn_de='20200101', report_tp='quarter')

# 연결손익계산서
df_is = fs['is']  # 또는 df = fs[1] 또는 df = fs.show('is')

# 컬럼 이름을 간결하게 변환하고 중복 제거
def simplify_column_name(col):
    if isinstance(col, tuple):
        # 괄호와 공백 제거
        simplified_name = re.sub(r'\[.*?\]|\(.*?\)|\s\|\s.*', '', col[0])
        return simplified_name
    return col

df_is.columns = [simplify_column_name(col) for col in df_is.columns]

# 중복된 컬럼 이름에 인덱스 추가
def make_unique(column_names):
    seen = {}
    for idx, name in enumerate(column_names):
        if name in seen:
            seen[name] += 1
            column_names[idx] = f"{name}_{seen[name]}"
        else:
            seen[name] = 0
    return column_names

df_is.columns = make_unique(df_is.columns.tolist())

# DataFrame을 JSON 형식으로 변환 (한 줄로 이어서 출력)
result_json = df_is.to_json(orient='records', force_ascii=False)

# 각 객체('}') 다음에 줄 바꿈 추가
formatted_json = result_json.replace('},', '},\n')

# JSON 출력
print(formatted_json)
