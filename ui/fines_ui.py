from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QStackedWidget, QListWidget,
    QTableWidget, QSplitter, QListWidgetItem, QInputDialog, QTableWidgetItem,
    QHeaderView, QTabWidget, QMessageBox, QComboBox, QGridLayout)
from PyQt6.QtCore import Qt

class FinesInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        table = QTableWidget(0, 7)
        table.setHorizontalHeaderLabels([
            "Fine ID", "Member", "Borrow ID", "Amount (VND)", "Reason", "Status", "Pay"
        ])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(table)