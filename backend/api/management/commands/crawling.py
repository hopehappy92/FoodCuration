from api import models
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from api import models
import pandas as pd
import pickle

class Command(BaseCommand):
    def _initialize(self):
        # store_id = pd.DataFrame(models.Store.objects.filter(review_count__gte=10).values('id'))['id']
        # for id in store_id:
        #     store = models.Store.objects.get(id=id)
        #     if not store.storeimage_set.all():
        #         try:
        #             soup = BeautifulSoup(requests.get("https://www.google.com/search?q={}+{}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjyvab49fXoAhXa7GEKHQBXA9YQ_AUoAXoECAsQAw&cshid=1587348524871324&biw=1920&bih=969".format(store.store_name, store.area)).text, 'html.parser')
        #         except:
        #             pass
        #         cnt = 0
        #         for img in soup.select('td a img'):
        #             if cnt > 2:
        #                 break
        #             if img.get('src')[:5] == 'http:':
        #                 print(img.get('src'))
        #                 try:
        #                     models.StoreImage.objects.create(store_id=id, url=img.get('src'))
        #                     cnt += 1
        #                 except:
        #                     pass
        
        # print(store_id)
        # review_df = pd.DataFrame(models.Review.objects.all().values(""))
        # print(review_df)

        
        df = pd.DataFrame(models.StoreImage.objects.all().values("store_id", "url"))
        with open('store_image.p', 'wb') as f:
            pickle.dump(df, f)

        # search_base = "https://openapi.naver.com/v1/search/webkr.xml?query=다이닝코드+"
        # search_opt = "&display=10&start=1"
        # base = "https://www.diningcode.com/profile.php"
        # headers={
        #             "X-Naver-Client-Id": "HzusvK5FvwGA_OcXs0xZ",
        #             "X-Naver-Client-Secret": "o7Hh0ooCxL",
        #         }
        # stores = models.Store.objects.all()
        # for i in range(3691, len(stores)):
        #     store = stores[i]
        #     print(store.id)
        #     add = store.address
        #     store_name = store.store_name
        #     add = add.replace(' ', '+')
        #     store_name = store_name.replace(' ', '+')
        #     url = search_base+add+'+'+store_name+search_opt
        #     res = requests.get(url, headers=headers).text.split(base)
        #     if len(res) >= 2:
        #         q = res[1].split("</link>")[0]
        #         print(q)
        #         soup = BeautifulSoup(requests.get(base+q).text, 'html.parser')
        #         a = soup.select('.btn-gallery-open > img')
        #         print(a)
        #         if a:
        #             img = ''
        #             img = a[0].attrs['src']
        #             print(img)
        #             models.StoreImage.objects.create(store=store, url=img)
    def handle(self, *args, **kwargs):
        self._initialize()
