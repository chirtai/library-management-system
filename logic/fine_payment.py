from database.db_connection import db
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem,QPushButton
from PyQt6.QtCore import Qt
from datetime import datetime
import math
import random

class FinesController:
    def __init__(self, ui_instance):
        self.ui = ui_instance

    def load_data(self):
        self.ui.table.setShowGrid(True)
        self.ui.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0; /* Màu xám rõ rệt cho dòng kẻ */
                border: none;
            }
            QTableWidget::item {
                border-bottom: 1px solid #d0d0d0; /* Vẽ dòng kẻ ngang thủ công */
                padding: 5px;
            }
        """)

        

        """Truy vấn dữ liệu từ SQL và đổ vào bảng QTableWidget"""
        # Câu lệnh SQL kết hợp 3 bảng để lấy tên thành viên
        query = """
            SELECT 
                f.fine_id, 
                u.user_id   , 
                f.borrow_id, 
                f.amount, 
                f.reason, 
                f.payment_status
            FROM Fines f
            JOIN Borrowing b ON f.borrow_id = b.borrow_id
            JOIN Users u ON b.user_id = u.user_id
        """
        # Thực hiện truy vấn qua đối tượng db
        rows = db.execute_query(query, fetch=True)
        
        # Xóa dữ liệu cũ trên bảng giao diện
        self.ui.table.setRowCount(0)
        
        if rows:
            for row_idx, row_data in enumerate(rows):
                self.ui.table.insertRow(row_idx)
                self.ui.table.setRowHeight(row_idx, 60)
                for col_idx, value in enumerate(row_data):
                    # Hiển thị dữ liệu dạng văn bản vào từng ô
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.ui.table.setItem(row_idx, col_idx, item)
                
                # Logic hiển thị nút "Thanh toán" ở cột cuối cùng
                status = row_data[5] # Cột payment_status
                if status == 'UNPAID':
                    btn_pay = QPushButton("Thanh toán")
                    btn_pay.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 3px;")
                    # Kết nối nút Pay với hàm xử lý thanh toán
                    btn_pay.clicked.connect(lambda _, r=row_idx: self.handle_payment(r))
                    self.ui.table.setCellWidget(row_idx, 6, btn_pay)
                else:
                    paid_item = QTableWidgetItem("Đã xong")
                    paid_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.ui.table.setItem(row_idx, 6, paid_item)

    def add_fine(self):
        """Thêm mới phiếu phạt dựa trên dữ liệu từ Form"""
        borrow_id = self.ui.txt_borrow_id.text()
        amount = self.ui.txt_amount.text()
        reason = self.ui.txt_reason.text()
        status = self.ui.cb_status.currentText()

        if not borrow_id or not amount:
            QMessageBox.warning(self.ui, "Lỗi", "Vui lòng nhập Borrow ID và Số tiền!")
            return

        query = "INSERT INTO Fines (borrow_id, amount, reason, payment_status) VALUES (?, ?, ?, ?)"
        success = db.execute_query(query, (borrow_id, amount, reason, status), commit=True)
        
        if success:
            QMessageBox.information(self.ui, "Thành công", "Đã thêm phiếu phạt!")
            self.load_data()
            self.clear_form()
        else:
            QMessageBox.critical(self.ui, "Lỗi", "Không thể thêm. Hãy kiểm tra lại Borrow ID!")

    def update_fine(self):
        """Cập nhật phiếu phạt đang được chọn"""
        selected_row = self.ui.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self.ui, "Thông báo", "Vui lòng chọn một dòng để sửa!")
            return

        fine_id = self.ui.table.item(selected_row, 0).text()
        query = "UPDATE Fines SET amount = ?, reason = ?, payment_status = ? WHERE fine_id = ?"
        params = (self.ui.txt_amount.text(), self.ui.txt_reason.text(), self.ui.cb_status.currentText(), fine_id)
        
        if db.execute_query(query, params, commit=True):
            QMessageBox.information(self.ui, "Thành công", "Đã cập nhật dữ liệu!")
            self.load_data()

    def delete_fine(self):
        """Xóa phiếu phạt dựa trên Fine ID"""
        selected_row = self.ui.table.currentRow()
        if selected_row >= 0:
            fine_id = self.ui.table.item(selected_row, 0).text()
            confirm = QMessageBox.question(self.ui, "Xác nhận", f"Xóa phiếu phạt {fine_id}?", 
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if confirm == QMessageBox.StandardButton.Yes:
                db.execute_query("DELETE FROM Fines WHERE fine_id = ?", (fine_id,), commit=True)
                self.load_data()
                self.clear_form()

    def clear_form(self):
        """Làm trống các ô nhập liệu"""
        self.ui.txt_borrow_id.clear()
        self.ui.txt_borrow_id.setReadOnly(False)
        self.ui.txt_amount.clear()
        self.ui.txt_reason.clear()
        self.ui.cb_status.setCurrentIndex(0)


class PaymentsController:
    def __init__(self, ui_instance):
        self.ui = ui_instance
        button_qss = """
            QPushButton {
                border-radius: 6px;
                padding: 8px;
                color: white;
                font-weight: bold;
                border: none;
            }
            /* Nút Xác nhận (Xanh lá) */
            QPushButton#btn_pay { background-color: #28a745; }
            QPushButton#btn_pay:hover { background-color: #218838; }
            QPushButton#btn_pay:pressed { background-color: #1e7e34; }

            /* Nút Xóa (Đỏ) */
            QPushButton#btn_delete { background-color: #dc3545; }
            QPushButton#btn_delete:hover { background-color: #c82333; }

            /* Nút Kiểm tra (Xanh đen/Xám) */
            QPushButton#btn_check { background-color: #34495e; }
            QPushButton#btn_check:hover { background-color: #2c3e50; }
        """
        self.ui.btn_pay.setStyleSheet(button_qss)
        self.ui.btn_delete.setStyleSheet(button_qss)
        # Nếu nút kiểm tra có tên là btn_check_info hoặc tương tự:
        if hasattr(self.ui, 'btn_check'): 
            self.ui.btn_check.setStyleSheet(button_qss)

    def check_staff_exists(self, staff_id):
        """Kiểm tra xem Staff ID có tồn tại trong bảng Users không"""
        query = "SELECT full_name FROM Users WHERE user_id = ?"
        # Sử dụng db.execute_query từ file db_connection của bạn
        result = db.execute_query(query, (staff_id,), fetch="one")
        return result[0] if result else None
    
    def check_borrow_info(self):
        """Kiểm tra thông tin và tự động điền các ô nhập liệu"""
        borrow_id = self.ui.txt_borrow_id.text()
        if not borrow_id:
            QMessageBox.warning(self.ui, "Lỗi", "Vui lòng nhập Mã mượn!")
            return

        # 1. Lấy thông tin từ bảng BorrowingRecords
        query_borrow = "SELECT user_id, borrow_date, due_date FROM Borrowing WHERE borrow_id = ?"
        borrow_data = db.execute_query(query_borrow, (borrow_id,), fetch="one")

        if borrow_data:
            user_id, b_date, d_date = borrow_data

            # 2. Tính tiền mượn sách gốc = (due_date - borrow_date) * 10000
            # Lưu ý: d_date và b_date là kiểu date/datetime từ SQL Server
            delta = d_date - b_date
            total_days = max(0, delta.days) # Không tính ngày âm nếu trả sớm
            periods = math.ceil(total_days / 2) if total_days > 0 else 0
            base_fee = periods * 10000
            self.ui.txt_base_fee.setText(str(base_fee))

            # 3. Kiểm tra xem có phiếu phạt (Fine) nào cho mã mượn này không
            query_fine = "SELECT fine_id, amount FROM Fines WHERE borrow_id = ? AND payment_status = 'UNPAID'"
            fine_data = db.execute_query(query_fine, (borrow_id,), fetch="one")

            fine_amt = 0

            if fine_data:
                fine_id, fine_amt = fine_data
                self.ui.txt_fine_id.setText(str(fine_id))
                current_fine_amt = float(fine_amt)
                self.ui.txt_fine_amount.setText(str(current_fine_amt))
                total = base_fee + current_fine_amt
            else:
                self.ui.txt_fine_id.clear()
                self.ui.txt_fine_amount.setText("0")
                total = base_fee

            self.ui.txt_total_pay.setText(str(total))
        else:
            QMessageBox.critical(self.ui, "Lỗi", "Không tìm thấy Mã mượn này!")

    def process_payment(self):
        """Xác nhận thanh toán và cập nhật trạng thái Fine"""
        borrow_id = self.ui.txt_borrow_id.text().strip()
        fine_id = self.ui.txt_fine_id.text().strip()
        total_amount = self.ui.txt_total_pay.text().strip()
        method = self.ui.cb_method.currentText()
        staff_id = self.ui.txt_staff_id.text().strip()

        if not staff_id or not total_amount:
            QMessageBox.warning(self.ui, "Lỗi", "Chưa có thông tin thanh toán!")
            return
           
        try:

            if fine_id:
                check_query = "SELECT payment_id FROM Payments WHERE fine_id = ?"
                exists = db.execute_query(check_query, (fine_id,), fetch="one")
            else:
                # Đối với thanh toán gốc (không phạt), kiểm tra xem borrow_id này đã trả tiền chưa
                check_query = "SELECT payment_id FROM Payments WHERE borrow_id = ? AND fine_id IS NULL"
                exists = db.execute_query(check_query, (borrow_id,), fetch="one")

            if exists:
                QMessageBox.warning(self.ui, "Thông báo", f"Giao dịch cho Mã mượn {borrow_id} đã tồn tại trong lịch sử!")
                return # Dừng thực hiện nếu đã tồn tại

            staff_id = int(staff_id)
            staff_name = self.check_staff_exists(staff_id)
            if not staff_name:
                QMessageBox.critical(self.ui, "Lỗi xác thực",
                                     f"Nhân viên có ID {staff_id} không tồn tại trong hệ thống!")
                return
        
            f_id = int(fine_id) if fine_id else None
            trans_no = f"PAY{random.randint(1000, 9999)}"
            # 1. Thêm bản ghi vào bảng Payments
            query_pay = """
                INSERT INTO Payments (fine_id, amount_paid, payment_date, payment_method, transaction_no, staff_id)
            VALUES (?, ?, GETDATE(), ?, ?, ?)
            """
            
            params = (f_id, total_amount, method, trans_no, int(staff_id))

            if db.execute_query(query_pay, params, commit=True):
                if f_id:
                    db.execute_query("UPDATE Fines SET payment_status = 'PAID' WHERE fine_id = ?", (f_id,), commit=True)
            
                QMessageBox.information(self.ui, "Thành công", f"Hóa đơn {trans_no} đã được lưu bởi NV {staff_id}!")
                self.load_payments_history()
                self.clear_form()
            else:
                QMessageBox.critical(self.ui, "Lỗi", "Không thể lưu bản ghi thanh toán!")
        except Exception as e:
            print(f"Lỗi thanh toán: {e}")

    def load_payments_history(self):
        """Hiển thị lịch sử: Lấy Member ID thông qua bảng trung gian"""
        # Join Payments -> Fines -> BorrowingRecords để lấy user_id
        query = """
                SELECT 
                    p.[payment_id], 
                    b.[user_id], 
                    p.[payment_date], 
                    b.[borrow_id], 
                    p.[fine_id], 
                    p.[amount_paid], 
                    p.[payment_method], 
                    p.[staff_id],
                    p.[transaction_no]
                FROM [Payments] p
                LEFT JOIN [Fines] f ON p.[fine_id] = f.[fine_id]
                LEFT JOIN [Borrowing] b ON f.[borrow_id] = b.[borrow_id]
            ORDER BY p.[payment_date] DESC
        """
        rows = db.execute_query(query, fetch=True)
        self.ui.table_payments.setRowCount(0)
        
        if rows:
            for row_idx, row_data in enumerate(rows):
                self.ui.table_payments.insertRow(row_idx)
                self.ui.table_payments.setRowHeight(row_idx, 60)
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value) if value is not None else "N/A")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.ui.table_payments.setItem(row_idx, col_idx, item)

    def search_payments(self):
        """Sửa lỗi tìm kiếm mã giao dịch không ra kết quả"""
        # Lấy từ đúng ô txt_search_input trên giao diện
        keyword = self.ui.txt_search_input.text().strip()
        
        if not keyword:
            self.load_payments_history()
            return

        # Khởi tạo câu lệnh SQL với
        # Sử dụng UPPER để không phân biệt chữ hoa/thường
        query = """
            SELECT 
                p.[payment_id], b.[user_id], p.[payment_date], 
                b.[borrow_id], p.[fine_id], p.[amount_paid], 
                p.[payment_method], p.[staff_id], p.[transaction_no]
            FROM [Payments] p
            LEFT JOIN [Fines] f ON p.[fine_id] = f.[fine_id]
            LEFT JOIN [Borrowing] b ON f.[borrow_id] = b.[borrow_id]
            WHERE 
                CAST(b.[borrow_id] AS VARCHAR) = ? 
                OR UPPER(p.[transaction_no]) LIKE UPPER(?)
            ORDER BY p.[payment_date] DESC
        """
        
        # Chuẩn bị tham số: Tìm chính xác ID hoặc tìm gần đúng Mã GD
        # Thêm dấu % vào tham số thay vì nối chuỗi trong SQL để an toàn hơn
        search_pattern = f"%{keyword}%"
        params = (keyword, search_pattern)

        try:
            rows = db.execute_query(query, params, fetch=True) #
            
            self.ui.table_payments.setRowCount(0)
            if rows:
                for row_idx, row_data in enumerate(rows):
                    self.ui.table_payments.insertRow(row_idx)
                    self.ui.table_payments.setRowHeight(row_idx, 60) #
                    for col_idx, value in enumerate(row_data):
                        display_val = str(value) if value is not None else "N/A"
                        item = QTableWidgetItem(display_val)
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.ui.table_payments.setItem(row_idx, col_idx, item)
            else:
                QMessageBox.information(self.ui, "Kết quả", f"Không tìm thấy dữ liệu cho: {keyword}")
        except Exception as e:
            print(f"Lỗi SQL: {e}")

    def delete_payment(self):
        """Xóa bản ghi thanh toán đang được chọn trên bảng"""
        selected_row = self.ui.table_payments.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self.ui, "Lỗi", "Vui lòng chọn một bản ghi trong bảng để xóa!")
            return

        # Lấy Payment ID và Fine ID từ hàng đang chọn
        payment_id = self.ui.table_payments.item(selected_row, 0).text()
        fine_id_str = self.ui.table_payments.item(selected_row, 4).text() # Cột Fine ID
        
        confirm = QMessageBox.question(
            self.ui, "Xác nhận", 
            f"Bạn có chắc chắn muốn xóa bản ghi thanh toán ID: {payment_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # 1. Nếu có Fine ID (không phải N/A), cập nhật lại trạng thái UNPAID cho phiếu phạt
                if fine_id_str != "N/A":
                    #
                    db.execute_query(
                        "UPDATE Fines SET payment_status = 'UNPAID' WHERE fine_id = ?", 
                        (fine_id_str,), commit=True
                    )

                # 2. Xóa bản ghi trong bảng Payments
                #
                if db.execute_query("DELETE FROM Payments WHERE payment_id = ?", (payment_id,), commit=True):
                    QMessageBox.information(self.ui, "Thành công", "Đã xóa bản ghi thanh toán!")
                    self.load_payments_history()
            except Exception as e:
                QMessageBox.critical(self.ui, "Lỗi", f"Không thể xóa: {str(e)}")

    def clear_form(self):
        self.ui.txt_borrow_id.clear()
        self.ui.txt_staff_id.clear()
        self.ui.txt_fine_id.clear()
        self.ui.txt_base_fee.clear()
        self.ui.txt_fine_amount.setText("0")
        self.ui.txt_total_pay.clear()        