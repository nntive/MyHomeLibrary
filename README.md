# MyHomeLibrary 📚 + AI Predictor

A smart desktop application for managing a personal book collection, featuring an integrated Explainable AI (XAI) that predicts whether a specific user will enjoy a new book based on their unique reading history.

## 🚀 About The Project

This project goes beyond a simple CRUD application by implementing a custom Machine Learning algorithm (Single-layer Perceptron) from scratch. The AI uses **Sentiment Analysis** to evaluate past reading experiences and solves the "Cold Start Problem" by normalizing user ratings into a -1.0 to 1.0 scale. 

The application is built using the **MVC (Model-View-Controller)** architecture to ensure clean, maintainable, and scalable code.

### ✨ Key Features
* **Smart Library Management:** Add, delete, and edit book ratings with dynamic UI updates.
* **Explainable AI Predictor:** Not only predicts if a user (Artem or Sasha) will like a book but also explains *why* (e.g., "Positive impact from: Genre" or "Negative impact from: Author").
* **Dynamic Feature Generation:** The GUI automatically adapts to your history, generating checkboxes for new genres as they are added to the library.
* **Persistent Storage:** Safely stores all data locally using JSON, with an auto-generated `Data` directory.

---

## 🎓 PPY Project Grading Criteria Checklist

This project heavily utilizes advanced Python concepts to meet all course requirements:

1. **Object-Oriented Programming:** Implemented via `Book`, `Library`, `Storage`, and `BookPerceptron` classes with appropriate methods (`__init__`, `__str__`, `@classmethod`).
2. **Custom Exceptions:** `BookAlreadyExistsError` prevents duplicate entries in the library.
3. **File I/O:** `storage.py` handles reading from and writing to `Data/library.json` using the `json` module.
4. **Decorators:** `@log_action` in `storage.py` logs all file saving/loading operations to the console with timestamps.
5. **Generators:** The `genre_yielder` method in `gui.py` uses the `yield` keyword to dynamically iterate through historical book genres to populate the UI.
6. **Comprehensions:** Extensive use of List, Set, and Dict comprehensions (e.g., zero-weight initialization in the neural network, extracting checked genres).
7. **Lambda Functions:** Used for inline callbacks in the GUI (e.g., `command=lambda b=book: self.delete_book(b)`).
8. **Regular Expressions:** The `re` module enforces strict input validation (e.g., `^\d+(\.\d+)?$` for ratings).
9. **Graphical User Interface (GUI):** Built with `customtkinter` for a modern, dark-themed, and responsive user experience.
10. **Data Structures:** Effectively combines standard lists, dictionaries (for sentiment scoring), and sets (for unique genre extraction).
11. **Creativity/Algorithm:** A fully custom, zero-dependency perceptron model featuring dynamic feature extraction, sentiment analysis, and explainable AI logic.

---

## 📂 Project Structure

* `main.py` — The entry point of the application.
* `models.py` — Contains the data structures (`Book`, `Library`) and custom exceptions.
* `storage.py` — Handles data persistence (JSON) and logging decorators.
* `gui.py` — The visual interface built with CustomTkinter.
* `ai.py` — The mathematical brain of the app (