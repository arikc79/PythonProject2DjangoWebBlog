from django.urls import path
from workers.views import all_workers_view

urlpatterns = [
    path('all/', all_workers_view, name='all_workers'),

]
