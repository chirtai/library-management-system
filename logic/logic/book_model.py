import pyodbc

class BookModel:
    def __init__(self):
        self.conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=localhost;"
            "DATABASE=LibraryManagement;"
            "Trusted_Connection=yes;"
        )

    def get_all_books(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                b.book_id,
                b.title,
                a.author_name,
                c.category_name,
                b.publisher,
                b.publish_year
            FROM Books b
            JOIN Authors a ON b.author_id = a.author_id
            JOIN Categories c ON b.category_id = c.category_id
            ORDER BY b.title
        """)

        rows = cursor.fetchall()
        return rows
