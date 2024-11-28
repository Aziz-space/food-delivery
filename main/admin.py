from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Dish, Order, Cart, Category, UserBalance

class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'available', 'img_display', 'seller', 'stock', 'weight')
    search_fields = ('name', 'description')
    list_filter = ('available', 'seller', 'categories')

    def img_display(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "Нет изображения"
    img_display.short_description = 'Изображение'


class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')

admin.site.register(Dish, DishAdmin)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(UserBalance, UserBalanceAdmin)