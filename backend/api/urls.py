from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from api import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

schema_view = get_schema_view(
    openapi.Info(
        #필수인자
        title="Restaurant API",
        default_version="v1",
        #선택인자
        description="식당관련 API 서비스입니다.",
        # terms_of_service='https://www.google.com/policies/terms/', # 약관 예시
        contact=openapi.Contact(email="pyeonggangkim@gmail.com"),
        license=openapi.License(name="SSAFY License"), 
    )
)



router = DefaultRouter(trailing_slash=False)
router.register(r"stores", views.StoreViewSet, basename="stores")
# router.register(r"reviews/<int:user_id>", views.UserReviewSet, basename="user-review")
router.register(r"stores_detail", views.StoreDetailViewSet, basename="stores-detail")
# router.register(r"user", views.UserViewSet, basename="user")
router.register(r"user_reviews", views.UserReviewSet, basename="user-review")


router.register(r"store_reviews", views.StoreReviewSet, basename="store-review")
router.register(r"like_store", views.like_store, basename="like-store")
# router.register(r"reviews", views.ReveiwViewSet, basename="reviews")
urlpatterns = [
    # path('stores/', views.stores, name='stores'),
    path('swagger/', schema_view.with_ui('swagger'), name='api_swagger'),
    path('user', views.UserViewSet.get_queryset, name='user'),
    path('store/<int:review_count>', views.StoreViewSet2.get_queryset, name='store'),
    path('all_stores/', views.StoreViewSet3.get_queryset, name='all_stores'),
    path('user_delete/', views.UserViewSet.user_delete, name='user_delete'),
    # path('user_reviews/<int:user_id>', views.UserReviewSet.get_queryset, name='user-review'),
    path('get_store_reviews_by_store_id/<int:store_id>', views.store_reviews, name='get-store-review'),
    # path('like_store/<int:user_id>/<int:store_id>', views.like_store.get_queryset, name='like_store'),
    *router.urls,
    path('reviews', views.review_list, name="reviews"),
    path('reviews_info', views.reviews_info, name="reviews_info"),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('search_store', views.search_store, name="search_store"),
    path('go_to_myhome/', views.go_to_myhome, name="go_to_myhome"),
    path('algorithm_check/', views.algorithm_check, name="algorithm_check"),
    path('algorithm_change/', views.algorithm_change, name="algorithm_change"),
    path('update_learning_dataframe', views.update_learning_dataframe, name="update_learning_dataframe"),
    path('relearning_current_model', views.relearning_current_model, name="relearning_current_model"),
    path('relearning_kmeans', views.relearning_kmeans, name="relearning_kmeans"),
    path('user_based_cf', views.user_based_cf, name="user_based_cf"),
    path('trend_by_tob', views.trend_by_tob, name="trend_by_tob"),
    path('compare_with_chain', views.compare_with_chain, name="compare_with_chain"),
    path('district_by_age_time', views.district_by_age_time, name="district_by_age_time"),
    path('token/', obtain_jwt_token),
    path('token/verify/', verify_jwt_token),
    path('token/refresh/', refresh_jwt_token),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('reset-password', PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('accounts/', include('allauth.urls')),
    path('crawling_check', views.crawling_check, name="crawling_check"),
    path('crawling_start', views.crawling_start, name="crawling_start"),
    path('create_store', views.create_store, name="create_store"),
    path('set_user_category', views.set_user_category, name="set_user_category"),
    path('recommend_by_store_id/<int:store_id>', views.recommend_by_store_id, name="recommend_by_store_id"),
]