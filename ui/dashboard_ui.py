import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QStackedWidget, QListWidget,
    QTableWidget, QSplitter, QListWidgetItem, QInputDialog, QTableWidgetItem,
    QHeaderView, QTabWidget, QMessageBox, QComboBox, QGridLayout)
from PyQt6.QtCore import Qt

class DashboardInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 70, 40, 40)
        layout.setSpacing(30)

        # Summary Cards
        grid = QGridLayout()
        grid.setSpacing(25)

        # Sample data
        cards = [
            ("Total Books", "1,247", "#3498db"),
            ("Currently Borrowed", "156", "#f39c12"),
            ("Overdue Books", "23", "#e74c3c"),
            ("Total Members", "482", "#2ecc71"),
            ("Available Books", "800", "#f39c12"),
            ("Unpaid Fines", "1,850,000 ₫", "#9b59b6"),
        ]

        for i, (title, value, color) in enumerate(cards):
            row = i // 3
            col = i % 3
            card = self._create_summary_card(title, value, color)
            grid.addWidget(card, row, col)

        layout.addLayout(grid)

        # Charts Section - Split Left & Right
        charts_container = QWidget()
        charts_layout = QHBoxLayout(charts_container)  # Horizontal layout → side by side
        charts_layout.setSpacing(40)

        # LEFT: Borrowing Trends - Line Chart
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(10)

        trend_title = QLabel("Borrowing Trends (Last 12 Months)")
        trend_title.setObjectName("chartTitle")
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(trend_title)

        trend_fig = Figure(figsize=(8, 4), dpi=100)  # Slightly smaller for side-by-side
        trend_canvas = FigureCanvas(trend_fig)
        ax1 = trend_fig.add_subplot(111)

        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        borrows = [85, 92, 110, 105, 130, 145, 160, 152, 138, 125, 115, 140]

        ax1.plot(months, borrows, marker='o', color='#3498db', linewidth=2.5)
        ax1.set_xlabel("Month")
        ax1.set_ylabel("Borrows")
        ax1.grid(True, linestyle='--', alpha=0.7)
        trend_canvas.setMinimumHeight(380)
        left_layout.addWidget(trend_canvas)

        charts_layout.addWidget(left_widget, stretch=1)

        # RIGHT: Books by Category - Bar Chart
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setSpacing(10)

        cat_title = QLabel("Total Books by Category")
        cat_title.setObjectName("chartTitle")
        right_layout.addWidget(cat_title)

        cat_fig = Figure(figsize=(8, 4), dpi=100)
        cat_canvas = FigureCanvas(cat_fig)
        ax2 = cat_fig.add_subplot(111)

        categories = ['Fiction', 'Science', 'History', 'Tech', 'Literature', 'Others']
        counts = [420, 280, 190, 150, 110, 97]

        bars = ax2.bar(categories, counts, color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6', '#95a5a6'])
        ax2.set_ylabel("Number of Books")
        ax2.grid(axis='y', linestyle='--', alpha=0.7)

        for bar in bars:
            yval = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width() / 2, yval + 5, int(yval), ha='center', va='bottom')

        cat_canvas.setMinimumHeight(380)
        right_layout.addWidget(cat_canvas)

        charts_layout.addWidget(right_widget, stretch=1)

        layout.addWidget(charts_container)
        layout.addStretch()

    def _create_summary_card(self, title, value, color):
        card = QWidget()
        card.setObjectName("summaryCard")

        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        val_lbl = QLabel(value)
        val_lbl.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {color};")
        val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(val_lbl)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("cardTitle")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_lbl)

        return card