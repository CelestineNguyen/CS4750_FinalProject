from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Referenced: https://www.w3schools.com/django/django_views.php


def register(request):
    return render(request, 'register.html')
