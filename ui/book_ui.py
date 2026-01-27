from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QStackedWidget, QListWidget,
    QTableWidget, QSplitter, QListWidgetItem, QInputDialog, QTableWidgetItem,
    QHeaderView, QTabWidget, QMessageBox, QComboBox, QGridLayout)
from PyQt6.QtCore import Qt

from ui.book_dialog import BookDialog

class BookInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
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
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Title", "Author", "Category", "Publisher", "Year", "Total Copies", "Available"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
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
    # ===== CRUD LOGIC =====
    def add_book(self):
    dialog = BookDialog(self)
    if dialog.exec():
        data = dialog.get_data()

        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(""))

        values = [
            data["title"],
            data["author"],
            data["category"],
            data["publisher"],
            data["year"],
            "1",
            "1"
        ]

        for col, val in enumerate(values, start=1):
            self.table.setItem(row, col, QTableWidgetItem(val))


    def edit_book(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Please select a book to edit.")
            return

        book = {
            "title": self.table.item(row, 1).text(),
            "author": self.table.item(row, 2).text(),
            "category": self.table.item(row, 3).text(),
            "publisher": self.table.item(row, 4).text(),
            "year": self.table.item(row, 5).text(),
        }

        dialog = BookDialog(self, book)
        if dialog.exec():
            data = dialog.get_data()

            self.table.item(row, 1).setText(data["title"])
            self.table.item(row, 2).setText(data["author"])
            self.table.item(row, 3).setText(data["category"])
            self.table.item(row, 4).setText(data["publisher"])
            self.table.item(row, 5).setText(data["year"])

    def delete_book(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Please select a book to delete.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this book?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.table.removeRow(row)

