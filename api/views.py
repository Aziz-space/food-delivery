from rest_framework import status,generics
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Category, Dish, Order, Cart, OrderItem, UserBalance
from .serializers import CategorySerializer, DishSerializer, OrderSerializer, CartSerializer, UserBalanceSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from api.auth.permissions import IsAdmin, IsSeller, IsCustomer


class DishListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAuthenticated(), IsSeller()]

    def get(self, request):
        dishes = Dish.objects.all()
        
        name = request.query_params.get('name', None)
        if name:
            dishes = dishes.filter(name__icontains=name) 

        category = request.query_params.get('category', None)
        if category:
            dishes = dishes.filter(category__name__icontains=category)  
        
        
        serializer = DishSerializer(dishes, many=True)
        return Response(serializer.data)


    
    def post(self, request):
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        try:
            dish = Dish.objects.get(pk=pk, seller=request.user) 
        except Dish.DoesNotExist:
            return Response({"detail": "Блюдо не найдено или у вас нет прав для его обновления."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DishSerializer(dish, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        try:
            dish = Dish.objects.get(pk=pk, seller=request.user)  
        except Dish.DoesNotExist:
            return Response({"detail": "Блюдо не найдено или у вас нет прав для его удаления."}, status=status.HTTP_404_NOT_FOUND)

        dish.delete()
        return Response({"detail": "Блюдо успешно удалено."}, status=status.HTTP_204_NO_CONTENT)

class CartView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        cart_items = Cart.objects.filter(customer=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request, order_id=None):
        if order_id:
            order = get_object_or_404(Order, id=order_id, customer=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            orders = Order.objects.filter(customer=request.user)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            balance = UserBalance.objects.get(user=request.user)
            total_price = serializer.validated_data['total_price']
            if balance.balance >= total_price:
                serializer.save(customer=request.user)
                balance.balance -= total_price
                balance.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error': 'Недостаточно средств'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            if 'status' in serializer.validated_data:
                if serializer.validated_data['status'] in dict(Order.STATUS_CHOICES):
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response({'error': 'Некорректный статус'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class CategoryList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)



from decimal import Decimal

class UserBalanceView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        balance = get_object_or_404(UserBalance, user=request.user)
        serializer = UserBalanceSerializer(balance)
        return Response(serializer.data)

    def post(self, request):
        if 'amount' in request.data:
            amount = request.data.get('amount', 0)

            if amount <= 0:
                return Response({"detail": "Сумма пополнения должна быть больше нуля."}, status=status.HTTP_400_BAD_REQUEST)

            user_balance = get_object_or_404(UserBalance, user=request.user)
            user_balance.balance += Decimal(amount)  # Преобразуем amount в Decimal
            user_balance.save()

            return Response({"balance": str(user_balance.balance)}, status=status.HTTP_200_OK)

        else:
            dish_id = request.data.get('dish_id')
            quantity = request.data.get('quantity', 1)
            dish = get_object_or_404(Dish, id=dish_id)

            user_balance = get_object_or_404(UserBalance, user=request.user)

            total_price = dish.price * quantity

            if user_balance.balance < total_price:
                return Response({"detail": "Недостаточно средств на балансе."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                with transaction.atomic():
                    order = Order.objects.create(
                        customer=request.user,
                        total_price=total_price,
                        status='pending'
                    )

                    order_item = OrderItem.objects.create(
                        order=order,
                        dish=dish,
                        quantity=quantity,
                        price=dish.price
                    )

                    user_balance.balance -= total_price
                    user_balance.save()

                    order_serializer = OrderSerializer(order)
                    return Response(order_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"detail": f"Ошибка: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)