from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

# Serializer for the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # Custom validation: publication year cannot be in the future
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# Serializer for the Author model with nested books
class AuthorSerializer(serializers.ModelSerializer):
    # Nested representation of related books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

    # This nested structure allows viewing all books associated with an author
