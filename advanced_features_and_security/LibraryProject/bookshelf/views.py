from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.views.generic.detail import DetailView

from .models import Book, Library
from .forms import BookForm, ExampleForm  # ✅ Add ExampleForm

def set_csp_headers(response):
    """
    Helper function to add Content Security Policy headers.
    """
    response['Content-Security-Policy'] = "default-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self';"
    return response

@permission_required('bookshelf.view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    response = render(request, 'bookshelf/list_books.html', {'books': books})
    return set_csp_headers(response)

@permission_required('bookshelf.add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    response = render(request, 'bookshelf/form_example.html', {'form': form})
    return set_csp_headers(response)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'bookshelf/library_detail.html'

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        return set_csp_headers(response)
