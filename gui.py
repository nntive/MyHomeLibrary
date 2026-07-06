import customtkinter as ctk
import re
from tkinter import messagebox
from models import Book, BookAlreadyExistsError
from ai import BookPerceptron, extract_features

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class LibraryGUI(ctk.CTk):  #Object-Oriented Programming and Graphical User Interface
    def __init__(self, library, storage):  #Object-Oriented Programming
        super().__init__()

        self.library = library
        self.storage = storage

        self.title("MyHomeLibrary 📚 + AI Prediction")
        self.geometry("900x650")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="MyHomeLibrary",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        self.btn_add = ctk.CTkButton(self.sidebar_frame, text="Add Book", command=self.show_add_frame)
        self.btn_add.grid(row=1, column=0, padx=20, pady=10)

        self.btn_list = ctk.CTkButton(self.sidebar_frame, text="My Books", command=self.show_list_frame)
        self.btn_list.grid(row=2, column=0, padx=20, pady=10)

        self.btn_ai = ctk.CTkButton(self.sidebar_frame, text="AI Predictor", command=self.show_ai_frame)
        self.btn_ai.grid(row=3, column=0, padx=20, pady=10)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.welcome_label = ctk.CTkLabel(self.main_frame,
                                          text="Welcome to your Library!\nSelect an action from the menu.",
                                          font=ctk.CTkFont(size=18))
        self.welcome_label.grid(row=0, column=0, pady=200)

    def get_dynamic_genres(self):
        def genre_yielder():  #Generators
            for book in self.library.get_all_books():
                if isinstance(book.genre, list):
                    for g in book.genre:
                        yield g

        unique_genres = {
            "Sci-Fi", "Fantasy", "Romance", "Detective", "Thriller",
            "Mystery", "Horror", "Adventure", "Drama", "Dystopian",
            "Historical Fiction", "Biography", "Self-Help"
        }  #Data Structures

        for g in genre_yielder():
            unique_genres.add(g.capitalize())

        return sorted(list(unique_genres))

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_add_frame(self):
        self.clear_main_frame()

        title_label = ctk.CTkLabel(self.main_frame, text="Add a New Book", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 10))

        self.entry_title = ctk.CTkEntry(self.main_frame, placeholder_text="Book Title", width=300)
        self.entry_title.pack(pady=10)

        self.entry_author = ctk.CTkEntry(self.main_frame, placeholder_text="Author", width=300)
        self.entry_author.pack(pady=10)

        self.entry_pages = ctk.CTkEntry(self.main_frame, placeholder_text="Number of Pages", width=300)
        self.entry_pages.pack(pady=10)

        genre_label = ctk.CTkLabel(self.main_frame, text="Select Genres:", font=ctk.CTkFont(size=14))
        genre_label.pack(pady=(10, 0))

        self.genre_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.genre_frame.pack(pady=5)

        available_genres = self.get_dynamic_genres()

        self.genre_vars = {}
        row, col = 0, 0
        for g in available_genres:
            var = ctk.BooleanVar(value=False)
            self.genre_vars[g] = var
            chk = ctk.CTkCheckBox(self.genre_frame, text=g, variable=var, width=120)
            chk.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.entry_custom_genre = ctk.CTkEntry(self.main_frame, placeholder_text="Or type a new genre (e.g. Drama)",
                                               width=300)
        self.entry_custom_genre.pack(pady=5)

        self.reader_var = ctk.StringVar(value="Artem")
        self.dropdown_reader = ctk.CTkOptionMenu(self.main_frame, values=["Artem", "Sasha"], variable=self.reader_var,
                                                 width=300)
        self.dropdown_reader.pack(pady=10)

        self.entry_rating = ctk.CTkEntry(self.main_frame, placeholder_text="Rating (0.0 to 10.0)", width=300)
        self.entry_rating.pack(pady=10)

        self.is_read_var = ctk.BooleanVar(value=True)
        self.checkbox_read = ctk.CTkCheckBox(self.main_frame, text="Already Read?", variable=self.is_read_var)
        self.checkbox_read.pack(pady=10)

        btn_save = ctk.CTkButton(self.main_frame, text="Save Book", command=self.save_new_book, fg_color="#27ae60",
                                 hover_color="#2ecc71")
        btn_save.pack(pady=20)

    def save_new_book(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        pages_text = self.entry_pages.get()
        reader = self.reader_var.get()
        rating_text = self.entry_rating.get()
        is_read = self.is_read_var.get()

        genre = [g for g, var in self.genre_vars.items() if var.get()]  #Comprehensions
        custom_genre = self.entry_custom_genre.get().strip()
        if custom_genre:
            genre.append(custom_genre.capitalize())

        if not title or not author:
            messagebox.showerror("Error", "Please fill in title and author!")
            return

        if not genre:
            messagebox.showerror("Error", "Please select or type at least one genre!")
            return

        if not re.match(r'^\d+$', pages_text):  #Regular Expressions
            messagebox.showerror("Regex Error", "Pages must contain ONLY numbers!")
            return

        if not re.match(r'^\d+(\.\d+)?$', rating_text):  #Regular Expressions
            messagebox.showerror("Regex Error", "Rating must be a number (e.g., 8 or 8.5)!")
            return

        rating = float(rating_text)
        if not (0.0 <= rating <= 10.0):
            messagebox.showerror("Error", "Rating must be between 0.0 and 10.0!")
            return

        pages = int(pages_text)
        new_book = Book(title, author, pages, genre, reader, rating, is_read)

        try:
            self.library.add_book(new_book)
            self.storage.save_books(self.library.get_all_books())
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")
            self.show_add_frame()
        except BookAlreadyExistsError as e:
            messagebox.showerror("Error", str(e))

    def show_list_frame(self):
        self.clear_main_frame()

        title_label = ctk.CTkLabel(self.main_frame, text="My Books Collection",
                                   font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 10))

        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, width=600, height=450)
        self.scrollable_frame.pack(pady=10, fill="both", expand=True)

        books = self.library.get_all_books()

        if not books:
            empty_label = ctk.CTkLabel(self.scrollable_frame, text="Your library is empty.")
            empty_label.pack(pady=20)
            return

        for book in books:
            book_frame = ctk.CTkFrame(self.scrollable_frame)
            book_frame.pack(pady=5, padx=10, fill="x")

            genre_display = ", ".join(book.genre) if isinstance(book.genre, list) else book.genre
            info_text = f"📖 {book.title} | ✍️ {book.author} | 🎭 {genre_display} | ⭐ {book.rating}/10 ({book.reader})"
            lbl_info = ctk.CTkLabel(book_frame, text=info_text, font=ctk.CTkFont(size=14))
            lbl_info.pack(side="left", padx=10, pady=10)

            btn_delete = ctk.CTkButton(book_frame, text="Delete", width=60, fg_color="#c0392b", hover_color="#e74c3c",
                                       command=lambda b=book: self.delete_book(b))  #Lambda Functions
            btn_delete.pack(side="right", padx=10, pady=10)

            btn_edit = ctk.CTkButton(book_frame, text="Edit Rating", width=80, fg_color="#f39c12",
                                     hover_color="#e67e22", command=lambda b=book: self.edit_rating(b))  #Lambda Functions
            btn_edit.pack(side="right", padx=10, pady=10)

    def delete_book(self, book):
        self.library.remove_book(book)
        self.storage.save_books(self.library.get_all_books())
        self.show_list_frame()

    def edit_rating(self, book):
        dialog = ctk.CTkInputDialog(text=f"Enter new rating for '{book.title}' (0.0 - 10.0):", title="Edit Rating")
        new_rating = dialog.get_input()

        if new_rating:
            if re.match(r'^\d+(\.\d+)?$', new_rating): #Regular Expressions
                rating_val = float(new_rating)
                if 0.0 <= rating_val <= 10.0:
                    book.rating = rating_val
                    self.storage.save_books(self.library.get_all_books())
                    self.show_list_frame()
                else:
                    messagebox.showerror("Error", "Rating must be between 0.0 and 10.0!")
            else:
                messagebox.showerror("Regex Error", "Invalid format! Use numbers (e.g., 8.5)")

    def show_ai_frame(self):
        self.clear_main_frame()

        title_label = ctk.CTkLabel(self.main_frame, text="AI Book Predictor", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 10))

        self.ai_target_reader = ctk.StringVar(value="Artem")
        reader_dropdown = ctk.CTkOptionMenu(self.main_frame, values=["Artem", "Sasha"], variable=self.ai_target_reader,
                                            width=300)
        reader_dropdown.pack(pady=10)

        self.ai_title = ctk.CTkEntry(self.main_frame, placeholder_text="Book Title", width=300)
        self.ai_title.pack(pady=10)
        self.ai_author = ctk.CTkEntry(self.main_frame, placeholder_text="Author", width=300)
        self.ai_author.pack(pady=10)
        self.ai_pages = ctk.CTkEntry(self.main_frame, placeholder_text="Pages", width=300)
        self.ai_pages.pack(pady=10)

        genre_label = ctk.CTkLabel(self.main_frame, text="Select Genres:", font=ctk.CTkFont(size=14))
        genre_label.pack(pady=(10, 0))

        self.ai_genre_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.ai_genre_frame.pack(pady=5)

        available_genres = self.get_dynamic_genres()

        self.ai_genre_vars = {}
        row, col = 0, 0
        for g in available_genres:
            var = ctk.BooleanVar(value=False)
            self.ai_genre_vars[g] = var
            chk = ctk.CTkCheckBox(self.ai_genre_frame, text=g, variable=var, width=120)
            chk.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.ai_entry_custom_genre = ctk.CTkEntry(self.main_frame, placeholder_text="Or type a new genre (e.g. Horror)",
                                                  width=300)
        self.ai_entry_custom_genre.pack(pady=5)

        btn_predict = ctk.CTkButton(self.main_frame, text="Ask AI 🤖", command=self.run_prediction, fg_color="#8e44ad",
                                    hover_color="#9b59b6")
        btn_predict.pack(pady=20)

        self.lbl_result = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_result.pack(pady=5)

        self.lbl_reason = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=14))
        self.lbl_reason.pack(pady=5)

    def run_prediction(self):
        pages_text = self.ai_pages.get()
        target_reader = self.ai_target_reader.get()

        ai_genre = [g for g, var in self.ai_genre_vars.items() if var.get()]
        custom_ai_genre = self.ai_entry_custom_genre.get().strip()
        if custom_ai_genre:
            ai_genre.append(custom_ai_genre.capitalize())

        if not ai_genre:
            messagebox.showerror("Error", "Please select or type at least one genre!")
            return

        if not re.match(r'^\d+$', pages_text):
            messagebox.showerror("Error", "Pages must be a number!")
            return

        target_books = [b for b in self.library.get_all_books() if b.reader == target_reader and b.is_read]

        if len(target_books) < 2:
            messagebox.showwarning("Warning", f"Not enough data for '{target_reader}'! Add at least 2 read books.")
            return

        genre_scores = {} #Data Structures
        author_scores = {} #Data Structures
        genre_counts = {} #Data Structures
        author_counts = {} #Data Structures

        for b in target_books:
            sentiment_score = (b.rating - 5.5) / 4.5

            if isinstance(b.genre, list):
                for g in b.genre:
                    g_lower = g.lower()
                    genre_scores[g_lower] = genre_scores.get(g_lower, 0.0) + sentiment_score
                    genre_counts[g_lower] = genre_counts.get(g_lower, 0) + 1

            a_lower = b.author.lower()
            author_scores[a_lower] = author_scores.get(a_lower, 0.0) + sentiment_score
            author_counts[a_lower] = author_counts.get(a_lower, 0) + 1

        for g in genre_scores:
            genre_scores[g] /= genre_counts[g]
        for a in author_scores:
            author_scores[a] /= author_counts[a]

        training_data = []
        targets = []

        for b in target_books:
            training_data.append(extract_features(b, genre_scores, author_scores))
            targets.append(1 if b.rating >= 6.0 else 0)

        ai = BookPerceptron(num_features=3)
        ai.train(training_data, targets, epochs=100)

        test_book = Book(
            title=self.ai_title.get(),
            author=self.ai_author.get(),
            pages=int(pages_text),
            genre=ai_genre,
            reader=target_reader
        )
        test_features = extract_features(test_book, genre_scores, author_scores)

        feature_names = ["Number of Pages", "Genre", "Author"]

        prediction, dominant_feature = ai.get_explanation(test_features, feature_names)

        if prediction == 1:
            self.lbl_result.configure(text=f"🟢 {target_reader} WILL LIKE IT!", text_color="#2ecc71")
            self.lbl_reason.configure(text=f"Why? Positive impact from: {dominant_feature}.", text_color="white")
        else:
            self.lbl_result.configure(text=f"🔴 NOT A GOOD FIT FOR {target_reader.upper()}.", text_color="#e74c3c")
            self.lbl_reason.configure(text=f"Why? Negative impact from: {dominant_feature.lower()}.",
                                      text_color="#bdc3c7")