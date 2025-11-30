from mini_library_demo import Library
from books import Book
from member_basic import Member
from exceptions import (
    LibraryError,
    MemberNotFoundError,
    BookNotFoundError,
    BookNotAvailableError,
    BorrowLimitExceededError,
)


def print_menu():
    print("\n" + "=" * 40)
    print("📚 THE BOOK VAULT - MAIN MENU")
    print("=" * 40)
    print("1. Add new book")
    print("2. Register new member")
    print("3. Issue book")
    print("4. Return book")
    print("5. List all books")
    print("6. List all members")
    print("7. Save & Exit")
    print("=" * 40)


def main():
    library = Library("The Book Vault")

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            # Add book
            book_id = input("Book ID: ").strip()
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            genre = input("Genre: ").strip()
            copies = int(input("Total copies: ").strip() or "1")

            if library.get_book(book_id):
                print("⚠️ Book with this ID already exists.")
            else:
                book = Book(book_id, title, author, genre, copies)
                library.add_book(book)
                print("✅ Book added.")

        elif choice == "2":
            # Register member
            member_id = input("Member ID: ").strip()
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            max_books = int(input("Max books (default 5): ").strip() or "5")

            if library.get_member(member_id):
                print("⚠️ Member with this ID already exists.")
            else:
                member = Member(member_id, name, email, max_books)
                library.register_member(member)
                print("✅ Member registered.")

        elif choice == "3":
            # Issue book
            member_id = input("Member ID: ").strip()
            book_id = input("Book ID: ").strip()
            try:
                library.issue_book(member_id, book_id)
                print("✅ Book issued.")
            except BookNotAvailableError as e:
                print("❌", e)
            except BorrowLimitExceededError as e:
                print("❌", e)
            except (MemberNotFoundError, BookNotFoundError, LibraryError) as e:
                print("❌", e)

        elif choice == "4":
            # Return book
            member_id = input("Member ID: ").strip()
            book_id = input("Book ID: ").strip()
            try:
                library.return_book(member_id, book_id)
                print("✅ Book returned.")
            except (MemberNotFoundError, BookNotFoundError, LibraryError) as e:
                print("❌", e)

        elif choice == "5":
            # List books
            print("\n📚 Books in library:")
            library.list_books()

        elif choice == "6":
            # List members
            print("\n👥 Members in library:")
            library.list_members()

        elif choice == "7":
            # Save & Exit
            library.save_all()
            print("💾 Data saved. Goodbye!")
            break

        else:
            print("⚠️ Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()
