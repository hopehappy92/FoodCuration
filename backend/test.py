import surprise
import os
import django
import pandas as pd
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from api.models import Review
from matplotlib import pyplot as plt

obj = Review.objects.all().values("user_id", "store_id", "score")
df = pd.DataFrame(list(obj))
print(df.head(10))
df_table = df.set_index(["user_id", "store_id"]).unstack()
print(df_table.shape)
print(df_table.iloc[2460:2470, 0:30].fillna(""))
# plt.imshow(df_table)
# plt.grid(False)
# plt.xlabel("item")
# plt.ylabel("user")
# plt.title("Rate Matrix")
# plt.show()