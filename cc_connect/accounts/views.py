from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

@login_required
def homepage(request):
    return render(request, 'accounts/homepage.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('account_home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

def create_account(request):

    # TODO:
    #       add account creation tips
    #       add privacy policy
    #       add encryption

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        country = request.POST['country']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('create_account')

        user = User.objects.create_user(username=username, password=password, country_of_origin=country)
        user.save()
        messages.success(request, 'Account created successfully')
        return redirect('login')
    return render(request, 'accounts/create_account.html')

#zip code functs

@login_required
def account_home(request):
    username = request.session.get('username', 'Guest')  # Retrieve username from session
    if request.method == 'POST':
        zip_code = request.POST.get('zipcode')
        return redirect('local_businesses', zip_code=zip_code)  # Redirect to businesses page

    return render(request, 'accounts/account_home.html')


def process_zip(request):
    if request.method == 'POST':
        zip_code = request.POST.get('zipcode')
        # Process the ZIP code here (e.g., fetch businesses or redirect)
        return render(request, 'result.html', {'zip_code': zip_code})
    return render(request, 'welcome.html')