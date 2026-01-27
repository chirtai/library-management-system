import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
    QComboBox, QFrame, QGridLayout, QMainWindow, QTabWidget, QStyledItemDelegate, QAbstractItemView
)
from PyQt6.QtCore import Qt
from logic.fine_payment import FinesController
from logic.fine_payment import PaymentsController

class CenterDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter

class MainApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Library Management System")
        self.resize(1000, 700)

        # Create central widget and QTabWidget
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        # Add "Fine Management" Tab
        self.fines_tab = FinesInterface()
        self.central_widget.addTab(self.fines_tab, "Fine Management")

        # Add "Payment Management" Tab
        self.payments_tab = PaymentsInterface() 
        self.central_widget.addTab(self.payments_tab, "Payment Management")

        # Other tabs can be added here
        # self.central_widget.addTab(QWidget(), "Book Management")
        # self.central_widget.addTab(QWidget(), "Member Management")

class FinesInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

        self.controller = FinesController(self)
        
        # Connect button events to logic file functions
        self.btn_add.clicked.connect(self.controller.add_fine)
        self.btn_update.clicked.connect(self.controller.update_fine)
        self.btn_delete.clicked.connect(self.controller.delete_fine)
        self.btn_clear.clicked.connect(self.controller.clear_form)
        
        # Load data on startup
        self.controller.load_data()
        
        # Table click event to populate form
        self.table.itemClicked.connect(self.display_selected_row)

    def display_selected_row(self, item):
        row = item.row()
        self.txt_borrow_id.setText(self.table.item(row, 2).text())
        self.txt_borrow_id.setReadOnly(True) # Prevent editing foreign key during update
        self.txt_amount.setText(self.table.item(row, 3).text())
        self.txt_reason.setText(self.table.item(row, 4).text())
        
        status_text = self.table.item(row, 5).text()
        self.cb_status.setCurrentText(status_text)

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # --- 1. Title ---
        self.label_title = QLabel("FINE MANAGEMENT")
        self.label_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2E7D32;")
        self.main_layout.addWidget(self.label_title)

        # --- 2. Input Area (Form) ---
        input_frame = QFrame()
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
        input_layout.addWidget(QLabel("Borrow ID:"), 0, 0)
        self.txt_borrow_id = QLineEdit()
        input_layout.addWidget(self.txt_borrow_id, 0, 1)

        input_layout.addWidget(QLabel("Amount (VND):"), 0, 2)
        self.txt_amount = QLineEdit()
        input_layout.addWidget(self.txt_amount, 0, 3)

        input_layout.addWidget(QLabel("Reason:"), 1, 0)
        self.txt_reason = QLineEdit()
        input_layout.addWidget(self.txt_reason, 1, 1, 1, 3)

        input_layout.addWidget(QLabel("Status:"), 2, 0)
        self.cb_status = QComboBox()
        self.cb_status.addItems(["UNPAID", "PAID"])
        input_layout.addWidget(self.cb_status, 2, 1)

        self.main_layout.addWidget(input_frame)

        # --- 3. Toolbar (Buttons with Hover effects) ---
        button_layout = QHBoxLayout()
        
        self.btn_add = QPushButton("Add Fine")
        self.btn_update = QPushButton("Update")
        self.btn_delete = QPushButton("Delete")
        self.btn_clear = QPushButton("Clear Form")

        # Apply Style Sheets
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

        # --- 4. Display Table ---
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Fine ID", "Member ID", "Borrow ID", "Amount", "Reason", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setItemDelegate(CenterDelegate(self.table))
        self.table.setStyleSheet("""
            QTableWidget { background-color: white; border: 1px solid #ddd; }
            QHeaderView::section { background-color: #ffffff; font-weight: bold; }
        """)

        self.main_layout.addWidget(self.table)


class PaymentsInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

        self.controller = PaymentsController(self)

        # Connect events
        self.btn_check_info.clicked.connect(self.controller.check_borrow_info)
        self.btn_pay.clicked.connect(self.controller.process_payment)
        self.btn_refresh.clicked.connect(self.controller.clear_form)
        self.btn_delete.clicked.connect(self.controller.delete_payment)
        self.btn_search.clicked.connect(self.controller.search_payments)
        self.txt_search_input.returnPressed.connect(self.controller.search_payments)

        # Set auto-fill fields to ReadOnly
        self.txt_fine_id.setReadOnly(True)
        self.txt_base_fee.setReadOnly(True)
        self.txt_total_pay.setReadOnly(True)

        # Load initial data
        self.controller.load_payments_history()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # --- 1. Title ---
        self.label_title = QLabel("PAYMENT PROCESSING")
        self.label_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1565C0;")
        self.main_layout.addWidget(self.label_title)

        # --- 2. Smart Input Area ---
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

        # Row 1: Borrow ID and Check button
        form_layout.addWidget(QLabel("Borrow ID:"), 0, 0)
        self.txt_borrow_id = QLineEdit()
        self.txt_borrow_id.setPlaceholderText("Enter ID and press Enter or Check...")
        form_layout.addWidget(self.txt_borrow_id, 0, 1)
        
        self.btn_check_info = QPushButton("Check Information")
        self.btn_check_info.setStyleSheet("background-color: #34495e; color: white; padding: 6px; font-weight: bold;")
        form_layout.addWidget(self.btn_check_info, 0, 2)

        # Row 2: Staff and Fine info
        form_layout.addWidget(QLabel("Staff ID:"), 1, 0)
        self.txt_staff_id = QLineEdit() 
        form_layout.addWidget(self.txt_staff_id, 1, 1)

        form_layout.addWidget(QLabel("Fine ID (if any):"), 1, 2)
        self.txt_fine_id = QLineEdit()
        form_layout.addWidget(self.txt_fine_id, 1, 3)

        # Row 3: Fees
        form_layout.addWidget(QLabel("Base Fee:"), 2, 0)
        self.txt_base_fee = QLineEdit() 
        self.txt_base_fee.setPlaceholderText("Default fee...")
        form_layout.addWidget(self.txt_base_fee, 2, 1)

        form_layout.addWidget(QLabel("Additional Fine:"), 2, 2)
        self.txt_fine_amount = QLineEdit()
        self.txt_fine_amount.setText("0")
        form_layout.addWidget(self.txt_fine_amount, 2, 3)

        # Row 4: Total and Method
        form_layout.addWidget(QLabel("TOTAL PAYMENT:"), 3, 0)
        self.txt_total_pay = QLineEdit()
        self.txt_total_pay.setStyleSheet("font-weight: bold; color: #e74c3c; font-size: 14px;")
        form_layout.addWidget(self.txt_total_pay, 3, 1)

        form_layout.addWidget(QLabel("Payment Method:"), 3, 2)
        self.cb_method = QComboBox()
        self.cb_method.addItems(["CASH", "BANK", "MOMO", "CARD"])
        self.cb_method.setStyleSheet("padding: 5px; border: 1px solid #bdc3c7;")
        form_layout.addWidget(self.cb_method, 3, 3)

        self.main_layout.addWidget(input_frame)

        # --- 3. Functional Navigation ---
        button_layout = QHBoxLayout()
        self.btn_pay = QPushButton("Confirm Payment")
        self.btn_delete = QPushButton("Delete Record")
        self.btn_search = QPushButton("Search History")
        self.btn_refresh = QPushButton("Refresh")

        self.txt_search_input = QLineEdit()
        self.txt_search_input.setPlaceholderText("Enter Borrow ID or TXN No...")
        self.txt_search_input.setFixedWidth(250)

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

        # --- 4. Display Table ---
        self.table_payments = QTableWidget(0, 9)
        self.table_payments.setHorizontalHeaderLabels([
            "Payment ID", "Member ID", "Payment Day", "Borrow ID",  
            "Fine ID", "Total Amount", "Method", "Staff ID", "TXN No."
        ])
        
        header = self.table_payments.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_payments.verticalHeader().setVisible(False)
        self.table_payments.setShowGrid(False)
        self.table_payments.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_payments.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_payments.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_payments.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table_payments.setItemDelegate(CenterDelegate(self.table_payments))
        self.table_payments.setStyleSheet("""
            QTableWidget { background-color: white; border: 1px solid #ddd; }
            QHeaderView::section { background-color: #ffffff; font-weight: bold;}
        """)
        self.main_layout.addWidget(self.table_payments)