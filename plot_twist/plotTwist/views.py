from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Max 
from .forms import CreateListForm

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
    # will need to add logged in user once that gets working
    books = BookDetails.objects.all()
    #user = Users.objects.get(user_id=6)
    user_lists = Lists.objects.filter(user=request.user)

    # Asked chat to help me to display all the lists of a signed in user and allow the user to add a book to one of
    # those lists
    if request.method == "POST":
        list_id = request.POST.get("list_id")
        book_id = request.POST.get("book_id")

        if list_id and book_id:
            existing_entry = ListBooks.objects.filter(list_id=list_id, book_id=book_id).exists()
            if existing_entry:
                list_name = Lists.objects.get(list_id=list_id).list_name
                messages.warning(request, f"This book is already in the list '{list_name}'.")
            else:
                ListBooks.objects.create(
                    list_id=list_id,
                    book_id=book_id
                )
                list_name = Lists.objects.get(list_id=list_id).list_name
                messages.success(request, f"The book has been successfully added to the list '{list_name}'.")

            return redirect('all_books')  # Redirect back to the same page

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
        user_list.delete()
        messages.success(request, 'List deleted successfully.')
    return redirect('view_lists')

def remove_book(request, list_id, book_id):
    if request.method == 'POST':
        ListBooks.objects.filter(list_id=list_id, book_id=book_id).delete()
        messages.success(request, 'Book removed from list.')
    return redirect('view_lists')
