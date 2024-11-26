from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def homepage(request):
    return render(request, 'accounts/homepage.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username, password=password)
            return render(request, 'accounts/account_home.html', {'user': user})
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')
    return render(request, 'accounts/signin.html')

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

        user = User(username=username, password=password, country_of_origin=country)
        user.save()
        messages.success(request, 'Account created successfully')
        return redirect('signin')
    return render(request, 'accounts/create_account.html')

#zip code functs


def welcome_page(request):
    username = request.session.get('username', 'Guest')  # Retrieve username from session
    if request.method == 'POST':
        zip_code = request.POST.get('zipcode')
        return redirect('local_businesses', zip_code=zip_code)  # Redirect to businesses page

    return render(request, 'welcome.html', {'username': username})

def process_zip(request):
    if request.method == 'POST':
        zip_code = request.POST.get('zipcode')
        # Process the ZIP code here (e.g., fetch businesses or redirect)
        return render(request, 'result.html', {'zip_code': zip_code})
    return render(request, 'welcome.html')