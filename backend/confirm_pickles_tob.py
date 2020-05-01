import pandas as pd
import pickle
# import plotly.graph_objs as go
# from plotly import tools

# 읽기
with open('pickles_tob/df_cosmetics.p', 'rb') as file:
    result_df = pickle.load(file)

print(result_df)

# 그래프
# kdj_k = go.Scatter(x=result_df.new_date, y=result_df['kdj_k'], name="Fast%K")
# kdj_d = go.Scatter(x=result_df.new_date, y=result_df['kdj_d'], name="Fast%D")
# kdj_d2 = go.Scatter(x=result_df.new_date, y=result_df['kdj_d'], name="Slow%K")
# kdj_j = go.Scatter(x=result_df.new_date, y=result_df['kdj_j'], name="Slow%D")
# trade_volume = go.Bar(x=result_df.new_date, y=result_df['all_payment'], name="all_payment")

# data1 = [kdj_d2, kdj_j]
# data2 = [trade_volume]

# fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True)

# for trace in data1:
#     fig.append_trace(trace, 1,1)
# for trace in data2:
#     fig.append_trace(trace, 2,1)

# fig.show()



