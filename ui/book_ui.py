from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QTabWidget, QPushButton, QLineEdit, QMessageBox, QInputDialog,
    QDialog, QFormLayout, QAbstractItemView, QStyledItemDelegate, QComboBox, QLabel
)
from PyQt6.QtCore import Qt

from ui.book_dialog import BookDialog
from logic.book_model import BookLogic

class CenterDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter

class BookInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = BookLogic()
        self.setup_ui()
        self.load_books()
        self.btn_add_book.clicked.connect(self.add_book)
        self.btn_edit_book.clicked.connect(self.edit_book)
        self.btn_delete_book.clicked.connect(self.delete_book)

    # ------------ BOOK MANAGEMENT INTERFACE ----------------
    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Search and filter bar
        top_bar = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search by BookID, Title, Author, Category")
        sort_combo = QComboBox()
        sort_combo.addItems(["Title A-Z", "Author", "Publish Year", "Category"])

        top_bar.addWidget(search_input, 1)
        top_bar.addSpacing(40)

        top_bar.addWidget(QLabel("Sort by:"))
        top_bar.addWidget(sort_combo)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        # Books table
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Title", "Author", "Category", "Publisher", "Year"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setItemDelegate(CenterDelegate(self.table))
        layout.addWidget(self.table)

        # Buttons (Add, Edit, Delete - visible only to Admin/Librarian)
        self.books_action_layout = QHBoxLayout()
        self.books_action_layout.addStretch()

        self.btn_add_book = QPushButton("Add Book")
        self.btn_edit_book = QPushButton("Edit Selected")
        self.btn_delete_book = QPushButton("Delete Selected")
        self.btn_add_book.setStyleSheet("background: #72bd77; color: white; font-weight: bold;")
        self.btn_edit_book.setStyleSheet("background: #2e7dff; color: white; font-weight: bold;")
        self.btn_delete_book.setStyleSheet("background: #ff5f56; color: white; font-weight: bold;")

        for btn in [self.btn_add_book, self.btn_edit_book, self.btn_delete_book]:
            btn.setFixedHeight(35)
            self.books_action_layout.addWidget(btn)

        layout.addLayout(self.books_action_layout)

    def load_books(self):
        try:
            books = self.logic.get_all_books()
            self.table.setRowCount(0)
            for book in books:
                row = self.table.rowCount()
                self.table.insertRow(row)

                items = [
                    str(book.get("book_id", "")),
                    book.get("title", "-"),
                    book.get("author", "-"),
                    book.get("category", "-"),
                    book.get("publisher", "-"),
                    str(book.get("publish_year", "-")) if book.get("publish_year") else "-",
                    str(book.get("total_copies", "1")),
                    str(book.get("available_copies", "1"))
                ]

                for col, text in enumerate(items):
                    item = QTableWidgetItem(text)
                    self.table.setItem(row, col, item)

            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Can not load:\n{str(e)}")

    def filter_books(self):
        text = self.search_input.text().strip().lower()
        for row in range(self.table.rowCount()):
            hide = True
            for col in [1, 2, 3, 4, 5]:  # Title, Author, Category, Publisher, Year
                item = self.table.item(row, col)
                if item and text in item.text().lower():
                    hide = False
                    break
            self.table.setRowHidden(row, hide)

    def add_book(self):
        dialog = BookDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not data["title"].strip():
                QMessageBox.warning(self, "Error", "Title can not be empty!")
                return
            try:
                year = int(data["year"]) if data["year"].strip() else 0
            except ValueError:
                QMessageBox.warning(self, "Error", "Year need to be numeric!")
                return

            success, message = self.logic.add_book(data)
            if success:
                QMessageBox.information(self, "Success", message)
                self.load_books()
            else:
                QMessageBox.warning(self, "Failed", message)

    def edit_book(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a book to edit!")
            return

        try:
            book_id = int(self.table.item(row, 0).text())
        except (AttributeError, ValueError):
            QMessageBox.warning(self, "Error", "Can not edit book id!")
            return

        book = {
            "title": self.table.item(row, 1).text() if self.table.item(row, 1) else "",
            "author": self.table.item(row, 2).text() if self.table.item(row, 2) else "",
            "category": self.table.item(row, 3).text() if self.table.item(row, 3) else "",
            "publisher": self.table.item(row, 4).text() if self.table.item(row, 4) else "",
            "year": self.table.item(row, 5).text() if self.table.item(row, 5) else "",
        }

        dialog = BookDialog(self, book)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            success, message = self.logic.update_book(book_id, data)
            if success:
                QMessageBox.information(self, "Success", message)
                self.load_books()
            else:
                QMessageBox.warning(self, "Failed", message)

    def delete_book(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a book to delete!")
            return

        try:
            book_id = int(self.table.item(row, 0).text())
        except (AttributeError, ValueError):
            QMessageBox.warning(self, "Error", "Can not delete book id!")
            return

        reply = QMessageBox.question(
            self, "Confirm",
            f"Do you sure to delete this book {book_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.logic.delete_book(book_id)
            if success:
                QMessageBox.information(self, "Success", message)
                self.load_books()
            else:
                QMessageBox.warning(self, "Failed", message)