import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox,
    QCheckBox, QHBoxLayout, QComboBox,
    QDateEdit, QRadioButton, QButtonGroup,
    QGridLayout, QCalendarWidget
)
from PyQt6.QtCore import Qt, QDate
from logic.auth_service import AuthService

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.resize(1000, 750)

        # Load QSS
        BASE_DIR = Path(__file__).resolve().parent.parent
        QSS_PATH = BASE_DIR / "styles" / "register.qss"

        try:
            with open(QSS_PATH, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Warning: main.qss not found:", e)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title = QLabel("Create Account")
        main_layout.addWidget(title)
        title.setObjectName("registerTitle")

        # Form Container
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)

        # Full Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Full Name:")
        name_label.setObjectName("formLabel")
        name_label.setMinimumWidth(120)
        name_layout.addWidget(name_label)

        self.input_firstname = QLineEdit()
        self.input_firstname.setObjectName("firstNameInput")
        self.input_firstname.setPlaceholderText("First Name")
        name_layout.addWidget(self.input_firstname)

        self.input_lastname = QLineEdit()
        self.input_lastname.setObjectName("lastNameInput")
        self.input_lastname.setPlaceholderText("Last Name")
        name_layout.addWidget(self.input_lastname)
        form_layout.addLayout(name_layout)

        # Email
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        email_label.setObjectName("formLabel")
        email_label.setMinimumWidth(120)
        email_layout.addWidget(email_label)

        self.input_email = QLineEdit()
        self.input_email.setObjectName("emailInput")
        self.input_email.setPlaceholderText("Email")
        email_layout.addWidget(self.input_email, 1)

        form_layout.addLayout(email_layout)

        # Phone
        phone_layout = QHBoxLayout()
        phone_label = QLabel("Phone:")
        phone_label.setObjectName("formLabel")
        phone_label.setMinimumWidth(120)
        phone_layout.addWidget(phone_label)

        self.input_phone = QLineEdit()
        self.input_phone.setObjectName("phoneInput")
        self.input_phone.setPlaceholderText("Phone Number")
        phone_layout.addWidget(self.input_phone, 1)
        form_layout.addLayout(phone_layout)

        # Date of Birth
        dob_layout = QHBoxLayout()
        dob_label = QLabel("Date of Birth:")
        dob_label.setObjectName("formLabel")
        dob_label.setMinimumWidth(120)
        dob_layout.addWidget(dob_label)

        self.input_dob = QDateEdit()
        self.input_dob.setObjectName("dobInput")
        self.input_dob.setCalendarPopup(True)

        self.input_dob.setMinimumDate(QDate(1900, 1, 1))
        self.input_dob.setMaximumDate(QDate.currentDate())

        dob_layout.addWidget(self.input_dob, 1)
        form_layout.addLayout(dob_layout)

        # Gender
        gender_layout = QHBoxLayout()
        gender_label = QLabel("Gender:")
        gender_label.setObjectName("formLabel")
        gender_label.setMinimumWidth(120)
        gender_layout.addWidget(gender_label)

        self.gender_group = QButtonGroup(self)

        self.radio_male = QRadioButton("Male")
        self.radio_male.setObjectName("genderRadio")
        self.gender_group.addButton(self.radio_male)

        self.radio_female = QRadioButton("Female")
        self.radio_female.setObjectName("genderRadio")
        self.gender_group.addButton(self.radio_female)

        self.radio_other = QRadioButton("Other")
        self.radio_other.setObjectName("genderRadio")
        self.gender_group.addButton(self.radio_other)

        gender_layout.addWidget(self.radio_male)
        gender_layout.addWidget(self.radio_female)
        gender_layout.addWidget(self.radio_other)
        gender_layout.addStretch()
        form_layout.addLayout(gender_layout)

        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setObjectName("formLabel")
        username_label.setMinimumWidth(120)
        username_layout.addWidget(username_label)

        self.input_username = QLineEdit()
        self.input_username.setObjectName("usernameInput")
        self.input_username.setPlaceholderText("Choose a username")
        username_layout.addWidget(self.input_username, 1)
        form_layout.addLayout(username_layout)

        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setObjectName("formLabel")
        password_label.setMinimumWidth(120)
        password_layout.addWidget(password_label)

        self.input_password = QLineEdit()
        self.input_password.setObjectName("passwordInput")
        self.input_password.setPlaceholderText("At least 8 characters")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.input_password, 1)
        form_layout.addLayout(password_layout)

        # Confirm Password
        confirm_layout = QHBoxLayout()
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setObjectName("formLabel")
        confirm_label.setMinimumWidth(120)
        confirm_layout.addWidget(confirm_label)

        self.input_confirm = QLineEdit()
        self.input_confirm.setObjectName("confirmInput")
        self.input_confirm.setPlaceholderText("Re-enter your password")
        self.input_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        confirm_layout.addWidget(self.input_confirm, 1)

        form_layout.addLayout(confirm_layout)

        # Add form to main layout
        main_layout.addLayout(form_layout)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Back to Login button
        btn_back = QPushButton("Back to Login")
        btn_back.clicked.connect(self.back_to_login)
        btn_back.setObjectName("backButton")
        buttons_layout.addWidget(btn_back)
        buttons_layout.addStretch()

        # Register button
        btn_register = QPushButton("Create Account")
        btn_register.clicked.connect(self.handle_register)
        btn_register.setObjectName("registerSubmitButton")
        btn_register.setMinimumHeight(45)
        buttons_layout.addWidget(btn_register)
        main_layout.addLayout(buttons_layout)

    def back_to_login(self):
        from login_ui import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def handle_register(self):
        first_name = self.input_firstname.text().strip()
        last_name = self.input_lastname.text().strip()
        full_name = f"{first_name} {last_name}".strip()

        email = self.input_email.text().strip()
        phone = self.input_phone.text().strip()
        username = self.input_username.text().strip()
        password = self.input_password.text()
        confirm = self.input_confirm.text()

        # Lấy giới tính
        gender = None
        if self.radio_male.isChecked():
            gender = "Male"
        elif self.radio_female.isChecked():
            gender = "Female"
        elif self.radio_other.isChecked():
            gender = "Other"

        dob = self.input_dob.date().toString("yyyy-MM-dd")

        # Validation cơ bản
        if not all([full_name, email, username, password]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ các trường bắt buộc!")
            return

        if password != confirm:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp!")
            return

        if len(password) < 8:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu phải ít nhất 8 ký tự!")
            return

        # Chuẩn bị data gửi đi register
        data = {
            'username': username,
            'password': password,
            'full_name': full_name,
            'email': email,
            'phone': phone if phone else None,
            # có thể thêm gender, dob nếu bạn sửa bảng Users
        }

        success, message = AuthService.register_user(data)

        if success:
            QMessageBox.information(self, "Thành công", message)
            self.back_to_login()  # quay về login
        else:
            QMessageBox.warning(self, "Đăng ký thất bại", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec())