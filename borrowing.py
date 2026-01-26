from datetime import datetime, date
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QWidget
from PyQt6.QtCore import Qt

class BorrowingInterfaceLogic:
    def __init__(self, ui_instance):
        self.ui = ui_instance
        # KHO DỮ LIỆU (Book Database)
        self.book_db = {
            "B001": {"title": "Dế Mèn Phiêu Lưu Ký", "status": "Available"}, 
            "B002": {"title": "Sherlock Holmes", "status": "Borrowed"}
        }

    # DFD: Check book availability
    def check_availability(self, book_id):
        book = self.book_db.get(book_id)
        return book and book["status"] == "Available"

    # DFD: Create borrowing record
    def process_borrow_request(self, member_name, book_id):
        if not self.check_availability(book_id):
            QMessageBox.warning(self.ui, "Thông báo", "Sách không có sẵn!")
            return

        # DFD: Update book status (to Borrowed)
        self.book_db[book_id]["status"] = "Borrowed"
        
        borrow_date = date.today().strftime("%Y-%m-%d")
        due_date = "2026-02-10" 
        
        # DFD: Save borrowing record (Update UI)
        row = self.ui.current_table.rowCount()
        self.ui.current_table.insertRow(row)
        data = [book_id, self.book_db[book_id]["title"], member_name, borrow_date, due_date, "Borrowed"]
        for col, value in enumerate(data):
            self.ui.current_table.setItem(row, col, QTableWidgetItem(str(value)))
            
        QMessageBox.information(self.ui, "Thành công", f"Librarian đã duyệt mượn cho {member_name}")

    # DFD: Return book & Calculate fine
    def process_return_book(self, row_index, book_id, return_date_str):
        # Giả định hạn trả là ngày 20/01/2026
        due_date = date(2026, 1, 20)
        return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
        
        # DFD: Late days flow
        late_days = (return_date - due_date).days
        fine = 0
        if late_days > 0:
            # DFD: Calculate fine
            fine = late_days * 5000 
            
        # DFD: Fine payment request & Payment result
        paid_status = "N/A"
        if fine > 0:
            reply = QMessageBox.question(self.ui, "Thanh toán", 
                                       f"Trễ {late_days} ngày. Phạt: {fine} VNĐ. Đã thanh toán?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            paid_status = "Yes" if reply == QMessageBox.StandardButton.Yes else "No"

        # DFD: Update book status (Back to Available)
        if book_id in self.book_db:
            self.book_db[book_id]["status"] = "Available"

        # DFD: Borrowing info -> Update history / Fine status
        title = self.ui.current_table.item(row_index, 1).text()
        member = self.ui.current_table.item(row_index, 2).text()
        b_date = self.ui.current_table.item(row_index, 3).text()
        
        self.update_history_ui(title, member, b_date, return_date_str, late_days, f"{fine} VNĐ", paid_status)
        
        # Xóa khỏi bảng đang mượn
        self.ui.current_table.removeRow(row_index)

    def update_history_ui(self, title, member, b_date, r_date, late, fine, paid):
        row = self.ui.history_table.rowCount()
        self.ui.history_table.insertRow(row)
        data = [title, member, b_date, r_date, max(0, late), fine, paid]
        for col, value in enumerate(data):
            self.ui.history_table.setItem(row, col, QTableWidgetItem(str(value)))