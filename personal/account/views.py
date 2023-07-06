from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CustomAuthenticationForm, CustomUserCreationForm


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'account/home.html') 

def home(request):
    return render(request, 'account/home.html')

def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('account:home'))
    else:
        form = CustomAuthenticationForm(request)
    return render(request, 'account/login.html', {'form': form})

def custom_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('nickname')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('account:home'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})


def custom_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))