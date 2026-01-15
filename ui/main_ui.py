import sys
import matplotlib
from fontTools.merge import layout
from logic.members import Member




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
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.resize(1500, 900)
        self.current_user = None

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
        main_layout.setSpacing(0)  
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

        self.refresh_functions = {
            0: self.refresh_dashboard,  # Dashboard
            1: self.refresh_books,  # Books Management
            2: self.refresh_borrow,  # Borrowing
            3: self.refresh_members,  # Members Management
            4: self.refresh_fines,  # Fines Management
        }
    def setup_sidebar_by_role(self):
        if not self.current_user or "role" not in self.current_user:
            return

        role = self.current_user["role"].upper()
        self.sidebar.clear()

        # Default Sidebar for every role
        menu_items = ["Dashboard", "Books Management", "Borrowing"]

        if role in ["ADMIN", "LIBRARIAN"]:
            menu_items.extend(["Members Management", "Fines Management"])

        for item in menu_items:
            self.sidebar.addItem(item)

        # Set default page
        if menu_items:
            self.sidebar.setCurrentRow(0)

    def on_sidebar_clicked(self, item):
        if self.current_user is None:
            QMessageBox.warning(self, "Error", "User not found")
            return

        row = self.sidebar.row(item)
        page_name = item.text().strip()

        # Page that ADMIN / LiBRARIAN can see
        restricted_pages = {
            "Members Management": ["ADMIN"],
            "Fines Management": ["ADMIN", "LIBRARIAN"],
        }

        if page_name in restricted_pages:
            allowed_roles = restricted_pages[page_name]
            if self.current_user.get("role") not in allowed_roles:
                QMessageBox.warning(
                    self,
                    "Access Denied",
                    f"Only {', '.join(allowed_roles)} can access {page_name}."
                )
                self.sidebar.setCurrentRow(0)
                self.stacked_widget.setCurrentIndex(0)
                return

        self.stacked_widget.setCurrentIndex(row)

        # Refresh when click the tab in sidebar
        if row in self.refresh_functions:
            self.refresh_functions[row]()

    def update_ui_by_role(self):
        if self.current_user is None:
            print("WARNING: current_user is None in update_ui_by_role")
            return

        role = self.current_user.get("role", "").upper()
        #print(f"DEBUG update_ui_by_role: role = {role}")  # debug

        show_buttons = role in ["ADMIN", "LIBRARIAN"]

        if hasattr(self, 'btn_add_book'):
            self.btn_add_book.setVisible(show_buttons)
            self.btn_edit_book.setVisible(show_buttons)
            self.btn_delete_book.setVisible(show_buttons)
            #print(f"Buttons visible: {show_buttons}")  # debug

#------------ REFRESH PAGE ---------------
    def refresh_dashboard(self):
        pass

    def refresh_books(self):
        pass

    def refresh_borrow(self):
        pass

    def refresh_members(self):
        self.load_pending_members()
        self.load_approved_members()

    def refresh_fines(self):
        pass

    # ------------ DASHBOARD INTERFACE -------------
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

# ------------ BOOK MANAGEMENT INTERFACE ----------------
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

        widget.setLayout(layout)
        return widget

# ------------ BORROWING INTERFACE -----------------
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

# ------------ MEMBER MANAGEMENT INTERFACE ----------------
    def create_members_page(self):
        widget = QWidget()
        main_layout = QVBoxLayout(widget)


        # Create Tab Widget
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setTabPosition(QTabWidget.TabPosition.North)

        # Tab 1: Approved Members
        approved_tab = QWidget()
        approved_layout = QVBoxLayout(approved_tab)

        # Search + Filter bar
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search by Name, Phone Number, ...")
        search_btn = QPushButton("Search")
        search_layout.addWidget(search_input, 1)
        search_layout.addWidget(search_btn)
        approved_layout.addLayout(search_layout)

        # Table thành viên đã duyệt
        self.approved_table = QTableWidget(0, 7)
        self.approved_table.setHorizontalHeaderLabels([
            "ID", "Full Name", "Email", "Phone Number", "Register Date", "Role", "Status"
        ])
        self.approved_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.approved_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        approved_layout.addWidget(self.approved_table)

        tabs.addTab(approved_tab, "Approved Members")

        # ── Tab 2: Pending Approvals ─────────────────────────────────────
        pending_tab = QWidget()
        pending_layout = QVBoxLayout(pending_tab)

        # Table chờ duyệt
        self.pending_table = QTableWidget(0, 7)
        self.pending_table.setHorizontalHeaderLabels([
            "ID", "Full Name", "Email", "Phone Number", "Register date", "Reason", "Action"
        ])
        header = self.pending_table.horizontalHeader()
        for col in range(6):  # 0 đến 5
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.pending_table.setColumnWidth(6, 200)
        self.pending_table.verticalHeader().setDefaultSectionSize(60)
        self.pending_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        pending_layout.addWidget(self.pending_table)

        # Approve / Reject All Buttons
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        self.approve_all_btn = QPushButton("Approve All")
        self.reject_all_btn = QPushButton("Reject All")
        action_layout.addWidget(self.approve_all_btn)
        action_layout.addWidget(self.reject_all_btn)
        pending_layout.addLayout(action_layout)

        tabs.addTab(pending_tab, "Pending Members")

        main_layout.addWidget(tabs)

        # Kết nối nút Approve/Reject All (phiên bản đơn giản - approve/reject tất cả pending)
        self.approve_all_btn.clicked.connect(self.approve_all_pending)
        self.reject_all_btn.clicked.connect(self.reject_all_pending)

        # Load dữ liệu lần đầu
        self.load_pending_members()
        self.load_approved_members()

        return widget

# -------------- FINES INTERFACE ----------------
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

# -------------- SIGN OUT ------------------
    def closeEvent(self, event):
        try:
            plt.close('all')
            for child in self.findChildren(FigureCanvas):
                child.figure.clear()
                child.deleteLater()
        except Exception as e:
            print("Matplotlib cleanup error:", e)

        msg = QMessageBox(self)
        msg.setWindowTitle("Exit")
        msg.setText("Sign out and exit?")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)

        reply = msg.exec()

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

# ------------ LOAD DATABASE -------------
    def load_pending_members(self):
        results = Member.get_pending_members()

        self.pending_table.setRowCount(len(results))
        for row, record in enumerate(results):
            user_id = None
            try:
                user_id = record[0] if len(record) > 0 else None
                full_name = record[1] if len(record) > 1 else ""
                email = record[2] if len(record) > 2 else ""
                phone = record[3] if len(record) > 3 else ""
                reg_date = record[4] if len(record) > 4 else ""
                reason = record[5 ] if len(record) > 5 else ""

                self.pending_table.setItem(row, 0, QTableWidgetItem(str(user_id)))
                self.pending_table.setItem(row, 1, QTableWidgetItem(full_name or ""))
                self.pending_table.setItem(row, 2, QTableWidgetItem(email or ""))
                self.pending_table.setItem(row, 3, QTableWidgetItem(phone or ""))
                self.pending_table.setItem(row, 4, QTableWidgetItem(reg_date or ""))
                self.pending_table.setItem(row, 5, QTableWidgetItem(reason) or "")
            except Exception as e:
                print(f"Error filling pending row {row}: {str(e)}")
                print("Record data:", record)

            if user_id is None:
                continue
            # Action buttons
            action_widget = QWidget()
            hbox = QHBoxLayout(action_widget)
            hbox.setContentsMargins(4, 2, 4, 2)
            hbox.setSpacing(8)

            hbox.addStretch(1)

            btn_approve = QPushButton("Approve")
            btn_reject = QPushButton("Reject")
            btn_approve.setFixedWidth(90)
            btn_reject.setFixedWidth(90)

            btn_approve.clicked.connect(lambda checked, uid = user_id: self.approve_pending(uid))
            btn_reject.clicked.connect(lambda checked, uid = user_id: self.reject_pending(uid))

            hbox.addWidget(btn_approve)
            hbox.addWidget(btn_reject)
            hbox.addStretch(1)

            self.pending_table.setCellWidget(row, 6, action_widget)

    def load_approved_members(self):
        results = Member.get_approved_members()

        self.approved_table.setRowCount(len(results))
        for row, record in enumerate(results):
            try:
                # Unpack an toàn hơn
                user_id = record[0] if len(record) > 0 else None
                full_name = record[1] if len(record) > 1 else ""
                email = record[2] if len(record) > 2 else ""
                phone = record[3] if len(record) > 3 else ""
                reg_date = record[4] if len(record) > 4 else ""
                role = record[5] if len(record) > 5 else ""
                status = record[6] if len(record) > 6 else ""

                self.approved_table.setItem(row, 0, QTableWidgetItem(str(user_id or "")))
                self.approved_table.setItem(row, 1, QTableWidgetItem(str(full_name or "")))
                self.approved_table.setItem(row, 2, QTableWidgetItem(str(email or "")))
                self.approved_table.setItem(row, 3, QTableWidgetItem(str(phone or "")))
                self.approved_table.setItem(row, 4, QTableWidgetItem(str(reg_date or "")))
                self.approved_table.setItem(row, 5, QTableWidgetItem(str(role or "")))
                self.approved_table.setItem(row, 6, QTableWidgetItem(str(status or "")))
            except Exception as e:
                print(f"Error filling row {row}: {str(e)}")
                print("Record data:", record)

    def approve_pending(self, user_id):
        if Member.approve_member(user_id):
            QMessageBox.information(self, "Success", f"Approved member with ID {user_id}")
            self.load_pending_members()
            self.load_approved_members()
        else:
            QMessageBox.critical(self, "Error", "Can not approve this user")

    def reject_pending(self, user_id):
        try:
            if user_id is None:
                raise ValueError("User ID is None")

            reason, ok = QInputDialog.getText(
                self,
                "Reject this pending member?",
                "Reason for rejection:"
            )

            if ok:
                if Member.reject_member(user_id, reason):
                    QMessageBox.information(self, "Success", f"Rejected member with ID {user_id}")
                    self.load_pending_members()
                else:
                    QMessageBox.critical(self, "Error", "Can not reject this user")
        except Exception as e:
            print(f"[ERROR in reject_pending]: {str(e)}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Reject failed: {str(e)}")

    def approve_all_pending(self):
        reply = QMessageBox.question(
            self, "Confirm",
            "Are you sure you want to approve all pending members?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            user_ids = []
            for row in range(self.pending_table.rowCount()):
                item = self.pending_table.item(row, 0)
                if item:
                    user_ids.append(int(item.text()))

            if user_ids:
                count = Member.approve_multiple_members(user_ids)
                QMessageBox.information(self, "Done!", f"Approved {count} member{'s' if count > 1 else ''}")
                self.load_pending_members()
                self.load_approved_members()

    def reject_all_pending(self):
        reason, ok = QInputDialog.getText(
            self,
            "Reject all pending members?",
            "Reason for rejection:"
        )

        if ok:
            reply = QMessageBox.question(
                self, "Confirm",
                "Are you sure you want to reject all pending members?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                user_ids = []
                for row in range(self.pending_table.rowCount()):
                    item = self.pending_table.item(row, 0)
                    if item:
                        user_ids.append(int(item.text()))

                if user_ids:
                    count = Member.reject_multiple_members(user_ids, reason)
                    QMessageBox.information(self, "Done", f"Rejected {count} member{'s' if count > 1 else ''}")
                    self.load_pending_members()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
