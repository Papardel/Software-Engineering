from django.shortcuts import render


def home(request):
    days_left = 12
    return render(request, 'home.html', {'days_left': days_left})
