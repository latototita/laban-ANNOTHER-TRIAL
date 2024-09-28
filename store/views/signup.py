from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .home import store
from django.views import View
from .forms import RegistrationForm

def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')  # Redirect after successful form submission
    else:
        form = RegistrationForm()

    return render(request, 'signup.html', {"form": form})
