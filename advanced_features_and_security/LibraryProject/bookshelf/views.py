from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
from django.views.generic.detail import DetailView
from .models import Book, Library


# Existing ones
def list_books(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/list_books.html', {'books': books})

def add_book(request):
    return render(request, 'bookshelf/add_book.html')  # Or use HttpResponse as before


# ✅ New required views
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Or wherever you want
    else:
        form = UserCreationForm()
    return render(request, 'bookshelf/register.html', {'form': form})


def admin_view(request):
    return render(request, 'bookshelf/admin_view.html')

def librarian_view(request):
    return render(request, 'bookshelf/librarian_view.html')

def member_view(request):
    return render(request, 'bookshelf/member_view.html')

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/edit_book.html', {'book': book})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/delete_book.html', {'book': book})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'bookshelf/library_detail.html'
