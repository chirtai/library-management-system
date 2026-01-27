import pyodbc
from database.db_connection import db
from typing import List, Dict, Optional, Tuple

class BookLogic:
    @staticmethod
    def get_all_books() -> List[Dict]:
        query = """
            SELECT 
                b.book_id,
                b.title,
                ISNULL(a.name, N'No Author') AS author_name,
                ISNULL(c.name, N'No Category') AS category_name,
                b.publisher,
                b.publish_year
            FROM Books b
            LEFT JOIN Authors a ON b.author_id = a.author_id
            LEFT JOIN Categories c ON b.category_id = c.category_id
            ORDER BY b.title
            """
        results = db.execute_query(query, fetch="all")
        if not results:
            return []

        return [
            {
                "book_id": row[0],
                "title": row[1],
                "author": row[2],
                "category": row[3],
                "publisher": row[4],
                "publish_year": row[5]
            }
            for row in results
        ]

    @staticmethod
    def add_book(data: Dict) -> Tuple[bool, str]:
        title = data.get("title", "").strip()
        if not title:
            return False, "Title is required"

        try:
            year = int(data.get("year", 0)) if str(data.get("year", "")).isdigit() else None
        except ValueError:
            return False, "Year is required"

        query = """
            INSERT INTO Books 
            (title, author_id, category_id, publisher, publish_year)
            VALUES (?, ?, ?, ?, ?)
            """
        params = (
            title,
            1,
            1,
            data.get("publisher", "").strip(),
            year
        )

        success = db.execute_query(query, params, commit=True)
        return success, "Book Added" if success else "Failed"

    @staticmethod
    def update_book(book_id: int, data: Dict) -> Tuple[bool, str]:
        fields = []
        params = []

        if "title" in data and data["title"].strip():
            fields.append("title = ?")
            params.append(data["title"].strip())

        if "publisher" in data:
            fields.append("publisher = ?")
            params.append(data["publisher"].strip())

        if "year" in data:
            try:
                year = int(data["year"]) if str(data["year"]).isdigit() else None
                fields.append("publish_year = ?")
                params.append(year)
            except:
                return False, "Invalid year"

        if not fields:
            return False, "No fields to update"

        query = f"""
                UPDATE Books 
                SET {', '.join(fields)}
                WHERE book_id = ?
            """
        params.append(book_id)

        success = db.execute_query(query, tuple(params), commit=True)
        return success, "Success" if success else "Failed"

    @staticmethod
    def delete_book(book_id: int) -> Tuple[bool, str]:
        query = "DELETE FROM Books WHERE book_id = ?"
        success = db.execute_query(query, (book_id,), commit=True)
        return success, "Deleted" if success else "Failed"