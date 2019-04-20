from django.urls import path, reverse_lazy
from . import views

app_name = 'tic_tac_toe'

urlpatterns = [
    path('', views.play_tic_tac_toe, name='play'), #процесс игры
    path('settings/', views.show_settings, name='settings') # настройки игры
]