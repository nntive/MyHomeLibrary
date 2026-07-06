import json
import os
from datetime import datetime
from models import Book


def log_action(action_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Executing system action: {action_name}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


class Storage:
    def __init__(self, filename="library.json"):
        self.folder = "Data"
        self.filepath = os.path.join(self.folder, filename)

        os.makedirs(self.folder, exist_ok=True)

    @log_action("save_books")
    def save_books(self, books):
        with open(self.filepath, "w", encoding="utf-8") as f:  #File I/O (JSON)
            json.dump([book.to_dict() for book in books], f, indent=4)  #File I/O (JSON) & Comprehensions

    @log_action("load_books")
    def load_books(self):
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as f:  #File I/O (JSON)
            try:
                data = json.load(f)  #File I/O (JSON)
                return [Book.from_dict(item) for item in data]
            except json.JSONDecodeError:
                return []