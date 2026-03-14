from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import Group, User
from workers.models import Worker, Notification


def notify_hr(text: str):
    hr_group = Group.objects.get(name='HR')
    hr_users = hr_group.user_set.all()

    # for user in hr_users:
    #     Notification.objects.create(
    #         recipient=user,
    #         text=text
    #     )

    notification = [Notification(recipient=user, text=text) for user in hr_users]
    Notification.objects.bulk_create(notification)


@receiver(post_save, sender=Worker)  #сигнал який спрацьовує після збереження моделі Worker
def notify_hr_on_worker_create(sender, instance, created, **kwargs):
    if not created:
        return

    notify_hr(f'Створено нового працівника: {instance.name}')


@receiver(post_delete, sender=Worker)  # сигнал який спрацьовує після видалення моделі Worker
def notify_hr_on_worker_delete(sender, instance, using, **kwargs):
    notify_hr(f'Звільнено працівника: {instance.name}')


@receiver(post_save, sender=User)  # сигнал, який спрацьовує після збереження моделі User
def add_user_to_hr_group(sender, instance, created, **kwargs):
    if not created:
        return

    hr_group, group_created = Group.objects.get_or_create(name='HR')

    instance.groups.add(hr_group)

    print(f'Користувача "{instance.username}" автоматично додано до групи HR!')
