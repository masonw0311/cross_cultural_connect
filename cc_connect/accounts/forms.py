from django import forms
from django.contrib.auth.models import User

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class ProfileUpdateForm(forms.Form):
    country_of_origin = forms.CharField(max_length=100)
