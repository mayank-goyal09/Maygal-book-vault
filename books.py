class Book:
    """Represents a book in the library with Pythonic properties."""

    def __init__(self, book_id, title, author, genre, copies=1):
        # Internal (encapsulated) attributes
        self._book_id = book_id
        self._title = title
        self._author = author
        self._genre = genre
        self._total_copies = copies
        self._available_copies = copies

    # ---------- READ-ONLY PROPERTIES ----------

    @property
    def book_id(self):
        return self._book_id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def genre(self):
        return self._genre

    @property
    def total_copies(self):
        return self._total_copies

    @property
    def available_copies(self):
        return self._available_copies

    # ---------- BEHAVIOR METHODS ----------

    def borrow_book(self):
        """Try to borrow one copy; return True if success, else False."""
        if self._available_copies > 0:
            self._available_copies -= 1
            return True
        return False

    def return_book(self):
        """Return one copy; return True if success, else False."""
        if self._available_copies < self._total_copies:
            self._available_copies += 1
            return True
        return False

    def is_available(self):
        return self._available_copies > 0

    def __str__(self):
        return f"{self.title} by {self.author} [{self.available_copies}/{self.total_copies} available]"


if __name__ == "__main__":
    book = Book("B001", "Harry Potter", "J.K. Rowling", "Fantasy", 3)

    print(book)                 # Pretty print
    print(book.title)           # Uses @property
    print(book.author)

    print("Available copies:", book.available_copies)
    book.borrow_book()
    print("After borrow:", book.available_copies)
    book.return_book()
    print("After return:", book.available_copies)


new_book = Book("B002", "The Hobbit", "J.R.R. Tolkien", "Fantasy", 2)
print(new_book.title)  # Accessing title via property
print(new_book.author)        # Using __str__ method   
