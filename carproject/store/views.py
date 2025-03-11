from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import viewsets, generics, status
from .models import (
    UserProfile, Client, Owner, CarMake, CarModel, Category, Car,
    CarReview, Cart, CartItem, Favorite, FavoriteItem, History
)
from .serializers import (
    UserProfileSerializer, ClientSerializer, OwnerSerializer, CarMakeListSerializer, CarMakeDetailSerializer,
    CarModelListSerializer, CarModelDetailSerializer, CategoryListSerializer, CategoryDetailSerializer, CarSerializer, CarListSerializer, CarDetailSerializer,
    CarReviewSerializer, CarReviewCreateSerializer, OwnerRegisterSerializer, ClientRegisterSerializer, LoginSerializer,
    CartSerializer, CartItemSerializer, FavoriteSerializer, FavoriteItemSerializer, HistorySerializer,
)
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .permission import *

class OwnerRegisterView(generics.CreateAPIView):
    serializer_class = OwnerRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ClientRegisterView(generics.CreateAPIView):
    serializer_class = ClientRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class CarMakeLisAPIView(generics.ListAPIView):
    queryset = CarMake.objects.all()
    serializer_class = CarMakeListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['category_name']


class CarMakeDetailAPIView(generics.RetrieveAPIView):
    queryset = CarMake.objects.all()
    serializer_class = CarMakeDetailSerializer


class CarModelListAPIView(generics.ListAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['category_name']

class CarModelDetailAPIView(generics.RetrieveAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelDetailSerializer



class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['category_name']

class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class CarCreateAPIView(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CarListAPIView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CarFilter
    search_fields = ['car_model', 'car_make']
    ordering_fields = ['price']


class CarDetailAPIView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CarReviewCreateAPIView(generics.ListCreateAPIView):
    queryset = CarReview.objects.all()
    serializer_class = CarReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated, CheckUserReview]

class CarReviewEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarReview.objects.all()
    serializer_class = CarReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


class CartListAPIView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


    def retrieve(self, request, *args, **kwargs ):
        cart, created = Cart.objects.get_or_create(user=request.user)

class CartItemDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class FavoriteListAPIView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

class FavoriteItemDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer

class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
