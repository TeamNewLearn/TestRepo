from flask import Flask, request, jsonify
from flask_cors import CORS
import dart_fss as dart
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import re

app = Flask(__name__)
CORS(app)

load_dotenv()

api_key = os.getenv('DART_API_KEY')
dart.set_api_key(api_key=api_key)

# DART에 공시된 회사 리스트 불러오기
corp_list = dart.get_corp_list()

def get_company_code(company_name):
    corp_info = corp_list.find_by_corp_name(company_name, exactly=True)
    if corp_info:
        return corp_info[0].corp_code
    return None

def get_start_date(years):
    today = datetime.today()
    start_date = today - timedelta(days=365 * years)
    return start_date.strftime('%Y%m%d')

@app.route('/financial_statements', methods=['POST'])
def financial_statements():
    data = request.json
    company_name = data.get('company_name')
    period = data.get('period')

    if period not in [3, 5]:
        return jsonify({'error': 'Invalid period. Please choose 3 or 5 years.'}), 400

    company_code = get_company_code(company_name)
    if not company_code:
        return jsonify({'error': 'Company not found.'}), 404

    start_date = get_start_date(period)

    corp_info = corp_list.find_by_corp_code(company_code)
    fs = corp_info.extract_fs(bgn_de=start_date, report_tp='quarter')
    df_is = fs['is']

    # 컬럼 이름을 간결하게 변환하고 중복 제거
    def simplify_column_name(col):
        if isinstance(col, tuple):
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

    # DataFrame을 JSON 형식으로 변환
    result_json = df_is.to_json(orient='records', force_ascii=False)
    formatted_json = result_json.replace('}, {', '},\n{')

    return result_json, 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # 포트를 5001로 변경
