class Member:
    """Represents a library member."""

    def __init__(self, member_id, name, email, max_books=5):
        self._member_id = member_id
        self._name = name
        self._email = email
        self._max_books = max_books
        self._borrowed_books = []  # will store book_ids for now

    def can_borrow(self):
        return len(self._borrowed_books) < self._max_books

    def borrow_book(self, book_id):
        if self.can_borrow():
            self._borrowed_books.append(book_id)
            return True
        return False

    def return_book(self, book_id):
        if book_id in self._borrowed_books:
            self._borrowed_books.remove(book_id)
            return True
        return False

    def __str__(self):
        return f"{self._name} ({self._member_id}) - Borrowed: {len(self._borrowed_books)}"


if __name__ == "__main__":
    member = Member("M001", "Mayank", "mayank@example.com", max_books=2)

    print(member)
    print("Can borrow?", member.can_borrow())

    member.borrow_book("B001")
    member.borrow_book("B002")
    print(member)
    print("Can borrow?", member.can_borrow())

    member.return_book("B001")
    print(member)
