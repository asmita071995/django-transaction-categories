from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    mobile = forms.CharField(max_length=15)
    city = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

