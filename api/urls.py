from django.urls import path
from .views import CategoryList, DishListCreateView, CartView, OrderView, UserBalanceView

urlpatterns = [
    path('dishes/', DishListCreateView.as_view(), name='dishes'),
    path('dishes/<int:pk>/', DishListCreateView.as_view(), name='dish-update'),
    path('cart/', CartView.as_view(), name='cart'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('balance/', UserBalanceView.as_view(), name='balance'),
    path('categories/', CategoryList.as_view(), name='category-list'),
]
