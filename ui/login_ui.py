import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox, QCheckBox, QHBoxLayout,
)
from PyQt6.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.resize(500, 500)

        # Load QSS
        try:
            with open("login.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Warning: login.qss not found or invalid.")

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
        username = self.input_username.text()
        password = self.input_password.text()

    def check_create_account(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())