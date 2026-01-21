from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QStackedWidget, QListWidget,
    QTableWidget, QSplitter, QListWidgetItem, QInputDialog, QTableWidgetItem,
    QHeaderView, QTabWidget, QMessageBox, QComboBox, QGridLayout)
from PyQt6.QtCore import Qt

class BookInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
# ------------ BOOK MANAGEMENT INTERFACE ----------------
    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Search and filter bar
        top_bar = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search by BookID, Title, Author, Category...")
        search_btn = QPushButton("Search")
        search_btn.setObjectName("searchButton")
        sort_combo = QComboBox()
        sort_combo.addItems(["Title A-Z", "Author", "Publish Year", "Category"])

        top_bar.addWidget(search_input, 1)
        top_bar.addWidget(search_btn)
        top_bar.addSpacing(40)

        top_bar.addWidget(QLabel("Sort by:"))
        top_bar.addWidget(sort_combo)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        # Books table
        table = QTableWidget(0, 8)
        table.setHorizontalHeaderLabels([
            "ID", "Title", "Author", "Category", "Publisher", "Year", "Total Copies", "Available"
        ])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(table)

        # Buttons (Add, Edit, Delete - visible only to Admin/Librarian)
        self.books_action_layout = QHBoxLayout()
        self.books_action_layout.addStretch()

        self.btn_add_book = QPushButton("Add Book")
        self.btn_edit_book = QPushButton("Edit Selected")
        self.btn_delete_book = QPushButton("Delete Selected")

        for btn in [self.btn_add_book, self.btn_edit_book, self.btn_delete_book]:
            btn.setFixedHeight(35)
            # btn.setObjectName("actionButton")  # nếu muốn style riêng
            self.books_action_layout.addWidget(btn)

        layout.addLayout(self.books_action_layout)