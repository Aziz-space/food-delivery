# api/auth/urls.py
from django.urls import path
from .views import LoginAPIView, RegisterAPIView, UserUpdateView, LogoutAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('update/<int:user_id>/', UserUpdateView.as_view(), name='update_user'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
