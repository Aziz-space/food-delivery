import calendar as cal
from datetime import date, datetime
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
import requests
from api.auth.serializers import RegisterSerializer
from api.serializers import DishSerializer
from main.models import Category, Dish
from django.contrib.auth import authenticate, login

# Функция для главной страницы
def home_view(request):
    categories = Category.objects.all()  
    return render(request, 'main/main.html', {'categories': categories}) 

def category_view(request):
    categories = Category.objects.all()  
    return render(request, 'main/components/nav.html', {'categories': categories}) 



def home_view(request):
    category_id = request.GET.get('category')  # Получаем ID категории из GET-запроса
    if category_id:
        dishes = Dish.objects.filter(categories__id=category_id)  # Фильтруем по категории
        selected_category = get_object_or_404(Category, id=category_id)
    else:
        dishes = Dish.objects.all()  # Если категория не выбрана, показываем все блюда
        selected_category = None

    categories = Category.objects.all()  # Для отображения списка категорий
    return render(request, 'main/main.html', {
        'dishes': dishes,
        'categories': categories,
        'selected_category': selected_category,  # Выбранная категория, если есть
})
    
    
    
def dish_detail_view(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    categories = dish.categories.all()  
    return render(request, 'main/product-page.html', {
        'dish': dish,
        'categories': categories,  
})
    
    
def register_view(request):
    template_name = 'main/register.html'
    
    if request.method == 'GET':
        current_year = datetime.now().year
        years = range(current_year - 100, current_year - 17)
        month_names = list(cal.month_name)[1:]
        return render(request, template_name, {'years': years, 'month_names': month_names})
    
    if request.method == 'POST':
        year = request.POST.get('year')
        month = request.POST.get('month')
        day = request.POST.get('day')
        
        try:
            birth_date = date(int(year), int(month), int(day))
        except ValueError:
            messages.error(request, 'Неверная дата рождения.')
            return redirect('register')
        
        data = {
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'password2': request.POST.get('password2'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'birth_date': birth_date,
            'gender': request.POST.get('gender'),
            'role': request.POST.get('role')
        }
        
        # Сериализация данных
        serializer = RegisterSerializer(data=data)
        
        if serializer.is_valid():
            try:
                serializer.save()  # Сохранение пользователя
                messages.success(request, 'Регистрация прошла успешно!')
                return redirect('login-form')  # Перенаправление на страницу входа
            except Exception as e:
                messages.error(request, f'Ошибка при регистрации: {str(e)}')
        else:
            # Обработка ошибок, если сериализатор не валиден
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
        
        # Рендеринг страницы регистрации с сохранением годов и месяцев
        current_year = datetime.now().year
        years = range(current_year - 100, current_year - 17)
        month_names = list(cal.month_name)[1:]
        return render(request, template_name, {'years': years, 'month_names': month_names})
    
def login_view(request):
    template_name = 'main/login.html'
    
    if request.method == 'GET':
        return render(request, template_name)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли!')
            return redirect('home')
        else:
            messages.error(request, 'Неверный email или пароль.')
            return render(request, template_name)  # Добавлен return