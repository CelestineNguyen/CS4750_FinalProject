from django.shortcuts import render
from .models import BookDetails

# Create your views here.
def all_books(request):
    books = BookDetails.objects.all()
    return render(request, 'plotTwist/all_books.html', {'books': books})