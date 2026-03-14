from django.shortcuts import render, redirect, get_object_or_404
import random

from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from workers.models import Notification


# Create your views here.


# PREDICTIONS = [
#     'Сьогодні вдалий день для нових ідей.',
#     'Не поспішайте: спокій принесе кращі рішення.',
#     'Добра новина вже близько.',
#     'Сьогодні варто завершити давню справу.',
#     'Зустріч принесе несподівану користь.',
#     'Час для маленьких кроків уперед.',
#     'Ваше терпіння сьогодні буде винагороджено.',
#     'Інтуїція підкаже правильний шлях.',
#     'Очікуйте приємний сюрприз.',
#     'Сьогодні корисно спробувати щось нове.',
# ]
#
#
# def index_view(request):
#     context = {
#         'title': 'Головна сторінка',
#         'first_value': 'Ласкаво просимо на головну сторінку',
#         'second_value': random.randint(1, 100),
#         'range': range(1, 100),
#         'prediction': random.choice(PREDICTIONS),
#     }
#
#     return render(request, 'main/index.html', context)
#
#
def all_workers_view(request):
    context = {'title': 'Всі працівники', }

    return render(request, 'main/all_workers.html', context)


class IndexView(TemplateView):
    template_name = 'main/index.html'

    predictions = ['Сьогодні вдалий день для нових ідей.', 'Не поспішайте: спокій принесе кращі рішення.',
        'Добра новина вже близько.', 'Сьогодні варто завершити давню справу.', 'Зустріч принесе несподівану користь.',
        'Час для маленьких кроків уперед.', 'Ваше терпіння сьогодні буде винагороджено.',
        'Інтуїція підкаже правильний шлях.', 'Очікуйте приємний сюрприз.', 'Сьогодні корисно спробувати щось нове.', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['prediction'] = random.choice(self.predictions)

        # Додаємо сповіщення для авторизованих користувачів
        if self.request.user.is_authenticated:
            notifications = Notification.objects.filter(
                recipient=self.request.user
            ).order_by('-date_created')[:5]  # Останні 5 сповіщень

            unread_count = Notification.objects.filter(
                recipient=self.request.user,
                is_read=False
            ).count()

            context['notifications'] = notifications
            context['unread_count'] = unread_count

        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Про нас'
        context['author'] = 'Ваше ім\'я'
        return context


class RegisterView(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'main/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрація успішна! Ви увійшли в систему.')
            return redirect('index')
        return render(request, 'main/register.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        messages.info(request, 'Ви успішно вийшли з системи.')
        return redirect('index')

    def post(self, request):
        logout(request)
        messages.info(request, 'Ви успішно вийшли з системи.')
        return redirect('index')


@login_required
def mark_notification_read(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )

    notification.is_read = True
    notification.save()

    messages.success(request, 'Сповіщення позначено як прочитане')
    return redirect('index')


@login_required
def mark_all_notifications_read(request):

    updated_count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True)

    if updated_count > 0:
        messages.success(request, f'Позначено {updated_count} сповіщень як прочитані')
    else:
        messages.info(request, 'Немає непрочитаних сповіщень')

    return redirect('index')

