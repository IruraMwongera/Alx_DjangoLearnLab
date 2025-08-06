from django.urls import path
from .views import (
    BookListView, BookDetailView, BookCreateView,
    BookUpdateView, BookDeleteView
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),                    # Supports ?search=, ?ordering=, ?title=
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),      # GET single book
    path('books/create/', BookCreateView.as_view(), name='book-create'),        # POST to create
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'), # PUT/PATCH to update
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'), # DELETE to delete
]

