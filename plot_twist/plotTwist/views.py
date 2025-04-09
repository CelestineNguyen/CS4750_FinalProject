from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Referenced: https://www.w3schools.com/django/django_views.php

from django.shortcuts import render

def home(request):
    return render(request, "home.html")



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after registration
            return redirect("home")  # or wherever you want
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})