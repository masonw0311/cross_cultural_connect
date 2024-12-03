from django.contrib.auth import authenticate, logout, login as auth_login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User
from .forms import AccountUpdateForm, ProfileUpdateForm, UserRegistrationForm

from django.http import JsonResponse
from google.cloud import translate_v2 as translate
import os
from dotenv import load_dotenv

@login_required
def homepage(request):
    return render(request, 'accounts/homepage.html')

def login(request):
    show_success_message = request.session.get('show_success_message', False)
    if show_success_message:
        messages.success(request, 'Your account has been successfully created! You can now log in.')
        # Clear the session flag
        del request.session['show_success_message']

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
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created! You can now log in.')
            request.session['show_success_message'] = True
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/create_account.html', {'form': form})

#zip code functs

@login_required
def account_home(request):
    username = request.session.get('username', 'Guest')  # Retrieve username from session
    if request.method == 'POST':
        zip_code = request.POST.get('zipcode')
        return redirect('local_businesses', zip_code=zip_code)  # Redirect to businesses page

    return render(request, 'accounts/account_home.html')

@login_required
def process_zip(request):
    if request.method == 'POST':
        zip_code = request.POST.get('zipcode', '').strip()
        if not zip_code:
            return render(request, 'account_home.html', {'error': 'Please enter a valid ZIP code.'})

        # Optional: Store ZIP code in session for later use
        request.session['zip_code'] = zip_code

        # Redirect to the welcome page
        return redirect('welcome')  # Replace 'welcome' with your actual URL name for the welcome page

    return render(request, 'account_home.html')

@login_required
def welcome_view(request):
    return render(request, 'accounts/overview.html', {'user': request.user})

@login_required
def overview_view(request):
    return render(request, 'accounts/overview.html')

# Load environment variables from .env file
load_dotenv()

# Set up the API key
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_TRANSLATE_API_KEY")

# Initialize the Translation client
translate_client = translate.Client()

from django.http import JsonResponse
from google.cloud import translate_v2 as translate
import json

translate_client = translate.Client()

def translate_text(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            text = data.get("text", "").strip()
            target_language = data.get("language", "en").strip()

            # Validation
            if not text:
                return JsonResponse({"error": "Text input is required."}, status=400)
            if not target_language:
                return JsonResponse({"error": "Target language is required."}, status=400)

            # API Call
            result = translate_client.translate(text, target_language=target_language)
            return JsonResponse({
                "translatedText": result["translatedText"],
                "sourceLanguage": result.get("detectedSourceLanguage")
            })

        except Exception as e:
            # Log error and return response
            print(f"Error in translation: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('login')  # Redirect to the login page after deletion
    return render(request, 'delete_account.html')  # Renders a confirmation pag

@login_required
def account_management(request):
    if request.method == "POST":
        user = request.user

        # Handle account deletion
        if 'delete_account' in request.POST:
            user.delete()
            logout(request)
            messages.success(request, "Your account has been deleted.")
            return redirect('login')
        
        account_form = AccountUpdateForm(request.POST, instance=user)
        if account_form.is_valid():
            account_form.save()
            messages.success(request, "Your username has been updated.")

        profile_form = ProfileUpdateForm(request.POST)
        if profile_form.is_valid():
            user.country_of_origin = profile_form.cleaned_data['country_of_origin']
            user.save()
            messages.success(request, "Your country of origin has been updated.")

        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            user.set_password(password_form.cleaned_data['new_password1'])
            user.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in after changing password
            messages.success(request, "Your password has been updated.")

    else:        
        account_form = AccountUpdateForm(instance=request.user)        
        profile_form = ProfileUpdateForm(initial={'country_of_origin': request.user.country_of_origin})
        password_form = PasswordChangeForm(request.user)
        
    return render(request, 'accounts/account_management.html', {
        'account_form': account_form,
        'profile_form': profile_form,
        'password_form': password_form,
    })

def privacy_policy(request):
    return render(request, 'accounts/privacy_policy.html')