import dart_fss as dart

# Open DART API KEY 설정
api_key='698e1025376cfbf1631574822d5744a07b1c30ea'
dart.set_api_key(api_key=api_key)

# 검색정보 쿼리
company = '삼성전자'

# DART 에 공시된 회사 리스트 불러오기
corp_list = dart.get_corp_list()

# 삼성전자 검색
corpName = corp_list.find_by_corp_name(company, exactly=True)[0]
print('연결재무제표 검색완료')


# 2012년부터 연간 연결손익계산서 불러오기
fs = corpName.extract_fs(bgn_de='20120101')

print('연결재무제표 데이터 호출 완료')

# 연결손익계산서
df_is = fs['is'] # 또는 df = fs[1] 또는 df = fs.show('is')
# 연결손익계산서 추출에 사용된 Label 정보
labels_is = fs.labels['is']

print('연결재무제표 데이터 Pasing 완료')


# # 재무제표 검색 결과를 엑셀파일로 저장 ( 기본저장위치: 실행폴더/fsdata )
# fs.save()

# 재무제표 일괄저장
filename = company
fs.save(filename=filename)
print('연결재무제표 저장완료')

