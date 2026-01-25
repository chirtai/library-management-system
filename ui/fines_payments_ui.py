import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
    QComboBox, QFrame, QGridLayout, QMainWindow, QTabWidget
)
from PyQt6.QtCore import Qt
from logic.fine_payment import FinesController
from logic.fine_payment import PaymentsController

class MainApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hệ Thống Quản Lý Thư Viện")
        self.resize(1000, 700)

        # Tạo widget trung tâm và QTabWidget
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        # Thêm Tab "Quản lý Phiếu phạt" từ class của bạn
        self.fines_tab = FinesInterface()
        self.central_widget.addTab(self.fines_tab, "Quản lý Phiếu phạt")

        self.payments_tab = PaymentsInterface() 
        self.central_widget.addTab(self.payments_tab, "Quản lý Thanh toán")

        # Bạn có thể thêm các Tab khác ở đây
        # self.central_widget.addTab(QWidget(), "Quản lý Sách")
        # self.central_widget.addTab(QWidget(), "Quản lý Thành viên")

class FinesInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

        self.controller = FinesController(self)
        
        # Kết nối sự kiện nút bấm với hàm trong file logic
        self.btn_add.clicked.connect(self.controller.add_fine)
        self.btn_update.clicked.connect(self.controller.update_fine)
        self.btn_delete.clicked.connect(self.controller.delete_fine)
        self.btn_clear.clicked.connect(self.controller.clear_form)
        
        # Tải dữ liệu khi mở ứng dụng
        self.controller.load_data()
        
        # Sự kiện click vào bảng để đổ ngược dữ liệu lên form
        self.table.itemClicked.connect(self.display_selected_row)

    def display_selected_row(self, item):
        row = item.row()
        self.txt_borrow_id.setText(self.table.item(row, 2).text())
        self.txt_borrow_id.setReadOnly(True) # Không cho sửa khóa ngoại khi đang cập nhật
        self.txt_amount.setText(self.table.item(row, 3).text())
        self.txt_reason.setText(self.table.item(row, 4).text())
        
        status_text = self.table.item(row, 5).text()
        self.cb_status.setCurrentText(status_text)

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # --- 1. Tiêu đề ---
        self.label_title = QLabel("QUẢN LÝ PHIẾU PHẠT")
        self.label_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2E7D32;")
        self.main_layout.addWidget(self.label_title)

        # --- 2. Khu vực Nhập liệu (Form) ---
        input_frame = QFrame()
        # Đổi màu nền frame và các ô nhập liệu để không bị trùng
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff; 
                border-radius: 8px; 
                border: 1px solid #e0e0e0;
            }
            QLabel {
                border: none;
                color: #555555;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                background-color: #fcfcfc;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 6px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
                background-color: #ffffff;
            }
        """)
        
        input_layout = QGridLayout(input_frame)
        input_layout.addWidget(QLabel("Mã mượn (Borrow ID):"), 0, 0)
        self.txt_borrow_id = QLineEdit()
        input_layout.addWidget(self.txt_borrow_id, 0, 1)

        input_layout.addWidget(QLabel("Số tiền (VND):"), 0, 2)
        self.txt_amount = QLineEdit()
        input_layout.addWidget(self.txt_amount, 0, 3)

        input_layout.addWidget(QLabel("Lý do:"), 1, 0)
        self.txt_reason = QLineEdit()
        input_layout.addWidget(self.txt_reason, 1, 1, 1, 3)

        input_layout.addWidget(QLabel("Trạng thái:"), 2, 0)
        self.cb_status = QComboBox()
        self.cb_status.addItems(["UNPAID", "PAID"])
        input_layout.addWidget(self.cb_status, 2, 1)

        self.main_layout.addWidget(input_frame)

        # --- 3. Thanh công cụ (Buttons với hiệu ứng Hover) ---
        button_layout = QHBoxLayout()
        
        self.btn_add = QPushButton("Thêm phiếu phạt")
        self.btn_update = QPushButton("Cập nhật")
        self.btn_delete = QPushButton("Xóa")
        self.btn_clear = QPushButton("Làm mới Form")

        # Áp dụng Style Sheet cho các nút (bao gồm Hover)
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; color: white; border-radius: 5px; padding: 8px 15px; font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.btn_update.setStyleSheet("""
            QPushButton {
                background-color: #2196F3; color: white; border-radius: 5px; padding: 8px 15px; font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1e88e5;
            }
        """)
        
        self.btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #F44336; color: white; border-radius: 5px; padding: 8px 15px; font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)

        self.btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #81c784; color: white; border-radius: 5px; padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #66bb6a;
            }
        """)
        
        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_update)
        button_layout.addWidget(self.btn_delete)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_clear)
        self.main_layout.addLayout(button_layout)

        # --- 4. Bảng hiển thị ---
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Fine ID", "Member ID", "Borrow ID", "Amount", "Reason", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget { background-color: white; border: 1px solid #ddd; }
            QHeaderView::section { background-color: #f2f2f2; font-weight: bold; }
        """)
        self.main_layout.addWidget(self.table)


class PaymentsInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

        self.controller = PaymentsController(self)
        
        # Kết nối sự kiện
        self.btn_check_info.clicked.connect(self.controller.check_borrow_info)
        self.btn_pay.clicked.connect(self.controller.process_payment)
        self.btn_refresh.clicked.connect(self.controller.clear_form)
        self.btn_delete.clicked.connect(self.controller.delete_payment)
        self.btn_search.clicked.connect(self.controller.search_payments)    
        self.txt_search_input.returnPressed.connect(self.controller.search_payments)
        
        # Thiết lập các ô tự động điền là ReadOnly để tránh sai sót
        self.txt_fine_id.setReadOnly(True)
        self.txt_base_fee.setReadOnly(True)
        self.txt_total_pay.setReadOnly(True)

        # Load dữ liệu ban đầu
        self.controller.load_payments_history()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # --- 1. Tiêu đề ---
        self.label_title = QLabel("XỬ LÝ THANH TOÁN CHI PHÍ")
        self.label_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1565C0;")
        self.main_layout.addWidget(self.label_title)

        # --- 2. Khu vực Nhập liệu thông minh ---
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame { background-color: #ffffff; border-radius: 10px; border: 1px solid #dcdde1; }
            QLabel { color: #2f3640; font-weight: bold; border: none; }
            QLineEdit { border: 1px solid #bdc3c7; border-radius: 4px; padding: 6px; background-color: #f5f6fa; }
            QLineEdit:focus { border: 2px solid #3498db; background-color: #ffffff; }
        """)
        
        form_layout = QGridLayout(input_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)

        # Dòng 1: Nhập Borrow ID và nút Kiểm tra
        form_layout.addWidget(QLabel("Mã Mượn (Borrow ID):"), 0, 0)
        self.txt_borrow_id = QLineEdit()
        self.txt_borrow_id.setPlaceholderText("Nhập ID và nhấn Enter hoặc Kiểm tra...")
        form_layout.addWidget(self.txt_borrow_id, 0, 1)
        
        self.btn_check_info = QPushButton("Kiểm tra thông tin")
        self.btn_check_info.setStyleSheet("background-color: #34495e; color: white; padding: 6px; font-weight: bold;")
        form_layout.addWidget(self.btn_check_info, 0, 2)

        # Dòng 2: Thông tin Member và Fine (Tự động điền - Read only hoặc chỉnh sửa nếu cần)
        form_layout.addWidget(QLabel("Mã Nhân viên (Staff ID):"), 1, 0)
        self.txt_staff_id = QLineEdit() 
        form_layout.addWidget(self.txt_staff_id, 1, 1)

        form_layout.addWidget(QLabel("Mã Phiếu Phạt (nếu có):"), 1, 2)
        self.txt_fine_id = QLineEdit()
        form_layout.addWidget(self.txt_fine_id, 1, 3)

        # Dòng 3: Các loại chi phí
        form_layout.addWidget(QLabel("Tiền mượn sách (Gốc):"), 2, 0)
        self.txt_base_fee = QLineEdit() 
        self.txt_base_fee.setPlaceholderText("Tiền mặc định...")
        form_layout.addWidget(self.txt_base_fee, 2, 1)

        form_layout.addWidget(QLabel("Tiền phạt cộng thêm:"), 2, 2)
        self.txt_fine_amount = QLineEdit()
        self.txt_fine_amount.setText("0")
        form_layout.addWidget(self.txt_fine_amount, 2, 3)

        # Dòng 4: Tổng tiền và Phương thức
        form_layout.addWidget(QLabel("TỔNG THANH TOÁN:"), 3, 0)
        self.txt_total_pay = QLineEdit()
        self.txt_total_pay.setStyleSheet("font-weight: bold; color: #e74c3c; font-size: 14px;")
        form_layout.addWidget(self.txt_total_pay, 3, 1)

        form_layout.addWidget(QLabel("Phương thức trả:"), 3, 2)
        self.cb_method = QComboBox()
        self.cb_method.addItems(["CASH", "BANK", "MOMO", "CARD"])
        self.cb_method.setStyleSheet("padding: 5px; border: 1px solid #bdc3c7;")
        form_layout.addWidget(self.cb_method, 3, 3)

        self.main_layout.addWidget(input_frame)

        # --- 3. Thanh điều hướng chức năng ---
        button_layout = QHBoxLayout()
        self.btn_pay = QPushButton("Xác nhận Thanh toán")
        self.btn_delete = QPushButton("Xóa bản ghi")
        self.btn_search = QPushButton("Tìm kiếm lịch sử")
        self.btn_refresh = QPushButton("Làm mới")

        self.txt_search_input = QLineEdit()
        self.txt_search_input.setPlaceholderText("Nhập Borrow ID hoặc Mã GD để tìm...")
        self.txt_search_input.setFixedWidth(250) # Đặt chiều rộng cố định cho đẹp

        self.btn_pay.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; font-weight: bold; border-radius: 5px;")
        self.btn_delete.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px; font-weight: bold; border-radius: 5px;")
        self.btn_search.setStyleSheet("background-color: #2980b9; color: white; padding: 10px; font-weight: bold; border-radius: 5px;")
        self.btn_refresh.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px; border-radius: 5px;")

        button_layout.addWidget(self.btn_pay)
        button_layout.addWidget(self.btn_delete)
        button_layout.addWidget(self.txt_search_input)
        button_layout.addWidget(self.btn_search)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_refresh)
        self.main_layout.addLayout(button_layout)

        # --- 4. Bảng hiển thị (Đúng các cột bạn yêu cầu) ---
        self.table_payments = QTableWidget(0, 9)
        self.table_payments.setHorizontalHeaderLabels([
            "Payment ID", "Member ID", "Payment Day", "Borrow ID",  
            "Fine ID", "Total Amount", "Method", "Staff ID", "TXN No."
        ])
        
        # Cấu hình bảng chuyên nghiệp
        header = self.table_payments.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_payments.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_payments.setStyleSheet("""
            QTableWidget { background-color: white; border: 1px solid #ddd; gridline-color: #f0f0f0; }
            QHeaderView::section { background-color: #f8f9fa; font-weight: bold; border: 1px solid #ddd; }
        """)
        self.main_layout.addWidget(self.table_payments)