class Book: #Object-Oriented Programming
    def __init__(self, title, author, pages, genre, reader, rating=0.0, is_read=False): #Object-Oriented Programming
        self.title = title
        self.author = author
        self.pages = pages
        self.genre = genre
        self.reader = reader
        self.rating = rating
        self.is_read = is_read

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "pages": self.pages,
            "genre": self.genre,
            "reader": self.reader,
            "rating": self.rating,
            "is_read": self.is_read
        }

    @classmethod #Object-Oriented Programming
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            author=data["author"],
            pages=data["pages"],
            genre=data["genre"],
            reader=data["reader"],
            rating=data["rating"],
            is_read=data["is_read"]
        )

    def __str__(self): #Object-Oriented Programming
        status = "Read" if self.is_read else "Unread"
        genre_str = ", ".join(self.genre) if isinstance(self.genre, list) else self.genre
        return f"{self.title} ({self.author}) - {status} [{self.rating}/10] 🎭 {genre_str}"


class Library: #Object-Oriented Programming
    def __init__(self): #Object-Oriented Programming
        self.books = []  #Data Structures

    def add_book(self, book: Book):
        if any(b.title.lower() == book.title.lower() for b in self.books):
            raise BookAlreadyExistsError(f"Book '{book.title}' already exists.")
        self.books.append(book)

    def get_all_books(self):
        return self.books

    def remove_book(self, book: Book):
        if book in self.books:
            self.books.remove(book)

class BookAlreadyExistsError(Exception):  #Custom Exceptions
    pass
