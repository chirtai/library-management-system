import sys
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QStackedWidget, QListWidget,
    QTableWidget, QSplitter, QListWidgetItem,
    QHeaderView, QTabWidget, QMessageBox, QComboBox, QGridLayout)
from PyQt6.QtCore import Qt
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.resize(1500, 900)
        self.current_user = {
            "name": "Administrator",
            "role": "ADMIN"  # Options: "ADMIN", "LIBRARIAN", "MEMBER"
        }

        # Load QSS
        BASE_DIR = Path(__file__).resolve().parent.parent
        QSS_PATH = BASE_DIR / "styles" / "main.qss"

        try:
            with open(QSS_PATH, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Warning: main.qss not found:", e)

        # Stacked widget for different pages
        self.stacked_widget = QStackedWidget()

        # Create pages
        self.dashboard_page = self.create_dashboard_page()
        self.books_page = self.create_books_page()
        self.borrow_page = self.create_borrow_page()
        self.members_page = self.create_members_page()
        self.fines_page = self.create_fines_page()

        # Add pages to stacked widget (order matters for index)
        self.stacked_widget.addWidget(self.dashboard_page)  # index 0
        self.stacked_widget.addWidget(self.books_page)  # index 1
        self.stacked_widget.addWidget(self.borrow_page)  # index 2
        self.stacked_widget.addWidget(self.members_page)  # index 3
        self.stacked_widget.addWidget(self.fines_page)  # index 4

        # Sidebar navigation
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(230)

        # Connect sidebar selection to page change
        self.sidebar.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
        self.sidebar.itemClicked.connect(self.on_sidebar_clicked)

        # Header (top bar)
        header = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(15, 10, 15, 10)

        # Main layout: header + splitter (sidebar + content)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)  # Loại bỏ khoảng cách thừa
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(header)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.stacked_widget)
        splitter.setSizes([230, 1050])
        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle { background-color: #34495e; }")

        main_layout.addWidget(splitter, 1)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Build sidebar based on role
        self.setup_sidebar_by_role()

    def setup_sidebar_by_role(self):
        role = self.current_user["role"]
        self.sidebar.clear()

        menu_items = ["Dashboard", "Books Management", "Borrowing"]

        if role in ["ADMIN", "LIBRARIAN"]:
            menu_items += ["Members Management", "Fines Management"]

        for item in menu_items:
            self.sidebar.addItem(item)

        # Set default page
        self.sidebar.setCurrentRow(0)

    def on_sidebar_clicked(self, item):
        row = self.sidebar.row(item)

        # Các trang khác bình thường
        self.stacked_widget.setCurrentIndex(row)

        # Always switch to the clicked page first
        self.stacked_widget.setCurrentIndex(row)

        # Refresh when click the tab in sidebar
        if row < len(self.sidebar):
            self.refresh_dashboard()

    def refresh_dashboard(self):
        QMessageBox.information(self, "Dashboard", "Dashboard đã tự động làm mới!")

    def create_dashboard_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
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

        return widget

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

    def create_books_page(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Search and filter bar
        top_bar = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search by BookID, Title, Author, Category...")
        search_btn = QPushButton("Search")
        search_btn.setObjectName("searchButton")
        sort_combo = QComboBox()
        sort_combo.addItems(["Title A-Z", "Author", "Publish Year", "Available Copies"])

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
        if self.current_user["role"] in ["ADMIN", "LIBRARIAN"]:
            btn_layout = QHBoxLayout()
            add_btn = QPushButton("Add New Book")
            edit_btn = QPushButton("Edit Selected")
            delete_btn = QPushButton("Delete Selected")
            for btn in [add_btn, edit_btn, delete_btn]:
                btn.setFixedHeight(35)
            btn_layout.addStretch()
            btn_layout.addWidget(add_btn)
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            layout.addLayout(btn_layout)

        widget.setLayout(layout)
        return widget

    def create_borrow_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        tabs = QTabWidget()

        # Tab 1: Current Borrowed Books
        current_tab = QWidget()
        current_layout = QVBoxLayout()
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
        widget.setLayout(layout)
        return widget

    def create_members_page(self):
        widget = QWidget()
        layout = QVBoxLayout()

        table = QTableWidget(0, 5)
        table.setHorizontalHeaderLabels(["ID", "Full Name", "Email", "Phone", "Status"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(table)
        widget.setLayout(layout)
        return widget

    def create_fines_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        table = QTableWidget(0, 7)
        table.setHorizontalHeaderLabels([
            "Fine ID", "Member", "Borrow ID", "Amount (VND)", "Reason", "Status", "Pay"
        ])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(table)
        widget.setLayout(layout)
        return widget

    def closeEvent(self, event):
        try:
            plt.close('all')
            for child in self.findChildren(FigureCanvas):
                child.figure.clear()
                child.deleteLater()
        except Exception as e:
            print("Matplotlib cleanup error:", e)

        msg = QMessageBox(self)
        msg.setWindowTitle("Thoát ứng dụng")
        msg.setText("Bạn có muốn thoát không?")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)

        reply = msg.exec()

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())