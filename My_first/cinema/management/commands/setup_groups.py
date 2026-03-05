from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from cinema.models import Movie, Session, Review


class Command(BaseCommand):
    help = 'Створює групи користувачів та налаштовує права доступу'

    def handle(self, *args, **options):
        # Отримуємо типи контенту
        movie_ct = ContentType.objects.get_for_model(Movie)
        session_ct = ContentType.objects.get_for_model(Session)
        review_ct = ContentType.objects.get_for_model(Review)

        # Отримуємо дозволи
        movie_add = Permission.objects.get(content_type=movie_ct, codename='add_movie')
        movie_change = Permission.objects.get(content_type=movie_ct, codename='change_movie')
        movie_delete = Permission.objects.get(content_type=movie_ct, codename='delete_movie')

        session_add = Permission.objects.get(content_type=session_ct, codename='add_session')
        session_change = Permission.objects.get(content_type=session_ct, codename='change_session')
        session_delete = Permission.objects.get(content_type=session_ct, codename='delete_session')

        review_add = Permission.objects.get(content_type=review_ct, codename='add_review')
        review_change = Permission.objects.get(content_type=review_ct, codename='change_review')
        review_delete = Permission.objects.get(content_type=review_ct, codename='delete_review')

        # ===== ГРУПА "КЛІЄНТ" =====
        client_group, created = Group.objects.get_or_create(name='Клієнт')
        client_group.permissions.set([
            review_add,      # Може додавати відгуки
            review_change,   # Може редагувати свої відгуки
            review_delete,   # Може видаляти свої відгуки
        ])
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Створена група "Клієнт"'))
        else:
            self.stdout.write(self.style.WARNING('✓ Група "Клієнт" вже існує'))

        # ===== ГРУПА "РОБІТНИК" =====
        worker_group, created = Group.objects.get_or_create(name='Робітник')
        worker_group.permissions.set([
            movie_add,       # Може додавати фільми
            movie_change,    # Може редагувати фільми
            movie_delete,    # Може видаляти фільми
            session_add,     # Може додавати сеанси
            session_change,  # Може редагувати сеанси
            session_delete,  # Може видаляти сеанси
            review_delete,   # Може видаляти будь-які відгуки
        ])
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Створена група "Робітник"'))
        else:
            self.stdout.write(self.style.WARNING('✓ Група "Робітник" вже існує'))

        self.stdout.write(self.style.SUCCESS('\n✓ Групи та права доступу налаштовані успішно!'))

