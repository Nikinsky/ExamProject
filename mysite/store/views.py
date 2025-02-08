from django.urls import reverse
from rest_framework import viewsets, generics, status
from .serializers import *
from rest_framework import permissions

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination

from .filters import *

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import reverse
from django.http import HttpResponseRedirect




class PaginationAll(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 30


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Создаем пользователя
            user = UserProfile.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )

            # Генерируем токены
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': access_token
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = UserProfile.objects.get(email=email)
                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)

                    return Response({
                        'status': 'success',
                        'tokens': {
                            'refresh': str(refresh),
                            'access': access_token
                        },
                        'user': {
                            'id': user.id,
                            'email': user.email,
                            'username': user.username
                        }
                    }, status=status.HTTP_200_OK)

            except UserProfile.DoesNotExist:
                pass

        return Response(
            {'detail': 'Неверный email или пароль'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            # Получаем refresh token из cookie
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

                response = Response(status=status.HTTP_205_RESET_CONTENT)
                response.delete_cookie('access_token')
                response.delete_cookie('refresh_token')
                return response

        except Exception as e:
            return Response(
                {'detail': 'Ошибка при выходе'},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserProfileView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer



class CarView(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = PaginationAll
    search_fields = ['description']
    ordering_fields = ['price']
    filterset_class = CarFilter


class BidView(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    filter_backends = [DjangoFilterBackend]

    serializer_class = BidsSerializer
    pagination_class = PaginationAll


class FeedbackView(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()

    serializer_class = FeedbackSerializer
    pagination_class = PaginationAll





