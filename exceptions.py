class LibraryError(Exception):
    """Base class for library-related errors."""
    pass


class MemberNotFoundError(LibraryError):
    pass


class BookNotFoundError(LibraryError):
    pass


class BookNotAvailableError(LibraryError):
    pass


class BorrowLimitExceededError(LibraryError):
    pass
