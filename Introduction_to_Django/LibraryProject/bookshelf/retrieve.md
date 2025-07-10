Book.objects.all()

\# <QuerySet \[<Book: 1984>]>

book = Book.objects.get(title="1984")

book.title, book.author, book.publication\_year

\# ('1984', 'George Orwell', 1949)



