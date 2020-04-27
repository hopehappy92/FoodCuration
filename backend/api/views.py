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
from sklearn.cluster import KMeans



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

male_value = 15
female_value = 0
min_review = 5
with open('k_means.p', 'rb') as f:
    cluster_list = pickle.load(f)
    centroid = pickle.load(f)

def get_cluster(age, gender):
    def gender_to_integer(gender):
        if gender=='남':
            return male_value
        else:
            return female_value
    gtoi = gender_to_integer(gender)
    index = -1
    init_distance = 9999999
    for i in range(5):
        distance_y = centroid[i][0]
        distance_x = centroid[i][1]
        distance = (distance_y-age)*(distance_y-age) + (distance_x-gtoi)*(distance_x-gtoi)
        if(init_distance>distance):
            init_distance = distance
            index = i
    return index


# 이미지 크롤링이 필요한 매장 id
get_image_dict = dict()

# 자동으로 크롤링 시작할 get_image_dict 길이
start_crawling_length = 100

all_store = Store.objects.all()
all_review = Review.objects.all()

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
    cnt2 = 30
    for key, value in get_image_dict.items():
        heapq.heappush(Q, [-value, key])
    while Q:
        _, store_id = heapq.heappop(Q)
        store = Store.objects.get(id=store_id)
        try:
            soup = BeautifulSoup(requests.get("https://www.google.com/search?q={}+{}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjyvab49fXoAhXa7GEKHQBXA9YQ_AUoAXoECAsQAw&cshid=1587348524871324&biw=1920&bih=969".format(store.store_name, store.area)).text, 'html.parser')
            cnt2 -= 1
        except:
            continue
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
            if cnt > 2:
                del get_image_dict[store_id]
                break
        if not cnt2:
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

with open('chain_result_list.p', 'rb') as file:
    chain_result_list = pickle.load(file)

with open('age_time_list.p', 'rb') as file:
    age_time_list = pickle.load(file)

@api_view(['GET'])
def district_by_age_time(self):
    global age_time_list
    age_time_dict = {
        "나이대별": age_time_list[0],
        "시간대별": age_time_list[1],
    }
    return Response(age_time_dict)

@api_view(['GET'])
def compare_with_chain(self):
    global chain_result_list
    chain_dict = {
        "체인점 평점 순위": chain_result_list[0],
        "비체인/체인/전체 평점 비교": chain_result_list[1],
    }
    return Response(chain_dict)

@api_view(['GET'])
def trend_by_tob(self):
    global df_tob_list
    tob_dict = {
        "의류": df_tob_list[0][["new_date", "kdj_d", "kdj_j"]],
        "악세사리류": df_tob_list[1][["new_date", "kdj_d", "kdj_j"]],
        "제과점/아이스크림점": df_tob_list[2][["new_date", "kdj_d", "kdj_j"]],
        "커피/음료전문점": df_tob_list[3][["new_date", "kdj_d", "kdj_j"]],
        "패스트푸드점": df_tob_list[4][["new_date", "kdj_d", "kdj_j"]],
        "한식": df_tob_list[5][["new_date", "kdj_d", "kdj_j"]],
        "일식/생선회집": df_tob_list[6][["new_date", "kdj_d", "kdj_j"]],
        "중식": df_tob_list[7][["new_date", "kdj_d", "kdj_j"]],
        "양식": df_tob_list[8][["new_date", "kdj_d", "kdj_j"]],
        "주점": df_tob_list[9][["new_date", "kdj_d", "kdj_j"]],
        "편의점": df_tob_list[10][["new_date", "kdj_d", "kdj_j"]],
        "숙박": df_tob_list[11][["new_date", "kdj_d", "kdj_j"]],
        "헬스장": df_tob_list[12][["new_date", "kdj_d", "kdj_j"]],
        "미용원/피부미용원": df_tob_list[13][["new_date", "kdj_d", "kdj_j"]],
        "화장품점": df_tob_list[14][["new_date", "kdj_d", "kdj_j"]],
    }
    return Response(tob_dict)

def go_to_myhome(request):
    return redirect("https://i02d106.p.ssafy.io/")

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
            all_review
        )
        return queryset

    def create(self, request):
        # 리뷰를 작성하는 함수입니다.
        print('asdf')
        if request.user.is_authenticated:
            data = request.data
            store = Store.objects.get(id=data["store"])
            user = request.user
            review = models.Review.objects.create(store=store, user=user, content=data["content"], score=data["score"])
            store.review_count += 1
            store.save()
            user.review_count += 1
            user.save()
            return Response("작성 성공")
        else:
            return Response("작성 실패")
        # data = request.data
        # store = Store.objects.get(id=data["store"])
        # store_name = store.store_name
        # user = CustomUser.objects.get(id=data["user"])
        # # 받아온 데이터를 이용해서 Review를 작성합니다.
        # models.Review.objects.create(store_id=data["store"], user_id=data["user"], content=data["content"], score=data["score"], reg_time=datetime.datetime.now(), store_name=store_name)
        
        # 작성이 완료되었다면 매장과 유저의 review_count를 1씩 추가합니다.
        # store.review_count += 1
        # store.save()
        # user.review_count += 1
        # user.save()
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
        if request.user.is_authenticated:
            review = models.Review.objects.get(id=pk)
            user = review.user
            store = review.store
            if user.id == review.user_id:
                review.delete()
                user.review_count -= 1
                user.save()
                store.review_count -= 1
                store.save()
                return Response("삭제 성공")
        elif request.user.is_staff:
            review = models.Review.objects.get(id=pk)
            user = review.user
            store = review.store
            review.delete()
            user.review_count -= 1
            user.save()
            store.review_count -= 1
            store.save()
            return Response("삭제 성공")
        return Response("삭제 실패")


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

class StoreViewSet3(viewsets.GenericViewSet):
    serializer_class = serializers.StoreSerializer3

    @api_view(['GET'])
    def get_queryset(self):
        serializer = serializers.StoreSerializer3(models.Store.objects.filter(review_count__gte=1), many=True)
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
    serializer = serializers.ReviewSerializer2(all_review, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def reviews_info(self):
    serializer = serializers.ReviewSerializer3(all_review, many=True)
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
    df = pd.DataFrame(all_review.values("user", "store", "score"))
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
def user_based_cf(self):
    '''
    추천할 알고리즘을 확인하여 추천을 해 줍니다.
    현재 요청을 보낸 유저의 리뷰가 10개 이상인 경우
    서버에 적용중인 알고리즘(knn, svdpp)이 어떤것인지 확인 후 해당 알고리즘 기반 추천 결과를 제공

    10개 미만인 경우
    k-means 알고리즘을 적용하여 결과를 제공

    추천 아이템은 20개이며 프론트에서 임의의 아이템을 선정하게 합니다.
    '''
    # user = CustomUser.objects.get(id=15)
    user = CustomUser.objects.get(id=self.user.id)
    # user = CustomUser.objects.get(id=15)
    if user.review_count > 9:
        alg_name = Algorithm.objects.get(id=1).alg_name
        df = learning_dataframe[learning_dataframe["user"] != user.id]
        stores = df["store"]
        arr = []
        if alg_name == 'svdpp':
            alg = svdpp
        elif alg_name == 'knn':
            alg = knn
        
        for store in stores.unique():
            arr.append([store, alg.predict(uid=user.id, iid=store).est])
        arr.sort(key = lambda x: x[1], reverse=True)
        serializer = serializers.StoreDetailSerializer2([Store.objects.get(id=arr[i][0]) for i in range(min(20, len(arr)))], many=True)
    else:
        serializer = serializers.StoreDetailSerializer2(cluster_list[get_cluster(user.age, user.gender)], many=True)
    
    check_image(serializer)
    return Response(serializer.data)


@api_view(['GET'])
def recommend_by_store_id(self, store_id):
    '''
    '''
    store = Store.objects.get(id=store_id)
    store_df = pd.DataFrame(all_store.values("id", "longitude", "latitude", "category"))
    min_review = 5
    lon = store.longitude
    lat = store.latitude
    store_df = store_df[store_df["longitude"] - lon < 0.015]
    store_df = store_df[store_df["longitude"] - lon > -0.015]
    store_df = store_df[store_df["latitude"] - lat < 0.015]
    store_df = store_df[store_df["latitude"] - lat > -0.015]
    store_df = store_df[store_df.apply(lambda x: 6371*acos(cos(radians(lat))*cos(radians(x["latitude"]))*cos(radians(x["longitude"])-radians(lon))+sin(radians(lat))*sin(radians(x["latitude"]))), axis=1) < 1][["id", "category"]]
    
    a = []
    store_category_set = set(store.category.split('|'))
    for categories in store_df["category"]:
        cnt = 0
        for category in categories.split('|'):
            if category in store_category_set:
                cnt += 1
        a.append(cnt)
    store_df['count'] = a
    
    # 필요한 review들만 가져옴
    review_df = pd.DataFrame(all_review.values("user_id", "score", "store_id"))
    review_df = review_df[review_df['store_id'].isin(set(store_df['id']))]

    review_df = review_df.groupby('store_id').agg(['sum', 'count', 'mean'])['score']
    a = sum(review_df['sum'])/sum(review_df['count'])    
    
    review_df['calc'] = review_df.apply(lambda x: ((x['count']/(x['count']+min_review))*x['mean'] + (min_review/(x['count']+min_review))*a), axis=1)
    
    store_df = pd.merge(store_df[["id", "count"]], review_df["calc"], right_index=True, left_on="id", how='outer').set_index('id')

    store_df['calc'] = store_df['calc'].fillna(0.0)
    store_df.sort_values(by=['count', 'calc'], inplace=True, ascending=False)

    queryset = [Store.objects.get(id=i) for i in store_df.index[:20]]


    serializer = serializers.StoreDetailSerializer2(queryset, many=True)
    
    check_image(serializer)
    return Response(serializer.data)


@api_view(['POST'])
def create_store(self):
    print('asdfasdf')
    try:
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
    user = CustomUser.objects.get(id=self.user.id)
    user.category = category
    user.save()
    return Response("카테고리 등록 완료")


@api_view(['GET'])
def relearning_kmeans(self):
    global cluster_list, centroid
    user_df = pd.DataFrame(CustomUser.objects.filter(review_count__gte=10).values("id", "age", "gender"))
    male_value = 15
    female_value = 0
    min_review = 5

    # gender 값을 정수로 변환
    user_df['gender'] = user_df['gender'].apply(lambda x: male_value if x=="남" else female_value)

    # kmeans 학습
    kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=300, random_state=0)
    kmeans.fit(user_df[["age", "gender"]])

    # kmeans.labels_ : 몇번 클르서티인지 라벨링 붙이고 분리했었던 id col을 붙임
    user_df['cluster'] = kmeans.labels_

    # 모든 리뷰를 불러와 데이터프레임 생성
    review_df = pd.DataFrame(all_review.values("user_id", "score", "store_id"))

    # 가져온 유저가 있는 리뷰만 남김
    review_df = review_df[review_df['user_id'].isin(set(user_df['id']))]

    user_df = user_df.set_index('id')

    # 리뷰 테이블에 유저 클러스터정보를 조인해서 합쳐준다.
    temp_df = pd.merge(user_df["cluster"], review_df, left_index=True, right_on="user_id")
    temp_df["score"] = temp_df["score"].astype(float)

    # 클러스터의 인덱스에 클러스터 번호에 해당하는 정보만 가져와서 저장한다.
    cluster_list = [temp_df[["store_id", "score"]][temp_df["cluster"]==i] for i in range(5)]

    for i in range(5):
        # cluster 각각을 store로 묶는다
        cluster_list[i] = cluster_list[i].groupby('store_id').agg(['sum', 'count', 'mean'])['score']
        cluster_list[i] = cluster_list[i][cluster_list[i]['count']>=5]

        # 각 클러스터별 평균평점을 계산한다.
        a = sum(cluster_list[i]['sum']) / sum(cluster_list[i]['count'])

        # calc 칼럼을 추가하고 거기에 인기도 점수 계산한 값을 넣어준다.
        cluster_list[i]['calc'] = cluster_list[i].apply(lambda x: ((x['count']/(x['count']+min_review))*x['mean'] + (min_review/x['count']+min_review))*a, axis=1)

        # calc 기준으로 내림차순 정렬한다.
        cluster_list[i].sort_values(['calc'], ascending=False, inplace=True)
        cluster_list[i] = cluster_list[i].index
        cluster_list[i] = [Store.objects.get(id=cluster_list[i][j]) for j in range(min(20, len(cluster_list[i])))]

    # centroid -> 저쟁해야하는 값
    centroid = kmeans.cluster_centers_
    with open('k_means.p', 'wb') as f:
        pickle.dump(cluster_list, f)
        pickle.dump(centroid, f)
    return Response('k_means 재 학습 완료')