# Food Curation

이 서비스는 사용자 정보 기반 맛집 추천 서비스로 사용자에게 적절한 매장들을 추천해 주는 기능과 여러 정보를 바탕으로 각종 보고서를 제작하여 제공해 주는 기능을 가지고 있습니다.

맛집 추천 서비스의 경우 KNN과 SVDPP, K-means 알고리즘을 복합적으로 사용하여 추천해 줍니다.

보고서의 경우~~~



## 핵심 기능 및 기대 효과

- 각종 알고리즘과 머신러닝을 기반으로 사용자에게 사용자의, 사용자를 위한, 사용자에 의한 맛집 추천 사이트
- 나만의 맛집 추천을 받고 싶은 사람들에게 맞춤 정장과 같은 느낌의 맛집 추천 시스템
- 보고서~~~

## 주요 사용자

- 무분별한 맛집 추천에 지친 30대 차도남
- +@@

## 개발 환경

### 사용 언어

- Python 3.6.8
- nodeJS 13.5.0

### 주요 라이브러리

- npm 6.13.4
- Django 2.2.7
- djangorestframework 3.10.3
- axios 0.19.0
- vue 2.6.10
- vuex 3.1.1
- pandas 0.25.3

그 외 기타 라이브러리는 backend/requirements.txt, frontend/package.json 참조

## How to Run

이 프로젝트는 pm2를 사용하여 서버를 관리하고 nginx를 사용하여 ssl 적용 및 프록시 제어를 하고 있습니다.

nginx의 경우 아래와 같은 설정으로 80포트로 들어오면 8080포트로 넘겨주게 설정되어 있으며

```
server {
        listen 80;
        server_name i02d106.p.ssafy.io;
        location / {
                proxy_pass http://127.0.0.1:8080;
        }
}
```

인증서는 아래의 경로에 보관되어 잇습니다.

```
/etd/nginx/ssl/server.crt
/etd/nginx/ssl/server.csr
/etd/nginx/ssl/server.key
```

pm2에서는 frontend와 backend의 스크립트파일을 통해 frontend서버와 backend서버를 구동할 수 있습니다.

```
pm2 start frontend/dps.json
pm2 start backend/dps.json
```

## data schema

![](images/ERD.png)

## 명세

### req1 데이터 DB 마이그레이션

1. DB 모델 설계

   [data schema](#data schema) 참조

2. Pandas DataFrame DB 마이그레이션

   데이터를 DB에 넣으려면 아래와 같이 실행하면 된다.

   ```bash
   cd backend
   python manage.py initialize
   ## 우분투 환경에선 python 대신 python3을 입력하면 된다.
   ```


### req2 웹 서비스 검색 기능 확장

1. 검색 기능 확장

   근처에 존재하는 매장들의 메뉴나 매장명을 검색하는 기능입니다.

2. 유저 정보 기능 구현

   유저의 상세 정보를 프론트에 제공해주기 위해 로그인 성공 시 유저 정보를 응답해줍니다.

   - 추가사항: 회원탈퇴, 비밀번호 변경, 비밀번호 재설정 기능(REST API 참고)

4. 음식점 정보 기능 구현

   매장명에 해당하는 매장을 반환합니다.

4. 음식점 사진 자료 크롤링

   서비스를 진행하는동안 자동으로 이미지가 등록되지 않은 매장을 조회 시 크롤링 할 매장 아이디와 우선순위를 저장한 딕셔너리를 갱신합니다.

   크롤링 해야 할 매장의 갯수가 일정 수준 이상이 되면 자동으로 크롤링을 시작하고 크롤링 할 목록이나 크롤링 시작을 요청할 수 있는 API가 있습니다.

   크롤링 할 딕셔너리 조회 API: https://i02d106.p.ssafy.io:8765/api/crawling_check

   크롤링 시작 요청 API: https://i02d106.p.ssafy.io:8765/api/crawling_start

5. 구글에 매장명, 주소를 검색하여 받아온 결과에서 썸네일 이미지 url을 가져와 db에 저장합니다.


### req3 웹 서비스 인증 기능 구현

1. 회원가입 기능 구현

   라이브러리에서 제공하는 회원가입 기능을 커스터마이징하여 추가적인 정보를 받도록 하였습니다.

   - 추가사항: 이메일 인증(REST API 참고) 

2. 로그인, 로그아웃 기능 구현

   django-rest-auth, rest_framework_jwt라이브러리를 사용하였고, 로그인 했을 경우, JWT 토큰을 프론트에 넘겨줍니다.

   ```python
       path('login/', views.CustomLoginView.as_view(), name='login'),
   ```

   JWT토큰을 사용하였기 때문에 백엔드에서는 로그아웃에 대한 처리를 따로 하지않았습니다.

   - 추가사항: 회원탈퇴 기능
     - 완전히 유저를 삭제하지 않고 is_active 값을 조정해줌으로써 관련 댓글과 리뷰 정보는 남겨두도록 하였습니다.
     - views.UserViewSet

   ```python
    @api_view(['POST'])
       def user_delete(self):
           if self.user.is_authenticated == False:
               return Response("삭제 실패")
           else:
               user = get_object_or_404(CustomUser, username=self.user)
               user.is_active = False
               user.save()
               return Response("삭제 성공")
   ```



### req4 웹 서비스 리뷰 기능 구현

1. 리뷰 기능 구현

   리뷰 작성 요청이 들어오면 권한이 있는지 확인 후 권한이 있으면 리뷰를 작성합니다.
   
   리뷰가 작성이 되면 store와 user의 review_count를 각 각 1씩 더해 줍니다.
   
   리뷰 삭제 요청이 들어오면 권한이 있는지 확인 후 권한이 있으면 리뷰를 삭제합니다.
   
   리뷰가 삭제되면 store와 user의 review_count를 각 각 1씩 빼줍니다.

### req5 KNN 알고리즘 구현

데이터 가공 -> 알고리즘 학습 -> user_based로 id에 대한 정보 선별 -> TOP10 식당 추천

1. 데이터 가공

   리뷰가 10개 이상인 음식점의 리뷰와 리뷰가 10개 이상인 유저 두 집합에 포함되는 리뷰의 user_id, store_id, score를 가져옵니다.

2. KNN 알고리즘 학습 및 구현

   위에 전처리 한 리뷰 데이터를 기반으로 평점을 매기지 않은 음식점들 중 추정 score 값이 가장 높은 매장 상위 20개를 반환합니다.

### req6 Matrix Factorization 알고리즘 구현

1. 데이터 가공

   KNN 알고리즘 구현의 데이터 가공과 동일
   
2. SVDPP 알고리즘 학습 및 구현

   이전에 전처리한 리뷰 데이터를 기반으로 평점을 매기지 않은 음식점들 중 추정 score 값이 가장 높은 매장 상위 20개를 반환합니다.

## REST API

### algorithm_change

경로: api/algorithm_change

메소드: PUT

| 인자           | 필수 여부                  |
| -------------- | -------------------------- |
| algorithm_list | True(0: "svdpp", 1: "knn") |

현재 서버에서 사용될 추천 알고리즘을 전송받은 데이터에 해당하는 알고리즘으로 변경합니다.

### algorithm_check

경로: api/algorithm_check

메소드: GET

현재 서버에서 어떤 추천 알고리즘이 적용되어 있는지 확인하는 API입니다.

### crawling_check

경로: api/crawling_check

메소드: GET

지금 크롤링 해야 할 매장을 저장한 딕셔너리를 조회합니다.

### crawling_start

경로: api/crawling_start

메소드: GET

크롤링 해야 할 매장이 저장된 딕셔너리를 조회하여 크로링을 시작하는 명령을 내립니다.

### create_store

경로: api/create_store

메소드: POST





### get_store_reviews_by_store_id

경로: api/get_store_reviews_by_store_id/{store_id} 

메소드: GET

|   인자   | 필수 여부 |
| :------: | :-------: |
| store_id |   True    |



반환값

```json
[
  {
    "id": INT,
    "store": INT(store_id),
    "store_name": String(store_name),
    "user": INT(user_id),
    "score": INT(score),
    "content": String(content),
    "reg_time": Datetime(reg_time),
    "category_list": [
      String(category),
    ]
  }
]
```

### like_store

user_id와 store_id를 인자로 받아 해당하는 좋아요 객체가 있으면 그 객체를 지우고 없으면 객체를 생성합니다.

경로: api/like_store

메소드: POST

|     인자      | 필수 여부 |
| :-----------: | :-------: |
| store_id: INT |   True    |
| user_id: INT  |   True    |

반환값

좋아요 객체 생성 시

```json
"좋아요"
```

좋아요 객체 삭제 시

```json
"좋아요 취소"
```

### reviews

모든 리뷰의  store, user, score를 가져와 반환합니다.

경로: api/reviews

메소드: GET

반환값

```json
[
    {
        "store": INT(store_id),
        "user": INT(user_id),
        "score": INT(score)
    }
]
```

### search_store

위치 정보와 검색어를 받아와서 인근 매장 중 검색어가 포함된 매장을 반환합니다.

경로: api/search_store

메소드: POST

|       인자       | 필수 여부 |
| :--------------: | :-------: |
| latitude: Float  |   True    |
| longitude: Float |   True    |
|  words: String   |   False   |

반환값

```json
[
    {
        "id": INT(pk),
        "store_name": String(store_name),
        "branch": String(branch),
        "area": String(area),
        "tel": String(phone_number),
        "address": String(address),
        "latitude": Float(latitude),
        "longitude": Float(longitude),
        "category_list": [
            String(category)
        ],
        "review_count": INT(review_count),
        "menues": [          
            {
                "id": INT(menu_id),
                "store": INT(store_id),
                "menu_name": String(menu_name),
                "price": INT(price)
            },
        ]
	}
]
```

### store

입력받은 리뷰갯수 이상인 매장들의 id, review_count를 받아 옵니다.

경로: api/store/{review_count}

메소드: GET

|       인자        | 필수 여부 |
| :---------------: | :-------: |
| review_count: INT |   True    |

반환값

```json
[
    {
        "id": INT(store_id),
        "review_count": INT(review_count)
    }
]
```

### store_reviews

경로: api/store_reviews

메소드: GET

|      인자      | 필수 여부 |
| :------------: | :-------: |
|   page: INT    |   False   |
| page_size: INT |   False   |

반환값

```json
{
    "count": INT(number of stores),
    "next": String(url of next page),
    "previous": String(url of next page),
    "results": [
        {
            "id": INT(review_id),
            "store": INT(store_id),
            "store_name": String(store_name),
            "user": INT(user_id),
            "branch": String(branch),
            "area": String(area),
            "tel": String(phone_number),
            "address": String(address),
            "latitude": Float(latitude),
            "longitude": Float(longitude),
            "category_list": [
                String(category)
            ],
            "id": 1,
            "store": 15,
            "store_name": "써리힐",
            "user": 68632,
            "score": 5,
            "content": "전포 윗길에 새로 생긴! 호주에서 온 쉐프가 직접 요리하는 호주식 레스토랑!",
            "reg_time": "1970-01-01T00:00:00+09:00",
            "category_list": [
                "호주레스토랑"
            ]
        }
    ]
}
```

메소드: POST

인자를 입력하면 리뷰를 작성합니다.

|         인자         | 필수 여부 |
| :------------------: | :-------: |
| store: INT(store_id) |   True    |
|  user: INT(user_id)  |   True    |
|      score: INT      |   True    |
|   content: String    |   True    |

반환값

```json
"작성 성공"
```

메소드: PUT

인자를 입력하면 리뷰를 수정합니다.

|        인자        | 필수 여부 |
| :----------------: | :-------: |
| id: INT(review_id) |   True    |
|     score: INT     |   True    |
|  content: String   |   True    |

반환값

```json
"수정 성공"
```

메소드: DELETE

인자를 입력하면 리뷰를 삭제합니다.

|        인자        | 필수 여부 |
| :----------------: | :-------: |
| id: INT(review_id) |   True    |

반환값

```json
"삭제 성공"
```

### stores

경로: api/stores

메소드: GET

|      인자      | 필수 여부 |
| :------------: | :-------: |
|   page: INT    |   False   |
| page_size: INT |   False   |

반환값

```json
{
    "count": INT(number of stores),
    "next": String(url of next page),
    "previous": String(url of next page),
    "results": [
        {
            "id": INT(store_id),
            "store_name": String(store_name),
            "branch": String,
            "area": String,
            "tel": String(phone_number),
            "address": String(address),
            "latitude": Float(latitude),
            "longitude": Float(longitude),
            "category_list": [
                String(category)
            ],
            "review_count": INT,
        }
    ]
}
```

### user_reviews

경로: api/user_reviews

메소드: GET

|      인자      | 필수 여부 |
| :------------: | :-------: |
|   page: INT    |   False   |
| page_size: INT |   False   |

반환값

```json
{
    "count": INT(number of users),
    "next": String(url of next page),
    "previous": String(url of next page),
    "results": [
        {
            "id": INT(review_id),
            "store": INT(store_id),
            "store_name": String(store_name),
            "user": INT(user_id),
            "score": INT(user_id),
            "content": String,
            "reg_time": Datetime,
            "category_list": [
                String(category)
            ],
        }
    ]
}
```

### algorithm_change

현재 서버에서 협업필터링 기반 추천 시스템에 적용할 알고리즘을 선택하는 부분입니다.

0번의 경우 svdpp, 1번의 경우 knn알고리즘을 적용하여 맛집을 추천해 줍니다.

경로: api/algorithm_change

메소드: PUT

|      인자      | 필수 여부 |
| :------------: | :-------: |
| algorithm: INT |   True    |

반환값: 지금부터 적용될 알고리즘 이름 String

### algorithm_check

현재 서버에서 협업필터링 기반 추천 시스템에 적용되어 있는 알고리즘을 확인하는 api입니다.

경로: api/algorithm_check

메소드: GET

반환값: 현재 적용중인 알고리즘 이름 String

### update_learning_dataframe

현재 서버에서 협업필터링 기반 추천 시스템을 학습시키기 위한 데이터프레임을 갱신하는 api입니다.

경로: api/update_learning_dataframe

메소드: GET

반환값: "갱신 완료"

### relearning_current_model

현재 서버에서 적용된 협업필터링 기반 추천 알고리즘을 재학습시키는 