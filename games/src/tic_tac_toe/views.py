from django.shortcuts import render


def play_tic_tac_toe(request, **kwargs):
    return render(request, 'tic-tac_toe/index.html')

def show_settings(request, **kwargs):
    pass
