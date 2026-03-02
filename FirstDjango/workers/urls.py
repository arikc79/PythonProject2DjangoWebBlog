from django.urls import path

from workers.views import (WorkersListView, WorkerUpdateView, WorkerDeleteView, WorkerCreateView,
                           WorkerDetailView, ResumeCreateView, ResumeUpdateView, ResumeDeleteView,
                           ContactCreateView, WorkerSearchView)

urlpatterns = [
    path('', WorkersListView.as_view(), name='all_workers'),
    path('all/', WorkersListView.as_view(), name='all_workers'),
    path('search/', WorkerSearchView.as_view(), name='worker_search'),
    path('create/', WorkerCreateView.as_view(), name='create_worker'),
    path('<int:pk>/', WorkerDetailView.as_view(), name='worker_detail'),
    path('edit/<int:pk>/', WorkerUpdateView.as_view(), name='edit_worker'),
    path('delete/<int:pk>/', WorkerDeleteView.as_view(), name='delete_worker'),
    path('<int:worker_pk>/resume/create/', ResumeCreateView.as_view(), name='create_resume'),
    path('resume/<int:pk>/edit/', ResumeUpdateView.as_view(), name='edit_resume'),
    path('resume/<int:pk>/delete/', ResumeDeleteView.as_view(), name='delete_resume'),
    path('<int:worker_pk>/contact/create/', ContactCreateView.as_view(), name='create_contact'),
]
