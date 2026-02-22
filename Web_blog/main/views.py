from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import RegisterForm, LoginForm, PostForm


def index(request):
    """Головна сторінка з усіма опублікованими постами"""
    posts = Post.objects.filter(published=True).order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'main/index.html', context)


def register(request):
    """Сторінка реєстрації користувача"""
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрація успішна! Ви увійшли в свій аккаунт.')
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})


def user_login(request):
    """Сторінка входу користувача"""
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Ласкаво просимо, {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Неправильне ім\'я користувача або пароль.')
    else:
        form = LoginForm()

    return render(request, 'main/login.html', {'form': form})


def user_logout(request):
    """Вихід користувача"""
    logout(request)
    messages.success(request, 'Ви вийшли з аккаунту.')
    return redirect('index')


@login_required(login_url='login')
def create_post(request):
    """Створення нового поста"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Пост успішно створено!')
            return redirect('my_posts')
    else:
        form = PostForm()

    return render(request, 'main/create_post.html', {'form': form})


@login_required(login_url='login')
def edit_post(request, post_id):
    """Редагування поста"""
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        messages.error(request, 'Ви можете редагувати тільки свої пости.')
        return redirect('index')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успішно оновлено!')
            return redirect('my_posts')
    else:
        form = PostForm(instance=post)

    return render(request, 'main/edit_post.html', {'form': form, 'post': post})


@login_required(login_url='login')
def delete_post(request, post_id):
    """Видалення поста"""
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        messages.error(request, 'Ви можете видалити тільки свої пости.')
        return redirect('index')

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Пост успішно видалено!')
        return redirect('my_posts')

    return render(request, 'main/confirm_delete.html', {'post': post})


@login_required(login_url='login')
def my_posts(request):
    """Список постів користувача"""
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'main/my_posts.html', context)


def all_posts(request):
    """Сторінка з усіма опублікованими постами з пошуком"""
    from django.db.models import Q

    posts = Post.objects.filter(published=True).order_by('-created_at')
    search_query = request.GET.get('search', '')
    author_filter = request.GET.get('author', '')

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    if author_filter:
        posts = posts.filter(author__username=author_filter)

    # Отримаємо всіх авторів для фільтра
    authors = Post.objects.filter(published=True).values_list('author__username', flat=True).distinct()

    context = {
        'posts': posts,
        'search_query': search_query,
        'author_filter': author_filter,
        'authors': authors,
        'total_posts': posts.count()
    }
    return render(request, 'main/all_posts.html', context)


def post_detail(request, post_id):
    """Детальна сторінка поста"""
    post = get_object_or_404(Post, id=post_id, published=True)
    return render(request, 'main/post_detail.html', {'post': post})
