from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    nickname = forms.CharField(label="Nickname", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ("nickname", "password1", "password2")

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Nickname", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
