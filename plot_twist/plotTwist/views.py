from django.shortcuts import render, redirect
from .models import BookDetails, Lists, ListBooks, Users
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
