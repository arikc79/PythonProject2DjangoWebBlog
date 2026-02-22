from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Post

User = get_user_model()


class RegisterForm(UserCreationForm):
    """Форма реєстрації користувача"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Електронна пошта'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ім\'я користувача'
        })
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )
    password2 = forms.CharField(
        label='Підтвердження пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Підтвердіть пароль'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    """Форма входу користувача"""
    username = forms.CharField(
        label='Ім\'я користувача',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть ім\'я користувача'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть пароль'
        })
    )


class PostForm(forms.ModelForm):
    """Форма для створення та редагування поста"""
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок поста'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Зміст поста',
                'rows': 10
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
