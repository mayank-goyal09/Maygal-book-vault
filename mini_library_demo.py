from books import Book
from member_basic import Member
from exceptions import (
    MemberNotFoundError,
    BookNotFoundError,
    BookNotAvailableError,
    BorrowLimitExceededError,LibraryError
)
from utils.file_handler import save_books, load_books, save_members, load_members



class Library:
    """Manages books and members, and coordinates issuing/returning."""

    def __init__(self, name):
        self._name = name
        self._books = load_books()
        self._members = load_members()
          # will persist later

    
    def save_all(self):
        save_books(self._books)
        save_members(self._members)


    # ---------- BOOK MANAGEMENT ----------

    def add_book(self, book: Book):
        """Add a Book object to the library."""
        self._books[book.book_id] = book

    def get_book(self, book_id):
        return self._books.get(book_id)

    # ---------- MEMBER MANAGEMENT ----------

    def register_member(self, member: Member):
        """Add a Member object to the library."""
        self._members[member._member_id] = member  # later we'll add a property

    def get_member(self, member_id):
        return self._members.get(member_id)

    # ---------- ISSUE / RETURN LOGIC ----------

    def issue_book(self, member_id, book_id):
        member = self.get_member(member_id)
        book = self.get_book(book_id)

        if member is None:
            raise MemberNotFoundError(f"Member '{member_id}' not found")

        if book is None:
            raise BookNotFoundError(f"Book '{book_id}' not found")

        if not book.is_available():
            raise BookNotAvailableError(f"Book '{book_id}' not available")

        if not member.can_borrow():
            raise BorrowLimitExceededError(f"Member '{member_id}' reached limit")

        book.borrow_book()
        member.borrow_book(book.book_id)
        return True

    def return_book(self, member_id, book_id):
        member = self.get_member(member_id)
        book = self.get_book(book_id)

        if member is None:
            raise MemberNotFoundError(f"Member '{member_id}' not found")

        if book is None:
            raise BookNotFoundError(f"Book '{book_id}' not found")

        if not member.return_book(book_id):
            # Book not in member's list – illegal state
            raise LibraryError("Member did not borrow this book")

        if not book.return_book():
            # More returns than issues – illegal state
            raise LibraryError("Book return invalid (copies mismatch)")

        return True


    # ---------- UTILITY ----------

    def list_books(self):
        if not self._books:
            print("No books in library yet.")
            return
        for book in self._books.values():
            print(book)

    def list_members(self):
        if not self._members:
            print("No members registered yet.")
            return
        for member in self._members.values():
            print(member)

    def search_books(self, query):
        """Simple case-insensitive search in title or author."""
        query = query.lower()
        results = []
        for book in self._books.values():
            if query in book.title.lower() or query in book.author.lower():
                results.append(book)
        return results

    def stats(self):
        """Return basic stats for dashboard."""
        total_books = len(self._books)
        total_members = len(self._members)
        total_copies = sum(b.total_copies for b in self._books.values())
        available_copies = sum(b.available_copies for b in self._books.values())
        return {
            "total_books": total_books,
            "total_members": total_members,
            "total_copies": total_copies,
            "available_copies": available_copies,
        }



if __name__ == "__main__":
    library = Library("The Book Vault")

    # Only add book if not already present
    if library.get_book("B001") is None:
        book = Book("B001", "Harry Potter", "J.K. Rowling", "Fantasy", copies=2)
        library.add_book(book)

    member = Member("M001", "Mayank", "mayank@example.com", max_books=1)
    library.register_member(member)

    try:
        library.issue_book("M001", "B001")
    except LibraryError as e:
        print("⚠️ Issue error:", e)

    library.save_all()
    print("💾 Books saved to CSV.")
