from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Referenced: https://www.w3schools.com/django/django_views.php

from django.shortcuts import render
from .models import BookDetails

def home(request):
    return render(request, "home.html")



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})

def all_books(request):
    books = BookDetails.objects.all()
    return render(request, 'books/all_books.html', {'books': books})
