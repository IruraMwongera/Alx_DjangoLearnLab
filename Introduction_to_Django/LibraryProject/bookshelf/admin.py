from django.contrib import admin

# Register your models here.
from.models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # shows these fields in list view
    search_fields = ('title', 'author')  # enables search by title and author
    list_filter = ('publication_year',)  # enables filtering by publication year
