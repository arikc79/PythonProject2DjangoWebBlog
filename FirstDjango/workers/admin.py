from django.contrib import admin
from workers.models import Worker, Resume, Contact, Notification

# Register your models here.

admin.site.register(Worker)
admin.site.register(Resume)
admin.site.register(Contact)
admin.site.register(Notification)
