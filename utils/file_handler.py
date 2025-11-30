import csv
from pathlib import Path
from books import Book
from member_basic import Member

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

BOOKS_FILE = DATA_DIR / "books.csv"
MEMBERS_FILE = DATA_DIR / "members.csv"


def save_books(books_dict):
    with BOOKS_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["book_id", "title", "author", "genre", "total_copies", "available_copies"])
        for book in books_dict.values():
            writer.writerow([
                book.book_id,
                book.title,
                book.author,
                book.genre,
                book.total_copies,
                book.available_copies,
            ])


def load_books():
    books = {}
    if not BOOKS_FILE.exists():
        return books

    with BOOKS_FILE.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            book = Book(
                book_id=row["book_id"],
                title=row["title"],
                author=row["author"],
                genre=row["genre"],
                copies=int(row["total_copies"]),
            )
            book._available_copies = int(row["available_copies"])
            books[book.book_id] = book
    return books


def save_members(members_dict):
    with MEMBERS_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["member_id", "name", "email", "max_books"])
        for m in members_dict.values():
            writer.writerow([
                m._member_id,
                m._name,
                m._email,
                m._max_books,
            ])


def load_members():
    members = {}
    if not MEMBERS_FILE.exists():
        return members

    with MEMBERS_FILE.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            member = Member(
                member_id=row["member_id"],
                name=row["name"],
                email=row["email"],
                max_books=int(row["max_books"]),
            )
            members[member._member_id] = member
    return members
