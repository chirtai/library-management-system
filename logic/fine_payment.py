from database.db_connection import db
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton
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
                gridline-color: #d0d0d0; /* Distinct gray for grid lines */
                border: none;
            }
            QTableWidget::item {
                border-bottom: 1px solid #d0d0d0; /* Manual horizontal lines */
                padding: 5px;
            }
        """)

        """Query data from SQL and populate QTableWidget"""
        # SQL query combining 3 tables to get member info
        query = """
            SELECT 
                f.fine_id, 
                u.user_id,     -- Column 1
                f.borrow_id,   -- Column 2
                f.amount,      -- Column 3
                f.reason,      -- Column 4
                f.payment_status -- Column 5
            FROM Fines f
            LEFT JOIN Borrowing b ON f.borrow_id = b.borrow_id
            LEFT JOIN Users u ON b.user_id = u.user_id
            ORDER BY f.fine_id DESC
        """
        # Execute query via db object
        rows = db.execute_query(query, fetch=True)
        
        # Clear old data from UI table
        self.ui.table.setRowCount(0)
        
        if rows:
            for row_idx, row_data in enumerate(rows):
                self.ui.table.insertRow(row_idx)
                self.ui.table.setRowHeight(row_idx, 60)
                for col_idx, value in enumerate(row_data):
                    # Display text data in cells
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.ui.table.setItem(row_idx, col_idx, item)
                
                # Logic to display "Pay" button in the last column
                status = row_data[5]    
                if status == 'UNPAID':
                    btn_pay = QPushButton("Pay")
                    btn_pay.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 3px;")
                    # Connect Pay button to payment handler
                    btn_pay.clicked.connect(lambda _, r=row_idx: self.handle_payment(r))
                    self.ui.table.setCellWidget(row_idx, 6, btn_pay)
                else:
                    paid_item = QTableWidgetItem("Completed")
                    paid_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.ui.table.setItem(row_idx, 6, paid_item)

    def add_fine(self):
        """Add new fine based on Form data"""
        borrow_id = self.ui.txt_borrow_id.text().strip()
        amount = self.ui.txt_amount.text()
        reason = self.ui.txt_reason.text()
        status = self.ui.cb_status.currentText()

        check_query = "SELECT borrow_id FROM Borrowing WHERE borrow_id = ?"
        exists = db.execute_query(check_query, (borrow_id,), fetch="one")

        if not borrow_id or not amount:
            QMessageBox.warning(self.ui, "Error", "Please enter Borrow ID and Amount!")
            return
        
        if not exists:
            QMessageBox.critical(self.ui, "Data Error", 
                                f"Borrow ID {borrow_id} does not exist in the system!")
            return

        query = "INSERT INTO Fines (borrow_id, amount, reason, payment_status) VALUES (?, ?, ?, ?)"
        success = db.execute_query(query, (borrow_id, amount, reason, status), commit=True)
        
        if success:
            QMessageBox.information(self.ui, "Success", "Fine added successfully!")
            self.load_data()
            self.clear_form()
        else:
            QMessageBox.critical(self.ui, "Error", "Could not add fine. Please check Borrow ID!")

    def update_fine(self):
        """Update selected fine"""
        selected_row = self.ui.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self.ui, "Notice", "Please select a row to edit!")
            return

        fine_id = self.ui.table.item(selected_row, 0).text()
        query = "UPDATE Fines SET amount = ?, reason = ?, payment_status = ? WHERE fine_id = ?"
        params = (self.ui.txt_amount.text(), self.ui.txt_reason.text(), self.ui.cb_status.currentText(), fine_id)
        
        if db.execute_query(query, params, commit=True):
            QMessageBox.information(self.ui, "Success", "Data updated successfully!")
            self.load_data()

    def delete_fine(self):
        """Delete fine based on Fine ID"""
        selected_row = self.ui.table.currentRow()
        if selected_row >= 0:
            fine_id = self.ui.table.item(selected_row, 0).text()
            confirm = QMessageBox.question(self.ui, "Confirm", f"Delete fine {fine_id}?", 
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if confirm == QMessageBox.StandardButton.Yes:
                db.execute_query("DELETE FROM Fines WHERE fine_id = ?", (fine_id,), commit=True)
                self.load_data()
                self.clear_form()

    def clear_form(self):
        """Clear input fields"""
        self.ui.txt_borrow_id.clear()
        self.ui.txt_borrow_id.setReadOnly(False)
        self.ui.txt_amount.clear()
        self.ui.txt_reason.clear()
        self.ui.cb_status.setCurrentIndex(0)


class PaymentsController:
    def __init__(self, ui_instance):
        self.ui = ui_instance

        self.ui.btn_delete.setObjectName("btn_delete")
        self.ui.btn_pay.setObjectName("btn_pay")

        button_qss = """
            QPushButton {
                border-radius: 6px;
                padding: 8px;
                color: white;
                font-weight: bold;
                border: none;
            }
            /* Confirm Button (Green) */
            QPushButton#btn_pay { 
                background-color: #28a745; 
            }
            QPushButton#btn_pay:hover { 
                background-color: #218838; 
            }

            /* Delete Button (Red) - Đã sửa ở đây */
            QPushButton#btn_delete { 
                background-color: #dc3545; 
            }
            QPushButton#btn_delete:hover { 
                background-color: #c82333; 
            }
            QPushButton#btn_delete:pressed { 
                background-color: #a71d2a; 
            }
        """
        self.ui.btn_pay.setStyleSheet(button_qss)
        self.ui.btn_delete.setStyleSheet(button_qss)
        if hasattr(self.ui, 'btn_check'): 
            self.ui.btn_check.setStyleSheet(button_qss)

    def check_staff_exists(self, staff_id):
        """Check if Staff ID exists in Users table"""
        query = "SELECT full_name FROM Users WHERE user_id = ?"
        result = db.execute_query(query, (staff_id,), fetch="one")
        return result[0] if result else None
    
    def check_borrow_info(self):
        """Check info and auto-fill input fields"""
        borrow_id = self.ui.txt_borrow_id.text()
        if not borrow_id:
            QMessageBox.warning(self.ui, "Error", "Please enter Borrow ID!")
            return

        # 1. Get info from Borrowing table
        query_borrow = "SELECT user_id, borrow_date, due_date FROM Borrowing WHERE borrow_id = ?"
        borrow_data = db.execute_query(query_borrow, (borrow_id,), fetch="one")

        if borrow_data:
            user_id, b_date, d_date = borrow_data

            # 2. Calculate base fee = (due_date - borrow_date) * 10000 logic
            delta = d_date - b_date
            total_days = max(0, delta.days) 
            periods = math.ceil(total_days / 2) if total_days > 0 else 0
            base_fee = periods * 10000
            self.ui.txt_base_fee.setText(str(base_fee))

            # 3. Check for UNPAID Fines linked to this borrow_id
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
            QMessageBox.critical(self.ui, "Error", "Borrow ID not found!")

    def process_payment(self):
        """Confirm payment and update Fine status"""
        borrow_id = self.ui.txt_borrow_id.text().strip()
        fine_id = self.ui.txt_fine_id.text().strip()
        total_amount = self.ui.txt_total_pay.text().strip()
        method = self.ui.cb_method.currentText()
        staff_id = self.ui.txt_staff_id.text().strip()

        if not staff_id or not total_amount:
            QMessageBox.warning(self.ui, "Error", "Payment information missing!")
            return
            
        try:
            if fine_id:
                check_query = "SELECT payment_id FROM Payments WHERE fine_id = ?"
                exists = db.execute_query(check_query, (fine_id,), fetch="one")
            else:
                # Check if base payment exists for this borrow_id
                check_query = "SELECT payment_id FROM Payments WHERE borrow_id = ? AND fine_id IS NULL"
                exists = db.execute_query(check_query, (borrow_id,), fetch="one")

            if exists:
                QMessageBox.warning(self.ui, "Notice", f"Transaction for Borrow ID {borrow_id} already exists in history!")
                return 

            staff_id = int(staff_id)
            staff_name = self.check_staff_exists(staff_id)
            if not staff_name:
                QMessageBox.critical(self.ui, "Authentication Error",
                                     f"Staff with ID {staff_id} does not exist in the system!")
                return
        
            f_id = int(fine_id) if fine_id else None
            trans_no = f"PAY{random.randint(1000, 9999)}"
            # 1. Add record to Payments table
            query_pay = """
                INSERT INTO Payments (fine_id, amount_paid, payment_date, payment_method, transaction_no, staff_id, borrow_id)
            VALUES (?, ?, GETDATE(), ?, ?, ?, ?)
            """
            
            params = (f_id, total_amount, method, trans_no, int(staff_id), int(borrow_id))

            if db.execute_query(query_pay, params, commit=True):
                if f_id:
                    db.execute_query("UPDATE Fines SET payment_status = 'PAID' WHERE fine_id = ?", (f_id,), commit=True)
            
                QMessageBox.information(self.ui, "Success", f"Invoice {trans_no} saved by Staff {staff_id}!")
                self.load_payments_history()
                self.clear_form()
            else:
                QMessageBox.critical(self.ui, "Error", "Could not save payment record!")
        except Exception as e:
            print(f"Payment error: {e}")

    def load_payments_history(self):
        """Display history: Get Member ID via intermediate tables"""
        query = """
               SELECT 
                p.payment_id, 
                b.user_id,     -- Member ID
                p.payment_date, 
                p.borrow_id, 
                p.fine_id, 
                p.amount_paid, 
                p.payment_method, 
                p.staff_id,
                p.transaction_no
            FROM Payments p
            LEFT JOIN Borrowing b ON p.borrow_id = b.borrow_id
            ORDER BY p.payment_date DESC
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
        """Search payments by Borrow ID or Transaction Number"""
        keyword = self.ui.txt_search_input.text().strip()
        
        if not keyword:
            self.load_payments_history()
            return

        query = """
            SELECT 
                p.payment_id, 
                b.user_id,        -- Get Member ID from Borrowing
                p.payment_date, 
                p.borrow_id,      -- Get from Payments
                p.fine_id, 
                p.amount_paid, 
                p.payment_method, 
                p.staff_id,
                p.transaction_no
            FROM Payments p
            LEFT JOIN Borrowing b ON p.borrow_id = b.borrow_id
            WHERE 
                CAST(p.borrow_id AS VARCHAR) = ? 
                OR UPPER(p.transaction_no) LIKE UPPER(?)
            ORDER BY p.payment_date DESC
        """
        
        search_pattern = f"%{keyword}%"
        params = (keyword, search_pattern)

        try:
            rows = db.execute_query(query, params, fetch=True) 
            
            self.ui.table_payments.setRowCount(0)
            if rows:
                for row_idx, row_data in enumerate(rows):
                    self.ui.table_payments.insertRow(row_idx)
                    self.ui.table_payments.setRowHeight(row_idx, 60) 
                    for col_idx, value in enumerate(row_data):
                        display_val = str(value) if value is not None else "N/A"
                        item = QTableWidgetItem(display_val)
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.ui.table_payments.setItem(row_idx, col_idx, item)
            else:
                QMessageBox.information(self.ui, "Results", f"No data found for: {keyword}")
        except Exception as e:
            print(f"SQL Error: {e}")

    def delete_payment(self):
        """Delete selected payment record from table"""
        selected_row = self.ui.table_payments.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self.ui, "Error", "Please select a record from the table to delete!")
            return

        payment_id = self.ui.table_payments.item(selected_row, 0).text()
        fine_id_str = self.ui.table_payments.item(selected_row, 4).text() 
        
        confirm = QMessageBox.question(
            self.ui, "Confirm", 
            f"Are you sure you want to delete payment record ID: {payment_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # 1. If Fine ID exists, revert status to UNPAID
                if fine_id_str != "N/A":
                    db.execute_query(
                        "UPDATE Fines SET payment_status = 'UNPAID' WHERE fine_id = ?", 
                        (fine_id_str,), commit=True
                    )

                # 2. Delete from Payments table
                if db.execute_query("DELETE FROM Payments WHERE payment_id = ?", (payment_id,), commit=True):
                    QMessageBox.information(self.ui, "Success", "Payment record deleted!")
                    self.load_payments_history()
            except Exception as e:
                QMessageBox.critical(self.ui, "Error", f"Could not delete: {str(e)}")

    def clear_form(self):
        self.ui.txt_borrow_id.clear()
        self.ui.txt_staff_id.clear()
        self.ui.txt_fine_id.clear()
        self.ui.txt_base_fee.clear()
        self.ui.txt_fine_amount.setText("0")
        self.ui.txt_total_pay.clear()