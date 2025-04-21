from django.contrib.sites import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Max 
from .forms import CreateListForm
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

    # Fetch from Google Books API
    query = request.GET.get("q", "fiction") # default to fiction

    # Using the Google Books API (without API key)
    google_books_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&orderBy=relevance&maxResults=20"

    try:
        response = requests.get(google_books_url)
        response.raise_for_status()
        google_books = response.json().get("items", [])
    except Exception as e:
        google_books = []
        messages.error(request, f"Google Books API error: {e}")

    # format the results
    books = []
    for item in google_books:
        volume_info = item.get("volumeInfo", {})
        industry_ids = volume_info.get("industryIdentifiers", [])
        isbn = next((id['identifier'] for id in industry_ids if id['type'] == 'ISBN_13'), None)

        books.append({
            "google_id": item.get("id"),
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
        google_id = request.POST.get("google_id")

        # get book info from Google again using the volume ID
        book_data = next((book for book in books if book["google_id"] == google_id), None)

        if list_id and book_data:
            try:
                # save book to DB if not already there
                book, created = BookDetails.objects.get_or_create(
                    isbn=book_data["isbn"] or google_id,
                    defaults={
                        "title": book_data["title"],
                        "authors": book_data["authors"],
                        "pages": book_data["pages"],
                        "date_published": book_data["date_published"],
                        "average_rating": book_data["average_rating"],
                        "description": book_data["description"]
                    }
                )

                # avoid duplicates in the list
                if ListBooks.objects.filter(list_id=list_id, book_id=book.book_id).exists():
                    list_name = Lists.objects.get(list_id=list_id).list_name
                    messages.warning(request, f"This book is already in the list '{list_name}'.")
                else:
                    ListBooks.objects.create(list_id=list_id, book_id=book.book_id)
                    list_name = Lists.objects.get(list_id=list_id).list_name
                    messages.success(request, f"This book is now in the list '{list_name}'.")

            except IntegrityError:
                messages.error(request, f"Could not add the book to the list.")

            return redirect("all_books")

    return render(request, 'plotTwist/all_books.html', {
        "books": books,
        'user_lists': user_lists,
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
