from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QTabWidget, QPushButton, QLineEdit, QMessageBox, QInputDialog,
    QDialog, QFormLayout, QAbstractItemView, QStyledItemDelegate
)
from PyQt6.QtCore import Qt
from datetime import date
from logic.borrowing_logic import BorrowingLogic

class CenterDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter

class BorrowingInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = BorrowingLogic()

        self.current_table = None
        self.history_table = None

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        tabs = QTabWidget()

        # Tab 1: Current Borrowed Books
        current_tab = QWidget()
        current_layout = QVBoxLayout(current_tab)

        self.current_table = QTableWidget(0, 6)
        self.current_table.setHorizontalHeaderLabels([
            "Borrow ID", "Book Title", "Member", "Borrow Date", "Due Date", "Status"
        ])
        self.current_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.current_table.verticalHeader().setVisible(False)
        self.current_table.setShowGrid(False)
        self.current_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.current_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.current_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.current_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.current_table.setItemDelegate(CenterDelegate(self.current_table))
        current_layout.addWidget(self.current_table)

        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.borrow_btn = QPushButton("Borrow Book")
        self.return_btn = QPushButton("Return Book")
        self.borrow_btn.setStyleSheet("background: #2e7dff; color: white; font-weight: bold;")
        self.return_btn.setStyleSheet("background: #ff5f56; color: white; font-weight: bold;")
        self.borrow_btn.clicked.connect(self.borrow_book)
        self.return_btn.clicked.connect(self.return_book)
        btn_layout.addWidget(self.borrow_btn)
        btn_layout.addWidget(self.return_btn)
        current_layout.addLayout(btn_layout)

        tabs.addTab(current_tab, "Current Borrowed Books")

        # Tab 2: Borrowing History
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)

        self.history_table = QTableWidget(0, 7)
        self.history_table.setHorizontalHeaderLabels([
            "Book", "Member", "Borrow Date", "Return Date", "Days Late", "Fine", "Paid"
        ])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setShowGrid(False)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.history_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.history_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.history_table.setItemDelegate(CenterDelegate(self.history_table))
        history_layout.addWidget(self.history_table)

        history_tab.setLayout(history_layout)
        tabs.addTab(history_tab, "Borrowing History")

        layout.addWidget(tabs)

    def load_data(self):
        try:
            # Current borrows
            current_data = self.logic.get_current_borrows()
            self.set_current_borrows(current_data)

            # History
            history_data = self.logic.get_borrowing_history()
            self.set_borrowing_history(history_data)
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Không thể tải dữ liệu:\n{str(e)}")

    def format_date(self, dt):
        """Định dạng ngày theo kiểu Việt Nam: dd/MM/yyyy"""
        if isinstance(dt, (date,)):
            return dt.strftime("%d/%m/%Y")
        return str(dt) if dt else "-"

    def set_current_borrows(self, data: list[dict]):
        self.current_table.setRowCount(0)
        for row_data in data:
            row = self.current_table.rowCount()
            self.current_table.insertRow(row)

            values = [
                row_data.get("borrow_id", ""),
                row_data.get("title", ""),
                row_data.get("full_name", ""),
                self.format_date(row_data.get("borrow_date")),
                self.format_date(row_data.get("due_date")),
                row_data.get("status", "")
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                if values[5] == "OVERDUE":  # status
                    item.setForeground(Qt.GlobalColor.red)
                self.current_table.setItem(row, col, item)

        self.current_table.resizeColumnsToContents()

    def set_borrowing_history(self, data: list[dict]):
        self.history_table.setRowCount(0)
        for row_data in data:
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)

            fine_value = row_data.get("fine", 0)
            fine_text = f"{fine_value:,.0f} ₫" if fine_value > 0 else "-"

            items = [
                row_data.get("title", ""),
                row_data.get("full_name", ""),
                self.format_date(row_data.get("borrow_date")),
                self.format_date(row_data.get("return_date")),
                str(row_data.get("days_late", 0)),
                fine_text,
                row_data.get("paid", "UNPAID")
            ]

            for col, text in enumerate(items):
                item = QTableWidgetItem(text)
                if col == 4 and int(text) > 0:          # days late
                    item.setForeground(Qt.GlobalColor.red)
                if col == 5 and text != "-":            # fine
                    item.setForeground(Qt.GlobalColor.darkRed)
                if col == 6 and text == "PAID":
                    item.setForeground(Qt.GlobalColor.darkGreen)
                elif col == 6:
                    item.setForeground(Qt.GlobalColor.red)
                self.history_table.setItem(row, col, item)

        self.history_table.resizeColumnsToContents()

    def borrow_book(self):
        dialog = BorrowBookDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                user_id = int(dialog.user_id_input.text().strip())
                book_id = int(dialog.book_id_input.text().strip())
                days = int(dialog.days_input.text().strip() or "14")
                if days <= 0:
                    raise ValueError("Số ngày mượn phải lớn hơn 0")
            except ValueError as e:
                QMessageBox.warning(self, "Lỗi nhập liệu", f"Dữ liệu không hợp lệ:\n{str(e)}")
                return

            success, message = self.logic.borrow_book(
                user_id=user_id,
                book_id=book_id,
                borrow_days=days
                # Bỏ staff_id
            )

            if success:
                QMessageBox.information(self, "Thành công", message)
                self.load_data()
            else:
                QMessageBox.warning(self, "Thất bại", message)

    def return_book(self):
        dialog = ReturnBookDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                borrow_id = int(dialog.borrow_id_input.text().strip())
            except ValueError:
                QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập Borrow ID là số.")
                return

            success, message, fine = self.logic.return_book(
                borrow_id=borrow_id
                # Bỏ staff_id
            )

            if success:
                if fine > 0:
                    QMessageBox.information(self, "Trả sách có phạt", f"{message}\nPhạt: {fine:,.0f} ₫")
                else:
                    QMessageBox.information(self, "Thành công", message)
                self.load_data()
            else:
                QMessageBox.warning(self, "Thất bại", message)


class BorrowBookDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mượn sách")
        self.setMinimumWidth(400)

        layout = QFormLayout(self)

        self.user_id_input = QLineEdit()
        self.book_id_input = QLineEdit()
        self.days_input = QLineEdit("14")

        layout.addRow("User ID:", self.user_id_input)
        layout.addRow("Book ID:", self.book_id_input)
        layout.addRow("Số ngày mượn:", self.days_input)

        buttons = QHBoxLayout()
        self.ok_btn = QPushButton("Mượn")
        self.cancel_btn = QPushButton("Hủy")
        buttons.addWidget(self.ok_btn)
        buttons.addWidget(self.cancel_btn)

        layout.addRow(buttons)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)


class ReturnBookDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Trả sách")
        layout = QFormLayout(self)

        self.borrow_id_input = QLineEdit()

        layout.addRow("Borrow ID:", self.borrow_id_input)

        buttons = QHBoxLayout()
        self.ok_btn = QPushButton("Trả")
        self.cancel_btn = QPushButton("Hủy")
        buttons.addWidget(self.ok_btn)
        buttons.addWidget(self.cancel_btn)

        layout.addRow(buttons)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)