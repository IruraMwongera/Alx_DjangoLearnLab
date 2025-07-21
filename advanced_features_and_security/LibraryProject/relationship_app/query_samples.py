import sys
import os

# Add the outer LibraryProject folder to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")

import django
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def run_queries():
    # Query 1: All books by a specific author
    author_name = "John Doe"
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)
    print(f"Books by {author_name}: {[book.title for book in books_by_author]}")

    # Query 2: List all books in a library
    library_name = "Central Library"
    library = Library.objects.get(name=library_name)
    library_books = library.books.all()
    print(f"Books in {library_name}: {[book.title for book in library_books]}")

    # Query 3: Retrieve the librarian for a library
    librarian = Librarian.objects.get(library=library)
    print(f"Librarian at {library_name}: {librarian.name}")

if __name__ == "__main__":
    run_queries()