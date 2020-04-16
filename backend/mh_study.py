import pandas as pd
import pickle

# # 2019-09.csv 불러오기 
# csv_data_09 = pd.read_csv('../../data/2019-09.csv', encoding = 'CP949', 
# dtype={
#     "회원_시도명": str, 
#     "회원_시군구명": str,
#     "개인기업구분": str,
#     "성별": str,
#     "연령": str,
#     "가맹점_시도명": str,
#     "가맹점_시군구명": str,
#     "가맹점_읍면동명": str,
#     })
# # 2019-10.csv 불러오기
# csv_data_10 = pd.read_csv('../../data/2019-10.csv', encoding = 'CP949', 
# dtype={
#     "회원_시도명": str, 
#     "회원_시군구명": str,
#     "개인기업구분": str,
#     "성별": str,
#     "연령": str,
#     "가맹점_시도명": str,
#     "가맹점_시군구명": str,
#     "가맹점_읍면동명": str,
#     })

# # 컬럼값 처리, 서울로 필터링
# df_09 = csv_data_09[csv_data_09["회원_시도명"] == "서울"][["회원_시도명", "매출년월일", "가맹점업종코드", "결제금액", "회원수"]]
# df_10 = csv_data_10[csv_data_10["회원_시도명"] == "서울"][["회원_시도명", "매출년월일", "가맹점업종코드", "결제금액", "회원수"]]

# # 합치기
# df_all = pd.concat([df_09, df_10])

# # row 수 확인
# # print("9월 데이터 row 수: ", len(df_09)) # 4887435
# # print("10월 데이터 row 수: ", len(df_10)) # 5191326
# # print("전체 데이터 row 수: ", len(df_all)) # 10078761

# # 컬럼명 변경
# df_all = df_all.rename(
#     columns= {
#         '회원_시도명': 'city', 
#         '매출년월일': 'date', 
#         '가맹점업종코드': 'type_code', 
#         '결제금액': 'all_payment', 
#         '회원수': 'customers'})

# =======================pickle 사용================================

# 쓰기
# with open('df_all.p', 'wb') as file:
#     pickle.dump(df_all, file)

# 읽기
with open('df_all.p', 'rb') as file:
    df_all = pickle.load(file)

# 한식 데이터만 필터링
df_2104_type = df_all[df_all["type_code"] == 2104]

# 날짜별 그룹화, all_payment와 customers의 합
df_2104_type = df_2104_type[["date", "all_payment", "customers"]]
df_2104_sum_by_date = df_2104_type.groupby(["date"]).sum()
# df_2104_sum_by_date["avg_payment"] = df_2104_sum_by_date["all_payment"]/df_2104_sum_by_date["customers"]

df_2104_sum_by_date["week"] = df_2104_sum_by_date.reset_index().index//7
df_2104_sum_by_week = df_2104_sum_by_date.groupby(["week"]).sum()
print(df_2104_sum_by_week)

