from models import Library, BookAlreadyExistsError
from storage import Storage
from gui import LibraryGUI


def main():
    storage = Storage()
    library = Library()

    loaded_books = storage.load_books()
    for book in loaded_books:
        try:
            library.add_book(book)
        except BookAlreadyExistsError:
            pass

    app = LibraryGUI(library, storage)
    app.mainloop()


if __name__ == "__main__":
    main()