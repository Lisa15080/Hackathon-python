from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),

    # Регистрация
    path('register/', views.register, name='register'),

    # Вход/Выход 
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # Профиль текущего пользователя
    path('profile/', views.profile, name='profile'),

    # Каталог другого пользователя
    path('user/<int:pk>/', views.user_detail, name='user_detail'),
]
]
