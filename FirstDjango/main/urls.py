
from django.urls import path
from main.views import (
    IndexView,
    AboutView,
    RegisterView,
    LogoutView,
    mark_notification_read,
    mark_all_notifications_read
)

urlpatterns = [

    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('notification/<int:notification_id>/read/', mark_notification_read, name='mark_notification_read'),
    path('notifications/read-all/', mark_all_notifications_read, name='mark_all_notifications_read'),

]
