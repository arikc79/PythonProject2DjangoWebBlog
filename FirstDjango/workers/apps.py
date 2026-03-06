from django.apps import AppConfig

from django.db.models.signals import post_save, post_delete

class WorkersConfig(AppConfig):
    name = 'workers'


    def ready(self):
        import workers.signals



