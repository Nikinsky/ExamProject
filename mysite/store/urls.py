
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'user', UserProfileView, basename='user-list')

router.register(r'cars', CarView, basename='car-list')

router.register(r'bid', BidView, basename='bid-list')

router.register(r'feedback', FeedbackView, basename='feedback-list')


urlpatterns = [
    path('', include(router.urls)),
    path('register', RegisterView.as_view(), name='register-list'),
    path('login', CustomLoginView.as_view(), name='login-list'),
    path('logout', LogoutView.as_view(), name='logout-list'),
]