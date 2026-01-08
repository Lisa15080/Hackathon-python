from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Регистрация
    path('register/', views.register, name='register'),

    # Профиль
    path('profile/', views.profile, name='profile'),

    # Детальная страница пользователя
    path('profile/<int:pk>/', views.user_detail, name='user_detail'),

    # Список пользователей
    path('list/', views.user_list, name='user_list'),

    # Встроенные views Django для входа/выхода
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html'
    ), name='logout'),
]