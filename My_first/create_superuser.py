import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'My_first.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Видаляємо старого користувача, якщо існує
if User.objects.filter(username='admin').exists():
    User.objects.filter(username='admin').delete()
    print('Старий користувач admin видалено')

# Створюємо нового суперюзера
user = User.objects.create_superuser(username='admin', email='admin@cinema.ua', password='admin123')
print(f'Суперюзер створено: {user.username}')
print('Username: admin')
print('Password: admin123')
