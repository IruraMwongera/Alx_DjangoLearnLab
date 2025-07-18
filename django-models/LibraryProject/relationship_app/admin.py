from django.contrib import admin
from .models import Book, Author, Library, Librarian, UserProfile  # Include UserProfile

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Library)
admin.site.register(Librarian)
admin.site.register(UserProfile)  # Add this line
