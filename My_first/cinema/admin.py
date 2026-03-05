from django.contrib import admin
from cinema.models import Movie, Session, Review


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'genre', 'duration', 'created_at']
    list_filter = ['genre', 'year']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    actions = ['delete_selected']

    def has_delete_permission(self, request, obj=None):
        """Дозволити видаляти тільки адміністраторам та робітникам"""
        return request.user.is_superuser or request.user.groups.filter(name='Робітник').exists()


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['movie', 'date', 'hall_number', 'created_at']
    list_filter = ['date', 'hall_number']
    search_fields = ['movie__title']
    ordering = ['date']

    def has_delete_permission(self, request, obj=None):
        """Дозволити видаляти тільки адміністраторам та робітникам"""
        return request.user.is_superuser or request.user.groups.filter(name='Робітник').exists()

    def has_add_permission(self, request):
        """Дозволити додавати тільки адміністраторам та робітникам"""
        return request.user.is_superuser or request.user.groups.filter(name='Робітник').exists()

    def has_change_permission(self, request, obj=None):
        """Дозволити редагувати тільки адміністраторам та робітникам"""
        return request.user.is_superuser or request.user.groups.filter(name='Робітник').exists()


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'movie']
    search_fields = ['user__username', 'movie__title', 'text']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'user']

    def has_delete_permission(self, request, obj=None):
        """Дозволити видаляти тільки адміністраторам та робітникам"""
        return request.user.is_superuser or request.user.groups.filter(name='Робітник').exists()

    def has_add_permission(self, request):
        """Дозволити додавати тільки адміністраторам та робітникам"""
        return request.user.is_superuser or request.user.groups.filter(name='Клієнт').exists() or request.user.groups.filter(name='Робітник').exists()

    def has_change_permission(self, request, obj=None):
        """Дозволити редагувати тільки власнику або адміністраторам"""
        if obj is None:
            return True
        return request.user.is_superuser or obj.user == request.user
