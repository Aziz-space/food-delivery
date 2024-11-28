from django.db import models
from django.conf import settings

class Dish(models.Model):
    name = models.CharField(verbose_name='название', max_length=100)
    description = models.TextField(verbose_name='описание', blank=True, max_length=300)
    price = models.DecimalField(verbose_name='цена', max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    weight = models.DecimalField(verbose_name='вес (граммы)', max_digits=5, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(verbose_name='количество в наличии', default=0)
    image = models.ImageField(upload_to='dishes/images/', blank=True, null=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='продавец', on_delete=models.CASCADE, limit_choices_to={'role': 'seller'}, blank=True, null=True)
    categories = models.ManyToManyField('Category', verbose_name='категории', related_name='dishes', blank=True)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name



# Модель категории
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('accepted', 'Принято'),
        ('delivered', 'Доставлено'),
        ('canceled', 'Отменено'),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'client'},
        blank=True,
        null=True
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    delivery_option = models.CharField(
        max_length=10,
        choices=[('pickup', 'Самовывоз'), ('delivery', 'Доставка')],
        blank=True,
        null=True
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Дата создания заказа

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.id} от {self.customer}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена за блюдо на момент заказа

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.dish.name} x {self.quantity}'

class Cart(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'client'},
        blank=True,
        null=True
    )
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина: {self.customer} - {self.dish.name} x {self.quantity}'


class UserBalance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'client'},blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Баланс пользователя'
        verbose_name_plural = 'Балансы пользователей'
