
from django.urls import path
from main.views import IndexView, AboutView, RegisterView, LogoutView

urlpatterns = [

    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
