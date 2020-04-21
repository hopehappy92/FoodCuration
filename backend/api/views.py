from django.shortcuts import render, get_object_or_404, redirect
from api import models, serializers
from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.schemas import AutoSchema
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import CustomUser, Store, UserLikeStore, Algorithm, Review, StoreImage
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import datetime
from rest_auth.views import LoginView
import pandas as pd
import pickle
import surprise
import heapq
import requests
from bs4 import BeautifulSoup
from math import acos, cos, sin, radians


# 메서드 정리
# class UserViewSet(viewsets.ViewSet):
#     """
#     Example empty viewset demonstrating the standard
#     actions that will be handled by a router class.

#     If you're using format suffixes, make sure to also include
#     the `format=None` keyword argument for each action.
#     """

#     def list(self, request):
#         pass
#     def create(self, request):
#         pass
#     def retrieve(self, request, pk=None):
#         pass
#     def update(self, request, pk=None):
#         pass
#     def partial_update(self, request, pk=None):
#         pass
#     def destroy(self, request, pk=None):
#         pass


# 이미지 크롤링이 필요한 매장 id
get_image_dict = dict()

# 자동으로 크롤링 시작할 get_image_dict 길이
start_crawling_length = 1000

all_store = Store.objects.all()

def check_image(serializer):
    global get_image_dict
    for data in serializer.data:
        if not data["images"]:
            if get_image_dict.get(data["id"]):
                get_image_dict[data["id"]] += 1
            else:
                get_image_dict[data["id"]] = 1
    if len(get_image_dict) > start_crawling_length:
        crawling()

def crawling():
    global get_image_dict
    Q = []
    for key, value in get_image_dict.items():
        heapq.heappush(Q, [-value, key])
    while Q:
        _, store_id = heapq.heappop(Q)
        store = Store.objects.get(id=store_id)
        soup = BeautifulSoup(requests.get("https://www.google.com/search?q={}+{}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjyvab49fXoAhXa7GEKHQBXA9YQ_AUoAXoECAsQAw&cshid=1587348524871324&biw=1920&bih=969#imgrc=RakknToj3buHrM".format(store.store_name, store.area)).text, 'html.parser')
        # print(soup.select('td a img'))
        cnt = 0
        for img in soup.select('td a img'):
            # print(img.get('src')[5])
            if img.get('src')[:5] == 'http:':
                try:
                    StoreImage.objects.create(store_id=store_id, url=img.get('src'))
                    cnt += 1
                except:
                    pass
            if cnt > 3:
                del get_image_dict[store_id]
                break
    
    df = pd.DataFrame(StoreImage.objects.all().values("store_id", "url"))
    with open('store_image.p', 'wb') as f:
        pickle.dump(df, f)


@api_view(['GET'])
def crawling_check(self):
    global get_image_dict
    return Response(get_image_dict)


@api_view(['GET'])
def crawling_start(self):
    crawling()
    return Response(get_image_dict)


with open('svdpp.p', 'rb') as file:
    svdpp = pickle.load(file)
with open('knn.p', 'rb') as file:
    knn = pickle.load(file)
with open('learning_dataframe.p', 'rb') as file:
    learning_dataframe = pickle.load(file)

with open('df_all_tob_list.p', 'rb') as file:
    df_tob_list = pickle.load(file)

@api_view(['GET'])
def trend_by_tob(self, tob_id):
    global df_tob_list
    return Response(df_tob_list[tob_id][["new_date", "kdj_d", "kdj_j"]])

def go_to_myhome(request):
    return redirect("http://localhost:8080/")

class CustomLoginView(LoginView):
    def get_response(self):
        user = get_object_or_404(CustomUser, username=self.user)
        # print(self.user)
        orginal_response = super().get_response()
        mydata = {
            "gender": user.gender,
            "age": user.age,
            "review_count": user.review_count,
            "is_staff": user.is_staff,
            "category_list": user.category_list,
            "status": "success",
            }
        orginal_response.data["user"].update(mydata)
        return orginal_response


class SmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    pagination_class = SmallPagination
    
    def get_queryset(self):
        name = self.request.query_params.get("name", "")
        queryset = (
            models.Store.objects.all().filter(store_name__contains=name).order_by("id")
        )
        return queryset


class UserReviewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        user = self.request.query_params.get("user", "")
        content = self.request.query_params.get("content", "")
        store_name = self.request.query_params.get("store_name", "")
        # 매장명, 
        if user:
            # print(dir(models.Review.objects.filter(user_id=user).filter(content__contains=content)))
            # print(models.Review.objects.filter(user_id=user).filter(content__contains=content))
            User = models.CustomUser.objects.get(id=user)
            reviews = models.Review.objects.filter(user_id=user)
            if content:
                if store_name:
                    queryset = (
                        reviews.filter(content__contains=content)|User.review_set.filter(store_name__contains=store_name)
                    )
                else:
                    queryset = (
                        reviews.filter(content__contains=content)
                    )
            elif store_name:
                queryset = (
                    User.review_set.filter(store_name__contains=store_name)
                )
            else:
                queryset = (
                    reviews
                )
        else:
            queryset = (
                models.Review.objects.filter(content__contains=content).filter(store_name__contains=store_name)
            )            
        return queryset


class StoreReviewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        queryset = (
            models.Review.objects.all()
        )
        return queryset

    def create(self, request):
        # 리뷰를 작성하는 함수입니다.
        # if request.user.is_authenticated:
        #     data = request.data
        #     review = models.Review.objects.create(store_id=data["store"], user_id=request.user.id, content=data["content"], score=data["score"], reg_time=datetime.datetime.now())
        #     return Response("작성 성공")
        # else:
        #     return Response("작성 실패")
        data = request.data
        store = Store.objects.get(id=data["store"])
        store_name = store.store_name
        user = CustomUser.objects.get(id=data["user"])

        # 받아온 데이터를 이용해서 Review를 작성합니다.
        models.Review.objects.create(store_id=data["store"], user_id=data["user"], content=data["content"], score=data["score"], reg_time=datetime.datetime.now(), store_name=store_name)
        
        # 작성이 완료되었다면 매장과 유저의 review_count를 1씩 추가합니다.
        store.review_count += 1
        store.save()
        user.review_count += 1
        user.save()
        return Response("작성 성공")

    def update(self, request, pk=None):
        '''
        받아온 데이터에서 평점과 내용을 가져와 리뷰 객체를 수정합니다.
        '''
        review = models.Review.objects.get(id=pk)
        if request.data.get("score"):
            review.score = request.data["score"]
        if request.data.get("content"):
            review.content = request.data["content"]
        review.save()
        return Response("수정 성공")

    def destroy(self, request, pk=None):
        '''
        받아온 pk에 해당하는 리뷰를 삭제합니다.
        '''
        review = models.Review.objects.get(id=pk)
        user = models.CustomUser.objects.get(id=review.user_id)
        store = models.Store.objects.get(id=review.store_id)
        review.delete()
        user.review_count -= 1
        user.save()
        store.review_count -= 1
        store.save()
        return Response("삭제 성공")


@api_view(['GET'])
def store_reviews(self, store_id):
    serializer = serializers.ReviewSerializer(models.Review.objects.filter(store_id=store_id), many=True)
    return Response(serializer.data)


@api_view(['POST'])
def search_store(self):
    '''
    입력 데이터
    {
        "latitude": float,
        "longitude": float,
        "words": string,
        "dis": int  ... (1 = 1m)
    }
    '''
    clon = self.data.get("longitude")
    clat = self.data.get("latitude")
    dis = self.data.get("dis")
    # 위치 정보가 없으면 오류 반환
    if not clon or not clat or not dis:
        return Response("위치 정보가 없습니다.")

    queryset = []
    dis /= 1000
    for store in all_store:
        lat = store.latitude
        lon = store.longitude
        if 6371*acos(cos(radians(lat))*cos(radians(clat))*cos(radians(clon)-radians(lon))+sin(radians(lat))*sin(radians(clat))) < dis:
            queryset.append(store)
    words = []
    # 검색어를 입력받아 띄워쓰기별로 나눠줍니다.
    if self.data.get("words"):
        words = self.data["words"].split()
    
    a = []
    if words:
        # 검색어가 존재할 경우 매장목록에 대해서 반복문을 돌면서
        # 검색 단어가 포함된 매장명이나 검색 단어가 포함된 메뉴가 있을 경우
        # a라는 리스트에 해당 매장을 추가합니다.
        for store in queryset:
            # print(store.location)
            chk = 0
            for word in words:
                if store.store_name in word:
                    chk = 1
                    break
            if chk:
                a.append(store)
                continue
            for menu in store.menu_set.all():
                for word in words:
                    if word in menu.menu_name:
                        chk = 1
                        break
                if chk:
                    break
            if chk:
                a.append(store)
        # 검색어에 해당하는 매장이 담긴 a 리스트를 직렬화합니다.
        serializer = serializers.StoreSerializer(a, many=True)
    else:
        serializer = serializers.StoreSerializer(queryset, many=True)
    # 데이터를 반환합니다.

    # print(a)
    return Response(serializer.data)


class StoreDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreDetailSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        name = self.request.query_params.get("name", "")
        queryset = (
            models.Store.objects.all().filter(store_name__contains=name).order_by("id")
        )
        return queryset
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            check_image(serializer)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        check_image(serializer)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    
    @api_view(['GET'])
    def get_queryset(self):
        serializer = serializers.UserSerializer(models.CustomUser.objects.filter(review_count__gte=10), many=True)
        # print(serializer.data)
        return Response(serializer.data)
    
    @api_view(['POST'])
    def user_delete(self):
        if self.user.is_authenticated == False:
            return Response("삭제 실패")
        else:
            user = get_object_or_404(CustomUser, username=self.user)
            user.is_active = False
            user.save()
            return Response("삭제 성공")


class StoreViewSet2(viewsets.GenericViewSet):
    serializer_class = serializers.StoreSerializer2

    @api_view(['GET'])
    def get_queryset(self, review_count):
        # review_count = self.request.query_params.get("review_count", "")
        serializer = serializers.StoreSerializer2(models.Store.objects.filter(review_count__gte=review_count), many=True)
        return Response(serializer.data)


class like_store(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.LikeUserSerializer
    @api_view(['POST'])
    def get_queryset(self, user_id, store_id):        
        a = get_object_or_404(get_user_model(), pk=user_id)
        b = get_object_or_404(Store, id=store_id)
        if a.like_stores.filter(id=store_id):
            a.like_stores.remove(b)
            return Response("좋아요 취소")
        else:
            a.like_stores.add(b)
            return Response("좋아요")

    def create(self, request):
        # UserLikeStore.objects.create(customuser_id=request.user.id, store_id=request.data["store_id"])
        # like = UserLikeStore.objects.filter(customuser_id = 68632, store_id = 15)
        # like[0].delete()
        if request.user.is_authenticated:
            like = UserLikeStore.objects.filter(customuser_id = request.user.id, store_id = request.data["store_id"])
            if like:
                like[0].delete()
                return Response("좋아요 취소")
            else:
                UserLikeStore.objects.create(customuser_id=request.user.id, store_id=request.data["store_id"])
                return Response("좋아요 등록")
        else:
            return Response("비 인증 유저")

@api_view(['GET'])
def review_list(self):
    serializer = serializers.ReviewSerializer2(models.Review.objects.all(), many=True)
    return Response(serializer.data)


@api_view(['GET'])
def algorithm_check(self):
    return Response(Algorithm.objects.get(id=1).alg_name)


@api_view(['PUT'])
def algorithm_change(self):
    """
    put
    {
        "algorithm": "0" # algorithm_list_index. svdpp
    }

    algorithm_list = {
        0: "svdpp",
        1: "knn",
    }
    """
    algorithm_list = ["svdpp", "knn"]
    algorithm = Algorithm.objects.get(id=1)
    algorithm.alg_name = algorithm_list[int(self.data["algorithm"])]
    algorithm.save()
    return Response(Algorithm.objects.get(id=1).alg_name)


@api_view(['GET'])
def update_learning_dataframe(self):
    global learning_dataframe
    userset = set()
    for user in CustomUser.objects.filter(review_count__gte=10).values("id"):
        userset.add(user['id'])
    # 리뷰가 열개 이상인 매장
    storeset = set()
    for store in Store.objects.filter(review_count__gte=10).values("id"):
        storeset.add(store['id'])
    df = pd.DataFrame(Review.objects.all().values("user", "store", "score"))
    df = df[df["user"].isin(userset) & df["store"].isin(storeset)]
    
    with open('learning_dataframe.p', 'wb') as f:
        pickle.dump(df, f)
    learning_dataframe = df
    return Response("갱신 완료")


@api_view(['GET'])
def relearning_current_model(self):
    global svdpp, knn
    alg_name = Algorithm.objects.get(id=1).alg_name
    reader = surprise.Reader(rating_scale=(1, 5))
    with open('learning_dataframe.p', 'rb') as file:
        df = pickle.load(file)
    data = surprise.Dataset.load_from_df(df, reader)
    trainset = data.build_full_trainset()
    if alg_name == 'svdpp':
        alg = surprise.SVDpp()
        output = alg.fit(trainset)
        svdpp = alg
        with open('svdpp.p', 'wb') as file:
            pickle.dump(alg, file)
    elif alg_name == 'knn':
        sim_options = {'name': 'pearson', 'user_based': True}
        alg = surprise.KNNBaseline(k=30, sim_options=sim_options)
        output = alg.fit(trainset)
        knn = alg
        with open('knn.p', 'wb') as file:
            pickle.dump(alg, file)
    else:
        return Response("알고리즘 식별 불가")
    
    return Response("{} 갱신 완료".format(alg_name))


@api_view(['GET'])
def user_based_cf(self, user_id):
    alg_name = Algorithm.objects.get(id=1).alg_name
    df = learning_dataframe[learning_dataframe["user"] != user_id]
    stores = df["store"]
    arr = []
    arr2 = []
    if alg_name == 'svdpp':
        alg = svdpp
    elif alg_name == 'knn':
        alg = knn
    
    for store in stores.unique():
        arr.append([store, alg.predict(uid=user_id, iid=store).est])
        arr2.append(store)
    arr.sort(key = lambda x: x[1], reverse=True)
    print(arr[:15])
    return Response([store for store, score in arr[:15]])


@api_view(['POST'])
def create_store(self):
    print('asdfasdf')
    try:
        print(dir(self))
        print(self.data)
        print("fsdfsdf")
        print(self.query_params)
        store_name = self.data.get("store_name")
        branch = self.data.get("branch")
        area = self.data.get("area")
        tel = self.data.get("tel")
        address = self.data.get("address")
        latitude = self.data.get("latitude")
        longitude = self.data.get("longitude")
        category = self.data.get("category")
        tag = self.data.get("tag")
        menues = self.data.get("menues")
        cid = Store.objects.all().order_by('-id')[0].id + 1
        print(cid)
        Store.objects.create(id=cid, store_name=store_name, branch=branch, area=area, tel=tel, address=address, latitude=latitude, longitude=longitude, category=category, tag=tag)
    except:
        return Response("매장 등록 실패")
    for menu in menues:
        try:
            Menu.objects.create(store_id=cid, menu_name=menu["menu_name"], price=menu["price"])
        except:
            pass
    return Response("매장 등록 완료")


@api_view(['POST'])
def set_user_category(self):
    category = self.data.get("category")
    user = CustomUser.objects.get(id=self.user_id)
    user.category = cagtegory
    user.save()
    return Response("카테고리 등록 완료")