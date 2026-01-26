from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QStackedWidget, QListWidget,
    QTableWidget, QSplitter, QListWidgetItem, QInputDialog, QTableWidgetItem,
    QHeaderView, QTabWidget, QMessageBox, QComboBox, QGridLayout)
from PyQt6.QtCore import Qt

class BorrowingInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

# ------------ BORROWING INTERFACE -----------------
    def setup_ui(self):
        layout = QVBoxLayout(self)
        tabs = QTabWidget()

        # Tab 1: Current Borrowed Books
        current_tab = QWidget()
        current_layout = QVBoxLayout(current_tab)
        current_table = QTableWidget(0, 6)
        current_table.setHorizontalHeaderLabels([
            "Borrow ID", "Book Title", "Member", "Borrow Date", "Due Date", "Status"
        ])
        current_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        current_layout.addWidget(current_table)
        current_tab.setLayout(current_layout)
        tabs.addTab(current_tab, "Current Borrowed Books")

        # Tab 2: Borrowing History
        history_tab = QWidget()
        history_layout = QVBoxLayout()
        history_table = QTableWidget(0, 7)
        history_table.setHorizontalHeaderLabels([
            "Book", "Member", "Borrow Date", "Return Date", "Days Late", "Fine", "Paid"
        ])
        history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        history_layout.addWidget(history_table)
        history_tab.setLayout(history_layout)
        tabs.addTab(history_tab, "Borrowing History")

        layout.addWidget(tabs)