from bookshelf.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication\_year=1949)

book

\# <Book: 1984>

from bookshelf.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication\_year=1949)

book

\# <Book: 1984>

Book.objects.all()

\# <QuerySet \[<Book: 1984>]>

book = Book.objects.get(title="1984")

book.title, book.author, book.publication\_year

\# ('1984', 'George Orwell', 1949)

book.title = "Nineteen Eighty-Four"

book.save()

book.title

\# 'Nineteen Eighty-Four'

book.delete()

Book.objects.all()

\# <QuerySet \[]>



