import pandas as pd
import pickle
import plotly.graph_objs as go
from plotly import tools

# # 2019-09.csv 불러오기 
# csv_data_09 = pd.read_csv('../../data/2019-09.csv', encoding = 'CP949', 
# dtype={
#     "회원_시도명": str, 
#     "회원_시군구명": str,
#     "개인기업구분": str,
#     "성별": str,
#     "연령": str,
#     "매출년월일": str,
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
#     "매출년월일": str,
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
# with open('pickles_tob/df_all.p', 'wb') as file:
#     pickle.dump(df_all, file)

# 읽기
with open('pickles_tob/df_all.p', 'rb') as file:
    df_all = pickle.load(file)

# 업종별 코드로 데이터 필터링
df_2104_type = df_all[df_all["type_code"] == 2104]

# 일별 그룹화, all_payment와 customers의 합
df_2104_type = df_2104_type[["date", "all_payment", "customers"]]
df_2104_sum_by_date = df_2104_type.groupby(["date"]).sum()
df_2104_sum_by_date["avg_payment"] = df_2104_sum_by_date["all_payment"]/df_2104_sum_by_date["customers"]

# 주별
# df_2104_sum_by_date["week"] = df_2104_sum_by_date.reset_index().index//7
# df_2104_sum_by_week = df_2104_sum_by_date.groupby(["week"]).sum()

# 날짜 타입 변경
df_2104_sum_by_date["date"] = df_2104_sum_by_date.index
df_2104_sum_by_date_copy = df_2104_sum_by_date.copy()
df_2104_sum_by_date_copy["new_date"] = df_2104_sum_by_date_copy["date"].map(lambda x: "20" + x[:2] + "-" + x[2:4] + "-" + x[4:])
df_2104_sum_by_date_copy["new_date"] = pd.to_datetime(df_2104_sum_by_date_copy["new_date"])

changed_df = df_2104_sum_by_date_copy[["all_payment", "customers", "avg_payment", "new_date"]]
# print(changed_df)

# 일자(n,m,t)에 따른 Stochastic(KDJ)의 값을 구하기 위해 함수형태로 만듬
def get_stochastic(df, n=15, m=5, t=3):
    
    # 입력받은 값이 dataframe이라는 것을 정의해줌
    df = pd.DataFrame(df)
    
    # n일중 최고가
    ndays_high = df.all_payment.rolling(window=n, min_periods=1).max()
    # n일중 최저가
    ndays_low = df.all_payment.rolling(window=n, min_periods=1).min()
 
    # Fast%K 계산
    kdj_k = ((df.all_payment - ndays_low) / (ndays_high - ndays_low))*100
    # Fast%D (=Slow%K) 계산
    kdj_d = kdj_k.ewm(span=m).mean()
    # Slow%D 계산
    kdj_j = kdj_d.ewm(span=t).mean()
 
    # dataframe에 컬럼 추가
    df = df.assign(kdj_k=kdj_k, kdj_d=kdj_d, kdj_j=kdj_j).dropna()
    
    return df

result_df = get_stochastic(changed_df)
# 최종결과
print(result_df)


# 그래프
kdj_k = go.Scatter(x=result_df.new_date, y=result_df['kdj_k'], name="Fast%K")
kdj_d = go.Scatter(x=result_df.new_date, y=result_df['kdj_d'], name="Fast%D")
kdj_d2 = go.Scatter(x=result_df.new_date, y=result_df['kdj_d'], name="Slow%K")
kdj_j = go.Scatter(x=result_df.new_date, y=result_df['kdj_j'], name="Slow%D")
trade_volume = go.Bar(x=result_df.new_date, y=result_df['all_payment'], name="all_payment")

data1 = [kdj_d2, kdj_j]
data2 = [trade_volume]

fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True)

for trace in data1:
    fig.append_trace(trace, 1,1)
for trace in data2:
    fig.append_trace(trace, 2,1)

fig.show()



