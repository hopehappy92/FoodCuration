import surprise
from pathlib import Path
import os
import django
import pandas as pd
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from api.models import Review
from matplotlib import pyplot as plt
from backend import settings
from api import models
import pickle

DATA_DIR = Path(settings.BASE_DIR).parent / "data"
DATA_FILE = str(DATA_DIR / "dump.pkl")
data = pd.read_pickle(DATA_FILE)
# print(data)
reviews = data['reviews'][["user","store","score"]]
print(reviews.columns)
print(reviews)
review_group = reviews.groupby('user')

print(review_group)
result = review_group.agg(['sum', 'count', 'mean'])

print(result)
result2 = result['score']
print(result2)

# obj = Review.objects.all().values("user_id", "store_id", "score")
# df = pd.DataFrame(list(obj))
# print(df.head(10))
# df_table = df.set_index(["user_id", "store_id"]).unstack()
# print(df_table.shape)
# print(df_table.iloc[2460:2470, 0:30].fillna(""))
# # plt.imshow(df_table)
# # plt.grid(False)
# # plt.xlabel("item")
# # plt.ylabel("user")
# # plt.title("Rate Matrix")
# # plt.show()