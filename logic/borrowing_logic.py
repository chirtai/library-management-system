from database.db_connection import db
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple

class BorrowingLogic:
    FINE_PER_DAY = 5000  # ₫ per day late

    def __init__(self):
        self.db = db

    def get_current_borrows(self) -> List[Dict]:
        """Get list of currently borrowed books (not yet returned)"""
        query = """
        SELECT 
            b.borrow_id,
            bk.title,
            u.full_name,
            b.borrow_date,
            b.due_date,
            CASE 
                WHEN b.return_date IS NULL AND b.due_date < CAST(GETDATE() AS DATE) 
                THEN 'OVERDUE'
                ELSE 'BORROWED'
            END AS status
        FROM Borrowing b
        JOIN Books bk ON b.book_id = bk.book_id
        JOIN Users u ON b.user_id = u.user_id
        WHERE b.return_date IS NULL
        ORDER BY b.borrow_date DESC
        """
        results = self.db.execute_query(query, fetch=True)
        if not results:
            return []

        return [
            {
                "borrow_id": row[0],
                "title": row[1],
                "full_name": row[2],
                "borrow_date": row[3],
                "due_date": row[4],
                "status": row[5]
            }
            for row in results
        ]

    def get_borrowing_history(self) -> List[Dict]:
        """Get complete borrowing history with fines"""
        query = """
        SELECT 
            bk.title,
            u.full_name,
            b.borrow_date,
            b.return_date,
            DATEDIFF(DAY, b.due_date, b.return_date) AS days_late,
            ISNULL(f.amount, 0) AS fine,
            ISNULL(f.payment_status, 'UNPAID') AS paid
        FROM Borrowing b
        JOIN Books bk ON b.book_id = bk.book_id
        JOIN Users u ON b.user_id = u.user_id
        LEFT JOIN Fines f ON b.borrow_id = f.borrow_id
        WHERE b.return_date IS NOT NULL
        ORDER BY b.return_date DESC
        """
        results = self.db.execute_query(query, fetch=True)
        if not results:
            return []

        return [
            {
                "title": row[0],
                "full_name": row[1],
                "borrow_date": row[2],
                "return_date": row[3],
                "days_late": max(0, row[4] if row[4] else 0),
                "fine": float(row[5]) if row[5] else 0,
                "paid": row[6]
            }
            for row in results
        ]

    def get_book_title_by_id(self, book_id: int) -> Optional[str]:
        result = self.db.execute_query(
            "SELECT title FROM Books WHERE book_id = ?",
            (book_id,),
            fetch="one"
        )
        return result[0] if result else None

    def get_user_name_by_id(self, user_id: int) -> Optional[str]:
        result = self.db.execute_query(
            "SELECT full_name FROM Users WHERE user_id = ?",
            (user_id,),
            fetch="one"
        )
        return result[0] if result else None

    def borrow_book(self, user_id: int, book_id: int, borrow_days: int = 14) -> Tuple[bool, str]:
        """Create a new borrowing record - KHÔNG cần staff_id"""
        today = date.today()
        due_date = today + timedelta(days=borrow_days)

        # Check if book is already borrowed
        check_query = """
        SELECT borrow_id 
        FROM Borrowing 
        WHERE book_id = ? AND return_date IS NULL
        """
        exists = self.db.execute_query(check_query, (book_id,), fetch="one")
        if exists:
            return False, "This book is currently borrowed by someone else."

        # Check if user exists and is active
        user_check = """
        SELECT status FROM Users WHERE user_id = ?
        """
        user = self.db.execute_query(user_check, (user_id,), fetch="one")
        if not user:
            return False, "User not found."
        if user[0] != 'ACTIVE':
            return False, f"User account is {user[0]}. Cannot borrow."

        # Insert borrowing record - BỎ staff_id
        insert_query = """
        INSERT INTO Borrowing (user_id, book_id, borrow_date, due_date)
        VALUES (?, ?, ?, ?)
        """
        success = self.db.execute_query(
            insert_query,
            (user_id, book_id, today, due_date),
            commit=True
        )

        if success:
            return True, f"Book borrowed successfully. Due date: {due_date}"
        else:
            return False, "Failed to create borrowing record."

    def return_book(self, borrow_id: int) -> Tuple[bool, str, float]:
        """Process book return and calculate fine if applicable - BỎ staff_id"""
        today = date.today()

        # Get borrowing info
        query = """
        SELECT user_id, due_date, return_date 
        FROM Borrowing 
        WHERE borrow_id = ? AND return_date IS NULL
        """
        borrow = self.db.execute_query(query, (borrow_id,), fetch="one")
        if not borrow:
            return False, "Borrow record not found or already returned.", 0

        user_id, due_date, _ = borrow

        days_late = max(0, (today - due_date).days)
        fine_amount = days_late * self.FINE_PER_DAY

        # Update borrowing record - BỎ staff_id
        update_query = """
        UPDATE Borrowing 
        SET return_date = ?
        WHERE borrow_id = ?
        """
        success = self.db.execute_query(
            update_query,
            (today, borrow_id),
            commit=True
        )

        if not success:
            return False, "Failed to update return date.", 0

        if days_late > 0:
            fine_query = """
            INSERT INTO Fines (borrow_id, amount, reason, payment_status)
            VALUES (?, ?, ?, 'UNPAID')
            """
            self.db.execute_query(
                fine_query,
                (borrow_id, fine_amount, f"Late by {days_late} days"),
                commit=True
            )
            return True, f"Book returned. Late by {days_late} days. Fine: {fine_amount:,.0f} ₫", fine_amount
        else:
            return True, "Book returned on time. No fine.", 0