from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Адмін-панель для кастомної моделі User"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Додаткова інформація', {'fields': ('avatar', 'bio', 'birth_date')}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Додаткова інформація', {'fields': ('avatar', 'bio', 'birth_date')}),
    )

