from rest_framework import serializers
from .models import (
    UserProfile, Client, Owner, CarMake, CarModel, Category, Car,
    CarImage, Cart, CartItem, Favorite, FavoriteItem, History, CarReview
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class OwnerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'owner_name', 'location', 'phone_number', 'role',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Owner.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class ClientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'role',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Client.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class CarMakeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = ['id', 'car_name']


class CarModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'car_model']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    category_make = CarMakeListSerializer(many=True, read_only=True)
    category_model = CarModelListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'category_make', 'category_model']


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image']


class CarReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = CarReview
        fields = ['id', 'user', 'text', 'stars']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class CarListSerializer(serializers.ModelSerializer):
    car_images = CarImageSerializer(many=True, read_only=True)
    car_make = CarMakeListSerializer()
    car_model = CarModelListSerializer()

    class Meta:
        model = Car
        fields = ['id', 'car_make', 'car_model', 'car_images', 'year', 'price']

class CarDetailSerializer(serializers.ModelSerializer):
    car_images = CarImageSerializer(many=True, read_only=True)
    car_make = CarMakeListSerializer()
    car_model = CarModelListSerializer()
    car_review = CarReviewSerializer(many=True, read_only=True)
    count_people = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['car_make', 'car_model', 'car_images' , 'year', 'price', 'description', 'body',
                  'fuel', 'rudder', 'gearbox', 'color', 'car_review', 'avg_rating', 'count_people', 'date_registered']

    def get_count_people(self, obj):
        return obj.get_count_people()

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

class CarModelDetailSerializer(serializers.ModelSerializer):
    model = CarListSerializer(many=True, read_only=True)

    class Meta:
        model = CarModel
        fields = ['car_model', 'model']


class CarMakeDetailSerializer(serializers.ModelSerializer):
    makes = CarListSerializer(many=True, read_only=True)
    car_makes = CarModelListSerializer(many=True, read_only=True)
    class Meta:
        model = CarMake
        fields = ['car_name', 'makes', 'car_makes']


class CarReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarReview
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    car = CarListSerializer(read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), write_only=True, source='car')

    class Meta:
        model = CartItem
        fields = ['id', 'car', 'car_id']


class CartSerializer(serializers.ModelSerializer):
    cart_item = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'client', 'cart_item', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'