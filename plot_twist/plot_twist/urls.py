# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('plotTwist.urls')),
# ]
from plotTwist import views
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.contrib.auth import views as auth_views
from plotTwist import views as your_views

# Referenced: https://www.w3schools.com/django/django_urls.php
# https://www.w3schools.com/django/django_templates.php
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('plotTwist.urls')),
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', views.all_books, name='all_books'),
    path("", your_views.home, name="home"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', your_views.register, name='register'),
]
