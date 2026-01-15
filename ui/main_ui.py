import sys
from pathlib import Path
# Import PyQT6
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QStackedWidget, QListWidget,
    QTableWidget, QSplitter, QListWidgetItem, QInputDialog, QTableWidgetItem,
    QHeaderView, QTabWidget, QMessageBox, QComboBox, QGridLayout)
from PyQt6.QtCore import Qt
# Import UI
from ui.fines_ui import FinesInterface
from ui.member_ui import MemberInterface
from ui.borrowing_ui import BorrowingInterface
from ui.book_ui import BookInterface
from ui.dashboard_ui import DashboardInterface

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.resize(1500, 900)
        self.current_user = None

        # ------ LOAD QSS -------
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
        self.dashboard_page = DashboardInterface(self)
        self.books_page = BookInterface(self)
        self.borrow_page = BorrowingInterface(self)
        self.members_page = MemberInterface(self)
        self.fines_page = FinesInterface(self)

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
        self.members_page.load_pending_members()
        self.members_page.load_approved_members()

    def refresh_fines(self):
        pass

# ------------ DASHBOARD INTERFACE -------------
    def create_dashboard_page(self):
        return DashboardInterface(self)
# ------------ BOOK MANAGEMENT INTERFACE ----------------
    def create_books_page(self):
        return BookInterface(self)
# ------------ BORROWING INTERFACE -----------------
    def create_borrow_page(self):
        return BorrowingInterface(self)
# ----------- MEMBER MANAGEMENT ------------
    def create_members_page(self):
        return MemberInterface(self)
# -------------- FINES INTERFACE ----------------
    def create_fines_page(self):
        return FinesInterface(self)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
