from .models import Store, Review, Menu, CustomUser, UserLikeStore, StoreImage
from rest_framework import serializers
from django.db.models import Avg
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from rest_auth.registration.serializers import RegisterSerializer


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "id",
            "store",
            "menu_name",
            "price",
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreImage
        fields = [
            "url",
        ]


class CustomRegisterSerializer(RegisterSerializer):
    age = serializers.IntegerField(required=False)
    gender = serializers.CharField(max_length=2, required=False)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['age'] = self.validated_data.get('age', '')
        data_dict['gender'] = self.validated_data.get('gender', '')
        return data_dict

class StoreSerializer(serializers.ModelSerializer):
    menues = MenuSerializer(source="menu_set", many=True)
    images = ImageSerializer(source="storeimage_set", many=True)
    class Meta:
        model = Store
        fields = [
            "id",
            "store_name",
            "branch",
            "area",
            "tel",
            "address",
            "latitude",
            "longitude",
            "category_list",
            "review_count",
            "menues",
            "images",
            "tag",
        ]

class StoreSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "id",
            "review_count",
        ]

class StoreSerializer3(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "id",
            "store_name",
        ]

class ReviewSerializer(serializers.ModelSerializer):
    category_list = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = [
            "id",
            "store",
            "store_name",
            "user_id",
            "username",
            "score",
            "content",
            "reg_time",
            "category_list",
        ]
    def get_username(self, obj):
        return obj.user.username
    def get_category_list(self, obj):
        return Store.objects.get(id=obj.store_id).category_list

class ReviewSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "store",
            "user",
            "score",
        ]

class ReviewSerializer3(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "store",
            "reg_time",
            "score",
        ]

class StoreDetailSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField()
    avg_score = serializers.SerializerMethodField()
    reviews = ReviewSerializer(source="review_set", many=True)
    menues = MenuSerializer(source="menu_set", many=True)
    images = ImageSerializer(source="storeimage_set", many=True)
    class Meta:
        model = Store
        fields = [
            "id",
            "store_name",
            "branch",
            "area",
            "tel",
            "address",
            "latitude",
            "longitude",
            "category_list",
            "review_count",
            "reviews",
            "avg_score",
            "menues",
            "images",
        ]

    def get_review_count(self, obj):
        return obj.review_set.count()

    def get_avg_score(self, obj):
        if obj.review_set.count():
            return obj.review_set.aggregate(Avg('score'))["score__avg"]
        return 0


class StoreDetailSerializer2(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField()
    avg_score = serializers.SerializerMethodField()
    images = ImageSerializer(source="storeimage_set", many=True)
    class Meta:
        model = Store
        fields = [
            "id",
            "store_name",
            "area",
            "review_count",
            "avg_score",
            "images",
        ]

    def get_review_count(self, obj):
        return obj.review_set.count()

    def get_avg_score(self, obj):
        if obj.review_set.count():
            return obj.review_set.aggregate(Avg('score'))["score__avg"]
        return 0


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "age",
            "gender",
            "review_count",
        ]


class LikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLikeStore
        fields = [
            "customuser_id",
            "store_id",
        ]
