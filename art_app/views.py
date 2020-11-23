from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from art_app.forms import RegistrationForm

# Create your views here.
def index(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("index")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})