import sqlite3

def create_db():
    # Connect to database (creates it if not exists)
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # 1. Create Students Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        branch TEXT,
        role TEXT
    )
    ''')

    # 2. Create Books Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        borrowed_by_id INTEGER
    )
    ''')

    # --- ADD SAMPLE DATA ---
    
    # Check if data exists, if not, add it
    cursor.execute("SELECT count(*) FROM students")
    if cursor.fetchone()[0] == 0:
        print("Adding sample students...")
        # NOTE: The ID here matches the Face ID you trained!
        # ID 1 = Rushal (Student)
        # ID 2 = The Librarian (Admin)
        cursor.execute("INSERT INTO students (id, name, branch, role) VALUES (1, 'Rushal', 'AI & DS', 'Student')")
        cursor.execute("INSERT INTO students (id, name, branch, role) VALUES (2, 'Ms. Admin', 'Staff', 'Librarian')")
        cursor.execute("INSERT INTO students (id, name, branch, role) VALUES (3, 'Rahul', 'CS', 'Student')")

    # Add some sample books
    cursor.execute("SELECT count(*) FROM books")
    if cursor.fetchone()[0] == 0:
        print("Adding sample books...")
        cursor.execute("INSERT INTO books (title, author, borrowed_by_id) VALUES ('Python Basics', 'Guido van Rossum', 1)")
        cursor.execute("INSERT INTO books (title, author, borrowed_by_id) VALUES ('Intro to AI', 'Andrew Ng', 0)") # 0 means available
        cursor.execute("INSERT INTO books (title, author, borrowed_by_id) VALUES ('Data Science 101', 'OReilly', 0)")

    conn.commit()
    conn.close()
    print("Database 'library.db' created successfully!")

if __name__ == "__main__":
    create_db()