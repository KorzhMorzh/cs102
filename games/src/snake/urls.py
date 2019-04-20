from django.urls import path, reverse_lazy
from . import views

app_name = 'snake'

urlpatterns = [
    path('', views.play_snake, name='play'), #процесс игры
    path('leaderboards/', views.show_leaderboard, name='leaderboards'), #таблица лидеров
    path('settings/', views.show_settings, name='settings') # настройки игры
]