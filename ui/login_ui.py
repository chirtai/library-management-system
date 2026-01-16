import sys
from pathlib import Path
import keyring
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox, QCheckBox, QHBoxLayout,
)
from PyQt6.QtCore import Qt
from logic.auth_service import AuthService
from ui.register_ui import RegisterWindow
from ui.main_ui import MainWindow

APP_NAME = "LibraryManagementSystem"

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

        # "Login" Title
        title = QLabel("Login")
        title.setObjectName("loginTitle")
        main_layout.addWidget(title)

        # Username
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Username")
        self.input_username.setObjectName("usernameInput")
        main_layout.addWidget(self.input_username)

        # Password
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Password")
        self.input_password.setObjectName("passwordInput")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        main_layout.addWidget(self.input_password)

        # Bottom Layout
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        # Remember Me Checkbox
        self.remember_checkbox = QCheckBox("Remember Me")
        self.remember_checkbox.setObjectName("rememberCheckbox")
        bottom_layout.addWidget(self.remember_checkbox)

        # Reset password
        btn_pass_reset = QPushButton("Forgot Password?")
        bottom_layout.addWidget(btn_pass_reset, alignment=Qt.AlignmentFlag.AlignRight)
        btn_pass_reset.setObjectName("passwordResetButton")

        main_layout.addLayout(bottom_layout)
        # Login Button
        btn_login = QPushButton("Login")
        btn_login.clicked.connect(self.check_login)
        main_layout.addWidget(btn_login)
        btn_login.setObjectName("loginButton")

        # "Don't have an account" Button
        btn_create_account = QPushButton("Don't have an account? Register")
        btn_create_account.clicked.connect(self.check_create_account)
        main_layout.addWidget(btn_create_account, alignment=Qt.AlignmentFlag.AlignCenter)
        btn_create_account.setObjectName("createAccountButton")

        # Load Remember me
        self.load_remembered_credentials()

    # Load username and password (if possible)
    def load_remembered_credentials(self):
        username = keyring.get_password(APP_NAME, "remember_username")
        password = keyring.get_password(APP_NAME, "remember_password")

        if username and password:
            self.input_username.setText(username)
            self.input_password.setText(password)
            self.remember_checkbox.setChecked(True)

    # Save Username and Password to keyring
    def save_remembered_credentials(self, username: str, password: str):
        keyring.set_password(APP_NAME, "remember_username", username)
        keyring.set_password(APP_NAME, "remember_password", password)

    # Clear saved Username and Password
    def clear_remembered_credentials(self):
        try:
            keyring.delete_password(APP_NAME, "remember_username")
            keyring.delete_password(APP_NAME, "remember_password")
        except keyring.errors.PasswordDeleteError:
            pass

    # Check if user can log in
    def check_login(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter your username and password!")
            return
        success, user_info, message = AuthService.login(username, password)
        if success:
            if success:
                # Check if Remember me is checked
                if self.remember_checkbox.isChecked():
                    self.save_remembered_credentials(username, password)
                else:
                    self.clear_remembered_credentials()

            # Login Success
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

    # Redirect to Register Page
    def check_create_account(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

# Check remember me before open LoginWindow
def try_auto_login():
    username = keyring.get_password("LibraryManagementSystem", "remember_username")
    password = keyring.get_password("LibraryManagementSystem", "remember_password")

    if username and password:
        success, user_info, message = AuthService.login(username, password)

        if success:
            main_window = MainWindow()
            main_window.current_user = {
                "user_id": user_info['user_id'],
                "name": user_info['full_name'],
                "role": user_info['role']
            }
            main_window.setup_sidebar_by_role()
            main_window.update_ui_by_role()
            main_window.stacked_widget.setCurrentIndex(0)
            main_window.sidebar.setCurrentRow(0)
            main_window.show()

            return True
    return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if try_auto_login():
        sys.exit(app.exec())
    else:
        window = LoginWindow()
        window.show()
        sys.exit(app.exec())