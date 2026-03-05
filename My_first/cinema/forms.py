from django import forms
from cinema.models import Movie, Session, Review


class MovieForm(forms.ModelForm):
    """Форма для створення/редагування фільму"""

    class Meta:
        model = Movie
        fields = ['title', 'description', 'year', 'duration', 'genre', 'poster']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть назву фільму'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Опис фільму'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1895,
                'max': 2100
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Тривалість у хвилинах'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-control'
            }),
            'poster': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }


class SessionForm(forms.ModelForm):
    """Форма для створення сеансу"""

    class Meta:
        model = Session
        fields = ['movie', 'date', 'hall_number']
        widgets = {
            'movie': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'hall_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 20,
                'placeholder': 'Номер зали (1-20)'
            })
        }


class ReviewForm(forms.ModelForm):
    """Форма для додавання відгуку"""

    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ваш відгук про фільм'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': 'Оцінка (1-10)'
            })
        }

