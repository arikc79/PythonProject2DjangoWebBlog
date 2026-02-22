from django.db import models
from django.conf import settings


# Create your models here.

class Post(models.Model):
    """Модель для блог-постів"""
    id=models.AutoField(primary_key=True, verbose_name='ID')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Зміст')
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='Зображення')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    published = models.BooleanField(default=False, verbose_name='Опубліковано')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
