from django.contrib import admin
from .models import Book, Author  # Import Author

admin.site.register(Book)
admin.site.register(Author)  # Register Author too
