from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book, Library
from django.views.generic.detail import DetailView

@permission_required('bookshelf.view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/list_books.html', {'books': books})

def add_book(request):
    return HttpResponse("This is the Add Book page.")

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'bookshelf/library_detail.html'
