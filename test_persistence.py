from mini_library_demo import Library
from member_basic import Member
from books import Book

def main():
    # 1) First run: create library, add stuff, save
    lib = Library("Test Library")

    print("Loaded books:", len(lib._books))
    print("Loaded members:", len(lib._members))

    # Only add if not already present
    if "B100" not in lib._books:
        b = Book("B100", "Test Book", "Test Author", "Test", copies=3)
        lib.add_book(b)

    if "M100" not in lib._members:
        m = Member("M100", "Test User", "test@example.com", max_books=2)
        lib.register_member(m)

    lib.save_all()
    print("Saved. Now reloading...")

    # 2) New Library instance to test loading
    lib2 = Library("Test Library Reloaded")
    print("Reloaded books:", len(lib2._books))
    print("Reloaded members:", len(lib2._members))

    print("\nSearch test:")
    results = lib2.search_books("test")
    for book in results:
        print("-", book)

    print("\nStats:")
    stats = lib2.stats()
    for k, v in stats.items():
        print(k, ":", v)

    # Check if our test IDs exist
    print("Has B100?", "B100" in lib2._books)
    print("Has M100?", "M100" in lib2._members)

if __name__ == "__main__":
    main()
