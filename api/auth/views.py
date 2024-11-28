from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied  # Импортируем PermissionDenied
from .serializers import LoginSerializer, ProfileSerializer, RegisterSerializer, UserSerializer
from .permissions import IsAdmin, IsSeller, IsCustomer  # Подключаем разрешения
from rest_framework.permissions import AllowAny

User = get_user_model()

# Вход в систему
class LoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Сначала проверяем, существует ли пользователь
        if not User.objects.filter(email=email).exists():
            return Response(
                {'detail': 'Пользователь с таким email не существует'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Если пользователь существует, проверяем пароль
        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'role': user.role
            })
        else:
            return Response(
                {'detail': 'Неверный пароль'},
                status=status.HTTP_401_UNAUTHORIZED
            )


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator    


@method_decorator(csrf_exempt, name='dispatch')
class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # Добавьте эту строку

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {'detail': 'Пользователь успешно зарегистрирован', 'token': token.key},
            status=status.HTTP_201_CREATED
        )


# Обновление данных пользователя
class UserUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] 
    
    def get_object(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        
        # Проверяем, что пользователь может редактировать только свой профиль
        if user.id != self.request.user.id:
            raise PermissionDenied("Вы не можете редактировать чужой профиль")
        
        return user
    
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)



class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()  # Удаляем токен
        return Response({"detail": "Вы успешно вышли из системы."}, status=status.HTTP_200_OK)
