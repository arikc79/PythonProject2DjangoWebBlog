from django.urls import path
from workers.views import WorkersListView, WorkerUpdateView, WorkerDeleteView

urlpatterns = [
    path('all/', WorkersListView.as_view(), name='all_workers'),
    path('edit/<int:pk>/', WorkerUpdateView.as_view(), name='edit_worker'),
    path('delete/<int:pk>/', WorkerDeleteView.as_view(), name='delete_worker'),

]
