import sys
#for VSCode
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pathlib import Path
import keyring
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox, QCheckBox, QHBoxLayout,
    QDialog, QFormLayout
)
from PyQt6.QtCore import Qt
from logic.login import Login
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
        pass_reset_btn = QPushButton("Forgot Password?")
        pass_reset_btn.setObjectName("passwordResetButton")
        pass_reset_btn.clicked.connect(self.show_forgot_password)
        bottom_layout.addWidget(pass_reset_btn, alignment=Qt.AlignmentFlag.AlignRight)
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

    # Password Reset
    def show_forgot_password(self):
        dialog = ForgotPasswordDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if dialog.result:
                from logic.login import Login

                success, message = Login.reset_password(
                    dialog.result["username"],
                    dialog.result["new_password"]
                )

                if success:
                    QMessageBox.information(self, "Success", message)
                else:
                    QMessageBox.warning(self, "Failed", message)

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
        success, user_info, message = Login.login(username, password)
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
        success, user_info, message = Login.login(username, password)

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

class ForgotPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reset Password")
        self.setMinimumWidth(450)
        self.result = None

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.setSpacing(12)

        self.username_edit = QLineEdit()
        self.new_password_edit = QLineEdit()
        self.new_password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Username:", self.username_edit)
        form_layout.addRow("New Password:", self.new_password_edit)
        form_layout.addRow("Confirm New Password:", self.confirm_password_edit)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.btn_confirm = QPushButton("Reset Password")
        self.btn_cancel = QPushButton("Cancel")

        self.btn_confirm.setDefault(True)
        self.btn_confirm.clicked.connect(self.validate_and_accept)
        self.btn_cancel.clicked.connect(self.reject)

        button_layout.addWidget(self.btn_confirm)
        button_layout.addWidget(self.btn_cancel)

        layout.addLayout(button_layout)
        layout.addStretch()

    def validate_and_accept(self):
        username = self.username_edit.text().strip()
        new_pass = self.new_password_edit.text()
        confirm_pass = self.confirm_password_edit.text()

        if not username:
            QMessageBox.warning(self, "Error", "Please enter your username!")
            return

        if not new_pass:
            QMessageBox.warning(self, "Error", "Please enter your new password!")
            return

        if len(new_pass) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 8 characters!")
            return

        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Error", "Password don't match!")
            return

        self.result = {
            "username": username,
            "new_password": new_pass
        }
        self.accept()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    if try_auto_login():
        sys.exit(app.exec())
    else:
        window = LoginWindow()
        window.show()
        sys.exit(app.exec())