from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """Розширена модель користувача"""
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    bio = models.TextField(blank=True, null=True, verbose_name='Про себе')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата народження')

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return self.username

