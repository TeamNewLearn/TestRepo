import pandas as pd

# 엑셀 파일을 읽어옵니다
file_path = 'fsdata/00126380_quarter.xlsx'
all_sheets = pd.read_excel(file_path, sheet_name=None)

# 각 시트를 데이터프레임으로 출력합니다
for sheet_name, df in all_sheets.items():
    print(f"Sheet name: {sheet_name}")
    print(df)
