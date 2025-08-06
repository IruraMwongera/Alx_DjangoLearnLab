from rest_framework import generics, permissions, filters
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework

# List all books (Read only, open to all)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    
    # Filter by field names
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Searchable fields
    search_fields = ['title', 'author']
    
    # Orderable fields
    ordering_fields = ['title', 'publication_year']
    
    permission_classes = [permissions.AllowAny]
# Retrieve one book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public

# Create a new book (Authenticated users only)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # You can log, modify or assign default values here
        print("Creating book...")
        serializer.save()
# Update a book (Authenticated users only)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Custom behavior (e.g., logging update)
        print("Updating book...")
        serializer.save()

# Delete a book (Authenticated users only)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]