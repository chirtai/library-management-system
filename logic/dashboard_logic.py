from database.db_connection import db  

class DashboardLogic:
    def __init__(self):
        pass

    # ===== 1. SUMMARY CARDS (Lấy số thật từ các bảng) =====
    def get_summary_stats(self):
        # Truy vấn tổng số sách
        res_total = db.execute_query("SELECT COUNT(*) FROM Books", fetch=True)
        # Truy vấn sách đang được mượn
        res_borrowed = db.execute_query("SELECT COUNT(*) FROM Borrowing WHERE return_date IS NULL", fetch=True)
        # Truy vấn sách quá hạn (giả sử so với ngày hiện tại)
        res_overdue = db.execute_query("SELECT COUNT(*) FROM Borrowing WHERE due_date < GETDATE() AND return_date IS NULL", fetch=True)
        # Truy vấn tổng số thành viên
        res_members = db.execute_query("SELECT COUNT(*) FROM Users", fetch=True)
        # Truy vấn tổng tiền phạt chưa trả
        res_fines = db.execute_query("SELECT SUM(amount) FROM Fines WHERE payment_status = 'UNPAID'", fetch=True)

        return {
            "total_books": res_total[0][0] if res_total else 0,
            "borrowed": res_borrowed[0][0] if res_borrowed else 0,
            "overdue": res_overdue[0][0] if res_overdue else 0,
            "members": res_members[0][0] if res_members else 0,
            "available": (res_total[0][0] if res_total else 0) - (res_borrowed[0][0] if res_borrowed else 0),
            "fines": float(res_fines[0][0]) if res_fines and res_fines[0][0] else 0
        }

    # ===== 2. LINE CHART (Xu hướng mượn sách theo tháng) =====
    def get_borrowing_trends(self):
        # Lấy dữ liệu mượn sách theo tháng trong năm hiện tại
        query = """
            SELECT FORMAT(borrow_date, 'MMM') as Month, COUNT(*) as Count
            FROM Borrowing
            WHERE YEAR(borrow_date) = YEAR(GETDATE())
            GROUP BY FORMAT(borrow_date, 'MMM'), MONTH(borrow_date)
            ORDER BY MONTH(borrow_date)
        """
        rows = db.execute_query(query, fetch=True)
        
        if not rows: # Nếu chưa có data thì trả về list trống để biểu đồ không lỗi
            return {"months": ["Trống"], "values": [0]}

        return {
            "months": [row[0] for row in rows],
            "values": [row[1] for row in rows]
        }

    # ===== 3. BAR CHART (Sách theo thể loại) =====
    def get_books_by_category(self):
        # Join bảng Books và Categories để đếm
        query = """
            SELECT c.category_name, COUNT(b.book_id)
            FROM Categories c
            LEFT JOIN Books b ON c.category_id = b.category_id
            GROUP BY c.category_name
        """
        rows = db.execute_query(query, fetch=True)
        
        if not rows:
            return {"categories": ["Chưa có dữ liệu"], "values": [0]}

        return {
            "categories": [row[0] for row in rows],
            "values": [row[1] for row in rows]
        }
