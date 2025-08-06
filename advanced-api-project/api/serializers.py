from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

# BookSerializer serializes all Book fields
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # Custom validation: publication_year must not be in the future
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# AuthorSerializer includes nested list of books
class AuthorSerializer(serializers.ModelSerializer):
    # Nested books using BookSerializer
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
