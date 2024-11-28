from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Кастомное разрешение, которое проверяет, является ли пользователь администратором.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

class IsSeller(permissions.BasePermission):
    """
    Кастомное разрешение, которое проверяет, является ли пользователь продавцом.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'seller'

class IsCustomer(permissions.BasePermission):
    """
    Кастомное разрешение, которое проверяет, является ли пользователь клиентом.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'client'
