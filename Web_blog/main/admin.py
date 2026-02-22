from django.contrib import admin
from .models import Post


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published')
    list_filter = ('published', 'created_at', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
