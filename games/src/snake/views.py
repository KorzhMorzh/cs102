from django.shortcuts import render, redirect
from .models import Leaders

def play_snake(request, **kwargs):
    #if kwargs.get('user'):
    return render(request, 'snake/snake.html',)
    #else:
     #   redirect('login')

def show_leaderboard(request, **kwargs):
    leaders = Leaders.objects.order_by('score')[:20]
    return render (request, 'snake/leaderboard.html', {'leaders' : leaders})

def show_settings(request, **kwargs):
    pass
