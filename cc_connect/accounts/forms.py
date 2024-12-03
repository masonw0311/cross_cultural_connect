from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class ProfileUpdateForm(forms.Form):
    country_of_origin = forms.CharField(max_length=100)


class UserRegistrationForm(UserCreationForm):
    country_of_origin = forms.ChoiceField(
        choices=[
            ('', 'Select your country'),
            ('Mexico', '🇲🇽 Mexico'),
            ('Brazil', '🇧🇷 Brazil'),
            ('United States', '🇺🇸 United States'),
        ],
        required=True,
        label='Country'
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'country_of_origin']
