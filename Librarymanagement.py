import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create a Database and Tables
def create_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    year INTEGER,
                    quantity INTEGER)''')

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    book_id INTEGER,
                    issue_date TEXT,
                    return_date TEXT,
                    status TEXT)''')
    
    conn.commit()
    conn.close()

# Main Application Class
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")

        # Menu
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        # Books Menu
        books_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Books", menu=books_menu)
        books_menu.add_command(label="Add Book", command=self.add_book_window)
        books_menu.add_command(label="View Books", command=self.view_books_window)

        # Users Menu
        users_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Users", menu=users_menu)
        users_menu.add_command(label="Add User", command=self.add_user_window)
        users_menu.add_command(label="View Users", command=self.view_users_window)

        # Transactions Menu
        transactions_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Transactions", menu=transactions_menu)
        transactions_menu.add_command(label="Issue Book", command=self.issue_book_window)
        transactions_menu.add_command(label="Return Book", command=self.return_book_window)

    # Add Book Window
    def add_book_window(self):
        add_book_win = tk.Toplevel(self.root)
        add_book_win.title("Add Book")
        add_book_win.geometry("400x300")

        tk.Label(add_book_win, text="Title").pack()
        title_entry = tk.Entry(add_book_win)
        title_entry.pack()

        tk.Label(add_book_win, text="Author").pack()
        author_entry = tk.Entry(add_book_win)
        author_entry.pack()

        tk.Label(add_book_win, text="Year").pack()
        year_entry = tk.Entry(add_book_win)
        year_entry.pack()

        tk.Label(add_book_win, text="Quantity").pack()
        quantity_entry = tk.Entry(add_book_win)
        quantity_entry.pack()

        def save_book():
            title = title_entry.get()
            author = author_entry.get()
            year = year_entry.get()
            quantity = quantity_entry.get()

            if title and author and year.isdigit() and quantity.isdigit():
                conn = sqlite3.connect('library.db')
                c = conn.cursor()
                c.execute("INSERT INTO books (title, author, year, quantity) VALUES (?, ?, ?, ?)",
                          (title, author, int(year), int(quantity)))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Book Added Successfully!")
                add_book_win.destroy()
            else:
                messagebox.showerror("Error", "Please fill all fields correctly.")

        tk.Button(add_book_win, text="Save", command=save_book).pack()

    # View Books Window
    def view_books_window(self):
        view_books_win = tk.Toplevel(self.root)
        view_books_win.title("View Books")
        view_books_win.geometry("600x400")

        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM books")
        books = c.fetchall()
        conn.close()

        listbox = tk.Listbox(view_books_win, width=70, height=15)
        listbox.pack()

        for book in books:
            listbox.insert(tk.END, f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Year: {book[3]} | Quantity: {book[4]}")

    # Add User Window
    def add_user_window(self):
        add_user_win = tk.Toplevel(self.root)
        add_user_win.title("Add User")
        add_user_win.geometry("400x300")

        tk.Label(add_user_win, text="Name").pack()
        name_entry = tk.Entry(add_user_win)
        name_entry.pack()

        tk.Label(add_user_win, text="Email").pack()
        email_entry = tk.Entry(add_user_win)
        email_entry.pack()

        def save_user():
            name = name_entry.get()
            email = email_entry.get()

            if name and email:
                conn = sqlite3.connect('library.db')
                c = conn.cursor()
                c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "User Added Successfully!")
                add_user_win.destroy()
            else:
                messagebox.showerror("Error", "Please fill all fields.")

        tk.Button(add_user_win, text="Save", command=save_user).pack()

    # View Users Window
    def view_users_window(self):
        view_users_win = tk.Toplevel(self.root)
        view_users_win.title("View Users")
        view_users_win.geometry("600x400")

        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        conn.close()

        listbox = tk.Listbox(view_users_win, width=70, height=15)
        listbox.pack()

        for user in users:
            listbox.insert(tk.END, f"ID: {user[0]} | Name: {user[1]} | Email: {user[2]}")

    # Issue Book Window
    def issue_book_window(self):
        issue_book_win = tk.Toplevel(self.root)
        issue_book_win.title("Issue Book")
        issue_book_win.geometry("400x300")

        tk.Label(issue_book_win, text="User ID").pack()
        user_id_entry = tk.Entry(issue_book_win)
        user_id_entry.pack()

        tk.Label(issue_book_win, text="Book ID").pack()
        book_id_entry = tk.Entry(issue_book_win)
        book_id_entry.pack()

        tk.Label(issue_book_win, text="Issue Date (YYYY-MM-DD)").pack()
        issue_date_entry = tk.Entry(issue_book_win)
        issue_date_entry.pack()

        def issue_book():
            user_id = user_id_entry.get()
            book_id = book_id_entry.get()
            issue_date = issue_date_entry.get()

            if user_id.isdigit() and book_id.isdigit() and issue_date:
                conn = sqlite3.connect('library.db')
                c = conn.cursor()

                # Check if the book is available
                c.execute("SELECT quantity FROM books WHERE book_id=?", (book_id,))
                book = c.fetchone()

                if book and book[0] > 0:
                    c.execute("INSERT INTO transactions (user_id, book_id, issue_date, return_date, status) VALUES (?, ?, ?, NULL, 'issued')",
                              (user_id, book_id, issue_date))
                    c.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id=?", (book_id,))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Book Issued Successfully!")
                    issue_book_win.destroy()
                else:
                    messagebox.showerror("Error", "Book not available.")
            else:
                messagebox.showerror("Error", "Please fill all fields correctly.")

        tk.Button(issue_book_win, text="Issue", command=issue_book).pack()

    # Return Book Window
    def return_book_window(self):
        return_book_win = tk.Toplevel(self.root)
        return_book_win.title("Return Book")
        return_book_win.geometry("400x300")

        tk.Label(return_book_win, text="Transaction ID").pack()
        transaction_id_entry = tk.Entry(return_book_win)
        transaction_id_entry.pack()

        tk.Label(return_book_win, text="Return Date (YYYY-MM-DD)").pack()
        return_date_entry = tk.Entry(return_book_win)
        return_date_entry.pack()

        def return_book():
            transaction_id = transaction_id_entry.get()
            return_date = return_date_entry.get()

            if transaction_id.isdigit() and return_date:
                conn = sqlite3.connect('library.db')
                c = conn.cursor()

                c.execute("SELECT book_id FROM transactions WHERE transaction_id=? AND status='issued'", (transaction_id,))
                transaction = c.fetchone()

                if transaction:
                    c.execute("UPDATE transactions SET return_date=?, status='returned' WHERE transaction_id=?",
                              (return_date, transaction_id))
                    c.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id=?", (transaction[0],))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Book Returned Successfully!")
                    return_book_win.destroy()
                else:
                    messagebox.showerror("Error", "Invalid Transaction ID or Book Already Returned.")
            else:
                messagebox.showerror("Error", "Please fill all fields correctly.")

        tk.Button(return_book_win, text="Return", command=return_book).pack()

if __name__ == "__main__":
    create_db()
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
