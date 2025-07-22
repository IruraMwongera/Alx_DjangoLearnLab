# bookshelf/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='list_books'),  # ✅ Correct
    path('add/', views.add_book, name='add_book'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]

