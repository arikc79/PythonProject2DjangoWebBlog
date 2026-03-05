from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Movie(models.Model):
    """Модель для фільмів"""
    GENRE_CHOICES = [
        ('action', 'Бойовик'),
        ('comedy', 'Комедія'),
        ('drama', 'Драма'),
        ('horror', 'Жахи'),
        ('fantasy', 'Фентезі'),
        ('sci-fi', 'Наукова фантастика'),
        ('thriller', 'Трилер'),
        ('romance', 'Романтика'),
        ('animation', 'Анімація'),
        ('documentary', 'Документальний'),
    ]

    title = models.CharField(max_length=200, verbose_name='Назва фільму')
    description = models.TextField(verbose_name='Опис')
    year = models.IntegerField(
        verbose_name='Рік випуску',
        validators=[MinValueValidator(1895), MaxValueValidator(2100)]
    )
    duration = models.IntegerField(
        verbose_name='Тривалість (хв)',
        validators=[MinValueValidator(1)]
    )
    genre = models.CharField(
        max_length=20,
        choices=GENRE_CHOICES,
        verbose_name='Жанр'
    )
    poster = models.ImageField(
        upload_to='posters/',
        blank=True,
        null=True,
        verbose_name='Постер'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Фільм'
        verbose_name_plural = 'Фільми'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.year})"

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'pk': self.pk})

    def average_rating(self):
        """Середня оцінка фільму"""
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(review.rating for review in reviews) / reviews.count(), 1)
        return 0


class Session(models.Model):
    """Модель для сеансів фільмів"""
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name='Фільм'
    )
    date = models.DateTimeField(verbose_name='Дата та час сеансу')
    hall_number = models.IntegerField(
        verbose_name='Номер зали',
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеанси'
        ordering = ['date']

    def __str__(self):
        return f"{self.movie.title} - {self.date.strftime('%d.%m.%Y %H:%M')} (Зала {self.hall_number})"


class Review(models.Model):
    """Модель для відгуків на фільми"""
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Фільм'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Користувач'
    )
    text = models.TextField(verbose_name='Текст відгуку')
    rating = models.IntegerField(
        verbose_name='Оцінка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
        ordering = ['-created_at']
        # Один користувач - один відгук на фільм
        unique_together = ('movie', 'user')

    def __str__(self):
        return f"Відгук від {self.user.username} на {self.movie.title} - {self.rating}/10"

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'pk': self.movie.pk})

