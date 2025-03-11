from django.urls import path, include

from .serializers import CarReviewCreateSerializer
from .views import (
    UserProfileViewSet, ClientViewSet, OwnerViewSet, CarMakeLisAPIView, CarMakeDetailAPIView,
    CarModelListAPIView, CarModelDetailAPIView, CategoryListAPIView, CategoryDetailAPIView, CarCreateAPIView, CarListAPIView, CarDetailAPIView,
    CarReviewCreateAPIView, CarReviewEditAPIView, CartListAPIView, CartItemDetailAPIView, FavoriteListAPIView, FavoriteItemDetailAPIView, HistoryViewSet,
    OwnerRegisterView, ClientRegisterView, LoginView, LogoutView,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='user_list')
router.register(r'clients', ClientViewSet, basename='client_list')
router.register(r'owners', OwnerViewSet, basename='owner_list')
router.register(r'history', HistoryViewSet, basename='history_list')



urlpatterns = [
    path('', include(router.urls)),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),

    path('car_make/', CarMakeLisAPIView.as_view(), name='car_make_list'),
    path('car_make/<int:pk>/', CarMakeDetailAPIView.as_view(), name='car_make_detail'),

    path('car_model/', CarModelListAPIView.as_view(), name='car_model_list'),
    path('car_model/<int:pk>/', CarModelDetailAPIView.as_view(), name='car_model_detail'),

    path('car_create/', CarCreateAPIView.as_view(), name='car_create'),
    path('car/', CarListAPIView.as_view(), name='car_list'),
    path('car/<int:pk>/', CarDetailAPIView.as_view(), name='car_detail'),

    path('review/', CarReviewCreateAPIView.as_view(), name='review_list'),
    path('review/<int:pk>/', CarReviewEditAPIView.as_view(), name='review_edit'),

    path('cart/', CartListAPIView.as_view(), name='cart_list'),
    path('cart_item/', CartItemDetailAPIView.as_view(), name='cart_item_detail'),

    path('favorite/', FavoriteListAPIView.as_view(), name='favorite_list'),
    path('favorite_item/', FavoriteItemDetailAPIView.as_view(), name='favorite_item_detail'),

    path('owner_register/', OwnerRegisterView.as_view(), name='owner_register'),
    path('client_register/', ClientRegisterView.as_view(), name='client_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')

]