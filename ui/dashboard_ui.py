# ui/dashboard_ui.py

import matplotlib
matplotlib.use("QtAgg")

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFrame
)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from logic.dashboard_logic import DashboardLogic


class DashboardInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = DashboardLogic()
        self.init_ui()
        self.load_data()

    # ================= UI =================
    def init_ui(self):
        self.setStyleSheet("""
            QWidget { background: #f4f6f9; font-family: Segoe UI; }
            QLabel#title { font-size: 26px; font-weight: 700; }
            QFrame.card { background: white; border-radius: 14px; padding: 18px; }
            QLabel.cardValue { font-size: 30px; font-weight: bold; }
            QLabel.cardTitle { color: #7f8c8d; font-size: 13px; }
        """)

        main = QVBoxLayout(self)
        main.setContentsMargins(30, 25, 30, 30)
        main.setSpacing(25)

        title = QLabel("Library Management Dashboard")
        title.setObjectName("title")
        main.addWidget(title)

        # ===== SUMMARY CARDS =====
        grid = QGridLayout()
        grid.setSpacing(20)

        self.cards = {}
        self.card_config = [
            ("total_books", "Total Books", "#3498db"),
            ("borrowed", "Borrowed Books", "#f39c12"),
            ("overdue", "Overdue Books", "#e74c3c"),
            ("members", "Members", "#2ecc71"),
            ("available", "Available Books", "#1abc9c"),
            ("fines", "Unpaid Fines", "#9b59b6"),
        ]

        for i, (key, title, color) in enumerate(self.card_config):
            card = self.create_card(title, color)
            self.cards[key] = card
            grid.addWidget(card, i // 3, i % 3)

        main.addLayout(grid)

        # ===== CHARTS =====
        charts = QHBoxLayout()
        charts.setSpacing(20)

        self.borrow_chart = self.create_borrow_chart()
        self.category_chart = self.create_category_chart()

        charts.addWidget(self.borrow_chart["frame"])
        charts.addWidget(self.category_chart["frame"])

        main.addLayout(charts)

    # ================= COMPONENTS =================
    def create_card(self, title, color):
        card = QFrame()
        card.setProperty("class", "card")
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        value = QLabel("0")
        value.setProperty("class", "cardValue")
        value.setStyleSheet(f"color: {color}")
        layout.addWidget(value)

        text = QLabel(title)
        text.setProperty("class", "cardTitle")
        layout.addWidget(text)

        card.value_label = value
        return card

    def create_borrow_chart(self):
        frame = QFrame()
        frame.setProperty("class", "card")
        layout = QVBoxLayout(frame)

        layout.addWidget(QLabel("Borrowing Trends (12 Months)"))

        fig = Figure(figsize=(5, 3))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        layout.addWidget(canvas)
        return {"frame": frame, "ax": ax, "canvas": canvas}

    def create_category_chart(self):
        frame = QFrame()
        frame.setProperty("class", "card")
        layout = QVBoxLayout(frame)

        layout.addWidget(QLabel("Books by Category"))

        fig = Figure(figsize=(5, 3))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        layout.addWidget(canvas)
        return {"frame": frame, "ax": ax, "canvas": canvas}

    # ================= DATA =================
    def load_data(self):
        # SUMMARY
        stats = self.logic.get_summary_stats()
        for key, value in stats.items():
            if key == "fines":
                self.cards[key].value_label.setText(f"{value:,} ₫")
            else:
                self.cards[key].value_label.setText(str(value))

        # LINE CHART
        trend = self.logic.get_borrowing_trends()
        ax = self.borrow_chart["ax"]
        ax.clear()
        ax.plot(trend["months"], trend["values"], marker="o")
        ax.grid(True, linestyle="--", alpha=0.6)
        self.borrow_chart["canvas"].draw()

        # BAR CHART
        cat = self.logic.get_books_by_category()
        ax2 = self.category_chart["ax"]
        ax2.clear()
        ax2.bar(cat["categories"], cat["values"])
        ax2.grid(axis="y", linestyle="--", alpha=0.6)
        self.category_chart["canvas"].draw()
