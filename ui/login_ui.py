import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox, QCheckBox, QHBoxLayout,
)
from PyQt6.QtCore import Qt
from logic.auth_service import AuthService

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.resize(500, 500)

        # Load QSS
        BASE_DIR = Path(__file__).resolve().parent.parent
        QSS_PATH = BASE_DIR / "styles" / "login.qss"

        try:
            with open(QSS_PATH, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Warning: main.qss not found:", e)

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # "Login "Title
        title = QLabel("Sign in")
        main_layout.addWidget(title)
        title.setObjectName("loginTitle")

        # Username
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Username")
        main_layout.addWidget(self.input_username)
        self.input_username.setObjectName("usernameInput")

        # Password
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)  # Ẩn mật khẩu
        main_layout.addWidget(self.input_password)
        self.input_password.setObjectName("passwordInput")

        # Login Button
        btn_login = QPushButton("Login")
        btn_login.clicked.connect(self.check_login)
        main_layout.addWidget(btn_login)
        btn_login.setObjectName("loginButton")

        # Bottom Layout
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        # Remember Me Checkbox
        self.remember_checkbox = QCheckBox("Remember Me")
        self.remember_checkbox.setObjectName("rememberCheckbox")
        bottom_layout.addWidget(self.remember_checkbox)

        bottom_layout.addStretch()

        # "Don't have an account" Button
        btn_create_account = QPushButton("Don't have an account?")
        btn_create_account.clicked.connect(self.check_create_account)
        bottom_layout.addWidget(btn_create_account)
        btn_create_account.setObjectName("createAccountButton")

        main_layout.addLayout(bottom_layout)
        main_layout.addStretch()

    def check_login(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter your username and password!")
            return
        success, user_info, message = AuthService.login(username, password)
        if success:
            # Insert user infos
            from main_ui import MainWindow
            self.main_window = MainWindow()
            self.main_window.current_user = {
                "user_id": user_info['user_id'],
                "name": user_info['full_name'],
                "role": user_info['role']
            }

            # Update sidebar by role
            self.main_window.setup_sidebar_by_role()
            self.main_window.update_ui_by_role()
            # Redirect to Dashboard
            self.main_window.stacked_widget.setCurrentIndex(0)
            self.main_window.sidebar.setCurrentRow(0)

            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Sign in failed", message)

    def check_create_account(self):
        # Open Register Window
        from ui.register_ui import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())