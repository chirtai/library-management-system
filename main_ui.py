import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QStackedWidget, QListWidget,
    QTableWidget, QTableWidgetItem, QGroupBox, QSplitter,
QHeaderView, QTabWidget, QMessageBox, QFormLayout, QComboBox, QGridLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

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
        try:
            with open("main.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Warning: main.qss not found or invalid.")

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

    def create_dashboard_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Grid for summary cards (2 rows × 3 columns or responsive)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(25)

        # Sample data - REPLACE THESE WITH REAL VALUES FROM YOUR DATABASE LATER
        total_books = 1247
        total_members = 482
        currently_borrowed = 156
        overdue_books = 23
        total_unpaid_fines = 1850000  # in VND

        # Card 1: Total Books
        grid_layout.addWidget(self.create_summary_card(
            "📚", "Total Books", f"{total_books:,}", "#3498db"), 0, 0)

        # Card 2: Total Members
        grid_layout.addWidget(self.create_summary_card(
            "👥", "Total Members", f"{total_members:,}", "#2ecc71"), 0, 1)

        # Card 3: Currently Borrowed
        grid_layout.addWidget(self.create_summary_card(
            "📖", "Currently Borrowed", f"{currently_borrowed}", "#f39c12"), 0, 2)

        # Card 4: Overdue Books
        grid_layout.addWidget(self.create_summary_card(
            "⚠️", "Overdue Books", f"{overdue_books}", "#e74c3c"), 1, 0)

        # Card 5: Unpaid Fines
        grid_layout.addWidget(self.create_summary_card(
            "💸", "Unpaid Fines", f"{total_unpaid_fines:,} VND", "#9b59b6"), 1, 1)

        # Optional: Add stretch to center if fewer cards
        grid_layout.addWidget(QWidget(), 1, 2)  # Empty spacer

        layout.addLayout(grid_layout)
        layout.addStretch()

        return widget

    def create_summary_card(self, icon, title, value, color):
        card = QWidget()
        card.setObjectName("summaryCard")
        card.setFixedHeight(180)
        card.setStyleSheet(f"""
            QWidget#summaryCard {{
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e0e0e0;
            }}
            QWidget#summaryCard:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.setSpacing(15)

        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 48px; color: {color};")
        card_layout.addWidget(icon_label)

        # Value (big number)
        value_label = QLabel(value)
        value_label.setObjectName("cardValue")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet(f"color: {color};")

        card_layout.addWidget(value_label)

        # Title
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card_layout.addWidget(title_label)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())