
from django.shortcuts import render, redirect
from .forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('common:registration_complete')
    else:
        form = RegistrationForm()
    return render(request, 'common/register.html', {'form': form})

def registration_complete(request):
    return render(request, 'common/registration_complete.html')
