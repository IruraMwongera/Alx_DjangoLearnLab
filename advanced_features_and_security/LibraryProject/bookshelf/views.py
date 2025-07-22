from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Library
from django.views.generic.detail import DetailView

def list_books(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/list_books.html', {'books': books})

def add_book(request):
    return HttpResponse("This is the Add Book page.")

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'bookshelf/library_detail.html'
