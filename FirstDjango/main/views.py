from django.shortcuts import render
import random


# Create your views here.

# A small pool of short predictions for the day.
PREDICTIONS = [
    'Сьогодні вдалий день для нових ідей.',
    'Не поспішайте: спокій принесе кращі рішення.',
    'Добра новина вже близько.',
    'Сьогодні варто завершити давню справу.',
    'Зустріч принесе несподівану користь.',
    'Час для маленьких кроків уперед.',
    'Ваше терпіння сьогодні буде винагороджено.',
    'Інтуїція підкаже правильний шлях.',
    'Очікуйте приємний сюрприз.',
    'Сьогодні корисно спробувати щось нове.',
]


def index_view(request):
    context = {
        'title': 'Головна сторінка',
        'first_value': 'Ласкаво просимо на головну сторінку',
        'second_value': random.randint(1, 100),
        'range': range(1, 100),
        'prediction': random.choice(PREDICTIONS),
    }

    return render(request, 'main/index.html', context)


def all_workers_view(request):
    context = {
        'title': 'Всі працівники',
    }

    return render(request, 'main/all_workers.html', context)
