from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import ProfileForm

User = get_user_model()


@login_required(login_url='login')
def profile(request, username):
    """Профіль користувача"""
    user = get_object_or_404(User, username=username)
    posts = user.posts.filter(published=True).order_by('-created_at')

    context = {
        'profile_user': user,
        'posts': posts,
        'is_own_profile': request.user == user
    }
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    """Редагування профілю"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профіль успішно оновлено!')
            return redirect('users:profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})
