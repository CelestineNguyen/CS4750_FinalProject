from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('plotTwist.urls')),
]
from django.urls import path
from plotTwist import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', views.all_books, name='all_books'),
]
