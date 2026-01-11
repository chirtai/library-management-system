from database.db_connection import db

def load_pending_users():
    users = db.execute_query("""
        SELECT user_id, username, full_name, email, created_at 
        FROM Users 
        WHERE status = 'PENDING'
    """, fetch=True)

    # Khi nhấn nút Duyệt:
    def approve_user(user_id):
        db.execute_query(
            "UPDATE Users SET status = 'ACTIVE' WHERE user_id = ?",
            (user_id,),
            commit=True
        )
        QMessageBox.information(self, "Thành công", "Đã duyệt tài khoản!")
        self.load_pending_users()  # reload danh sách