class Book:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"Book {self.name}"


class BookShelf:
    def __init__(self, *books: Book) -> None:
        self.books = books

    def __str__(self) -> str:
        return f"BookShelf with {len(self.books)} books."


book = Book("Harry Potter")
book2 = Book("GOT")
shelf = BookShelf(book, book2)

print(shelf)
