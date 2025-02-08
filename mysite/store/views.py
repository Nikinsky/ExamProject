from django.urls import reverse
from rest_framework import viewsets, generics, status
from .serializers import *
from rest_framework import permissions

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination

from .filters import *

from



class PaginationAll(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 30


from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect





class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        return Response({
            'user': {
                'email': user.email,
                'username': user.username,
                'token': str(token.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.valdated_data
        refresh = RefreshToken.for_user(user)
        response = HttpResponseRedirect(reverse('user_list'))
        response.set_cookie('token', str(refresh.access_token))
        response.set_cookie('token', str(refresh.access_token))
        return response


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)




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
    filter_backends = [DjangoFilterBackend]

    serializer_class = FeedbackSerializer
    pagination_class = PaginationAll





