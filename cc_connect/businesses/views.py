from django.shortcuts import render

def homepage(request):
    return render(request, 'businesses/home.html')