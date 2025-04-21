from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Max 
from .forms import CreateListForm
import requests
from django.db.utils import IntegrityError

# Referenced: https://www.w3schools.com/django/django_views.php

from django.shortcuts import render
from .models import BookDetails, ListBooks, Lists, ListTypes, Users


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("all_books")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def all_books(request):
    print(f"logged-in user: {request.user}")
    user_lists = Lists.objects.filter(user=request.user)

    # Using the Google Books API (without API key)
    google_books_url = "https://www.googleapis.com/books/v1/volumes?q=the&orderBy=relevance"
    try:
        response = requests.get(google_books_url)
        response.raise_for_status()
        google_books = response.json().get("items", [])
    except Exception as e:
        google_books = []
        messages.error(request, f"Google Books API error: {e}")

    books = list(BookDetails.objects.all())
    for item in google_books:
        volume_info = item.get("volumeInfo", {})
        isbn = next((identifier["identifier"] for identifier in volume_info.get("industryIdentifiers", [])
                     if identifier["type"] == "ISBN_13"), None)
        if isbn and not any(getattr(book, 'isbn', None) == isbn for book in books if isinstance(book, BookDetails)):
            books.append({
                "title": volume_info.get("title", "Unknown"),
                "authors": ", ".join(volume_info.get("authors", [])),
                "isbn": isbn,
                "pages": volume_info.get("pageCount"),
                "date_published": volume_info.get("publishedDate"),
                "average_rating": volume_info.get("averageRating", "N/A"),
                "description": volume_info.get("description", "No description available.")
            })

    # Handle adding books to lists
    if request.method == "POST":
        list_id = request.POST.get("list_id")
        book_id = request.POST.get("book_id")

        if list_id and book_id:
            existing_entry = ListBooks.objects.filter(list_id=list_id, book_id=book_id).exists()
            if existing_entry:
                list_name = Lists.objects.get(list_id=list_id).list_name
                messages.warning(request, f"This book is already in the list '{list_name}'.")
            else:
                # Add book to database if it doesn't exist
                book_data = next((book for book in books if book.get("isbn") == book_id), None)
                if book_data:
                    try:
                        book, created = BookDetails.objects.get_or_create(
                            isbn=book_data["isbn"],
                            defaults={
                                "title": book_data["title"],
                                "authors": book_data["authors"],
                                "pages": book_data["pages"],
                                "date_published": book_data["date_published"],
                                "average_rating": book_data["average_rating"],
                                "description": book_data["description"]
                            }
                        )
                        if created:
                            messages.success(request, f"Book '{book_data['title']}' added to database.")
                        ListBooks.objects.create(list_id=list_id, book_id=book.book_id)
                        list_name = Lists.objects.get(list_id=list_id).list_name
                        messages.success(request, f"The book has been successfully added to the list '{list_name}'.")
                    except IntegrityError:
                        messages.error(request, f"Failed to add book '{book_data['title']}' to the list.")
                else:
                    messages.error(request, "Failed to find book data.")
            return redirect('all_books')

    return render(request, 'plotTwist/all_books.html', {
        'books': books,
        'user_lists': user_lists
    })


def view_lists(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user_lists = Lists.objects.filter(user=request.user).prefetch_related('listbooks_set__book')
    form = CreateListForm()

    if request.method == 'POST':
        form = CreateListForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.user = request.user

            max_id = Lists.objects.aggregate(Max('list_id'))['list_id__max'] or 0
            new_list.list_id = max_id + 1

            new_list.save()
            messages.success(request, "List created successfully!")
            return redirect("view_lists")

    return render(request, "plotTwist/lists.html", {
        "user_lists": user_lists,
        "form": form,
    })


def rename_list(request, list_id):
    if request.method == 'POST':
        new_name = request.POST.get('new_name', '').strip()
        if new_name:
            user_list = get_object_or_404(Lists, list_id=list_id, user=request.user)
            user_list.list_name = new_name
            user_list.save()
            messages.success(request, 'List renamed successfully!')
    return redirect('view_lists')


def delete_list(request, list_id):
    if request.method == 'POST':
        user_list = get_object_or_404(Lists, list_id=list_id, user=request.user)

        # Delete all book entries tied to the list
        ListBooks.objects.filter(list=user_list).delete()

        # Now delete the list itself
        user_list.delete()
        messages.success(request, 'List and its books deleted successfully.')
    return redirect('view_lists')

def remove_book(request, list_id, book_id):
    if request.method == 'POST':
        ListBooks.objects.filter(list_id=list_id, book_id=book_id).delete()
        messages.success(request, 'Book removed from list.')
    return redirect('view_lists')
