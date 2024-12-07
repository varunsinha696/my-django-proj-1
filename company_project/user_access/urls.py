from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='user_access/login.html'), name='login'),
    path('logout/', LoginView.as_view(), name='logout'),
]
