import psycopg2
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import hashlib

# Database connection
def connect_db(dbname='postgres'):
    try:
        conn = psycopg2.connect(
            dbname="227480201IS003", 
            user="postgres", 
            password="1234", 
            host="localhost", 
            port='5432'
        )
        print(f"Connection to {dbname} successful")
        return conn
    except Exception as e:
        print(f"Error while connecting to database {dbname}:", e)
        raise

def create_database():
    try:
        conn = connect_db()
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("CREATE DATABASE books")
        cur.close()
        conn.close()
        print("Database 'books' created successfully")
    except psycopg2.errors.DuplicateDatabase:
        print("Database 'books' already exists")
    except Exception as e:
        print("Error creating database:", e)
        raise

def create_table(connection):
    if connection is None:
        messagebox.showerror("Database Error", "Unable to connect to the database")
        return
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                year INTEGER NOT NULL,
                genre VARCHAR(100) NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        """)
        connection.commit()
        print("Tables have been created successfully.")
    except Exception as e:
        print("Error while creating tables:", e)
        messagebox.showerror("Database Error", str(e))
    finally:
        if cursor:
            cursor.close()

# Add book to the database
def add_book():
    title = entry_title.get()
    author = entry_author.get()
    year = entry_year.get()
    genre = entry_genre.get()
    if not validate_input(title, author, year, genre):
        return
    try:
        conn = connect_db('books')
        cur = conn.cursor()
        cur.execute("INSERT INTO books (title, author, year, genre) VALUES (%s, %s, %s, %s)",
                    (title, author, int(year), genre))
        conn.commit()
        cur.close()
        conn.close()
        reload_books()
        clear_entries()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Update selected book
def update_book():
    try:
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a book to update.")
            return 
        book_id = tree.item(selected_item)['values'][0]
        title = entry_title.get()
        author = entry_author.get()
        year = entry_year.get()
        genre = entry_genre.get()
        if not validate_input(title, author, year, genre):
            return
        conn = connect_db('books')
        cur = conn.cursor()
        cur.execute("UPDATE books SET title=%s, author=%s, year=%s, genre=%s WHERE id=%s",
                    (title, author, int(year), genre, book_id))
        conn.commit()
        cur.close()
        conn.close()
        reload_books()
        clear_entries()
    except Exception as e:
        messagebox.showerror("Update Error", str(e))

# Delete selected book
def delete_book():
    try:
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a book to delete.")
            return
        book_id = tree.item(selected_item)['values'][0]
        conn = connect_db('books')
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id=%s", (book_id,))
        conn.commit()
        cur.close()
        conn.close()
        reload_books()
        clear_entries()
    except Exception as e:
        messagebox.showerror("Delete Error", str(e))

# Reload the book list from database
def reload_books():
    try:
        conn = connect_db('books')
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        
        # Clear existing data
        for row in tree.get_children():
            tree.delete(row)
        # Insert new data
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Load Error", str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Validate input fields
def validate_input(title, author, year, genre):
    if not title or not author or not year or not genre:
        messagebox.showwarning("Input Error", "All fields are required.")
        return False
    try:
        int(year)
    except ValueError:
        messagebox.showwarning("Input Error", "Year must be a number.")
        return False
    return True

# Clear entry fields
def clear_entries():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_genre.delete(0, tk.END)

# Login function
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        messagebox.showwarning("Login Error", "Username and password are required.")
        return
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        conn = connect_db('books')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user:
            messagebox.showinfo("Login Successful", "Welcome to the Library Management System!")
            login_frame.pack_forget()
            main_frame.pack(fill=tk.BOTH, expand=True)
        else:
            # If user doesn't exist, create a new account
            create_user(username, hashed_password)
            messagebox.showinfo("Account Created", "New account created. You can now log in.")
    except Exception as e:
        messagebox.showerror("Login Error", str(e))

# Create new user
def create_user(username, hashed_password):
    try:
        conn = connect_db('books')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Account Creation Error", str(e))

# Setup GUI
root = tk.Tk()
root.title("Library Management System")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

# Custom fonts
title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
button_font = tkfont.Font(family="Helvetica", size=10, weight="bold")

# Login Frame
login_frame = tk.Frame(root, bg="#f0f0f0")
login_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(login_frame, text="Library Management System", font=title_font, bg="#f0f0f0").pack(pady=20)

tk.Label(login_frame, text="Username:", bg="#f0f0f0").pack(pady=5)
entry_username = tk.Entry(login_frame, width=30)
entry_username.pack(pady=5)

tk.Label(login_frame, text="Password:", bg="#f0f0f0").pack(pady=5)
entry_password = tk.Entry(login_frame, show="*", width=30)
entry_password.pack(pady=5)

login_button = tk.Button(login_frame, text="Login", command=login, bg="#4CAF50", fg="white", font=button_font)
login_button.pack(pady=20)

# Main Frame
main_frame = tk.Frame(root, bg="#f0f0f0")

# Labels and entries
tk.Label(main_frame, text="Tên sách:", bg="#f0f0f0").grid(row=0, column=0, padx=(10,2), pady=5, sticky="e")
entry_title = tk.Entry(main_frame, width=30)
entry_title.grid(row=0, column=1, padx=(2,10), pady=5, sticky="w")

tk.Label(main_frame, text="Tác giả:", bg="#f0f0f0").grid(row=1, column=0, padx=(10,2), pady=5, sticky="e")
entry_author = tk.Entry(main_frame, width=30)
entry_author.grid(row=1, column=1, padx=(2,10), pady=5, sticky="w")

tk.Label(main_frame, text="Năm XB:", bg="#f0f0f0").grid(row=2, column=0, padx=(10,2), pady=5, sticky="e")
entry_year = tk.Entry(main_frame, width=30)
entry_year.grid(row=2, column=1, padx=(2,10), pady=5, sticky="w")

tk.Label(main_frame, text="Thể loại:", bg="#f0f0f0").grid(row=3, column=0, padx=(10,2), pady=5, sticky="e")
entry_genre = tk.Entry(main_frame, width=30)
entry_genre.grid(row=3, column=1, padx=(2,10), pady=5, sticky="w")

# Buttons
button_frame = tk.Frame(main_frame, bg="#f0f0f0")
button_frame.grid(row=4, column=0, columnspan=2, pady=10)

add_button = tk.Button(button_frame, text="Thêm sách", command=add_book, bg="#2196F3", fg="white", font=button_font)
add_button.pack(side=tk.LEFT, padx=5)

update_button = tk.Button(button_frame, text="Cập nhật", command=update_book, bg="#FF9800", fg="white", font=button_font)
update_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(button_frame, text="Xóa sách", command=delete_book, bg="#f44336", fg="white", font=button_font)
delete_button.pack(side=tk.LEFT, padx=5)

reload_button = tk.Button(button_frame, text="Tải lại DS", command=reload_books, bg="#4CAF50", fg="white", font=button_font)
reload_button.pack(side=tk.LEFT, padx=5)

# Treeview for book list
columns = ("ID", "Tên sách", "Tác giả", "Năm XB", "Thể loại")
tree = ttk.Treeview(main_frame, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Tên sách", text="Tên sách")
tree.heading("Tác giả", text="Tác giả")
tree.heading("Năm XB", text="Năm XB")
tree.heading("Thể loại", text="Thể loại")
tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
# Configure grid weights
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(5, weight=1)

# Scrollbar for Treeview
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
scrollbar.grid(row=5, column=2, sticky="ns")
tree.configure(yscrollcommand=scrollbar.set)

try:
    connection = connect_db('books')
    if connection:
        create_table(connection)
        connection.close()
except Exception as e:
    messagebox.showerror("Database Error", f"Unable to setup the database: {str(e)}")
    root.quit()

# Start with a load of books
reload_books()

# Run the application
root.mainloop()
