from django.urls import path
from . import views
from .views import register_view

urlpatterns = [
    path('', views.home_view, name='home'), 
    path('dish/<int:dish_id>/', views.dish_detail_view, name='dish_detail'),
    path('register/', register_view, name='register-form'),
    path('login-form/', views.login_view, name='login-form'),
]