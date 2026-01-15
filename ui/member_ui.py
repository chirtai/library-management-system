from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QTabWidget, QPushButton, QLineEdit, QMessageBox, QInputDialog
)

from logic.members import Member

class MemberInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

# ------------ MEMBER MANAGEMENT INTERFACE ----------------
    def setup_ui(self):
        main_layout = QVBoxLayout(self)

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
