from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QTabWidget, QPushButton, QLineEdit, QMessageBox, QInputDialog,
    QDialog, QFormLayout, QAbstractItemView, QStyledItemDelegate
)
from PyQt6.QtCore import Qt

from logic.members import Member

class CenterDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter

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

        # ---------- Tab 1: Approved Members -----------
        approved_tab = QWidget()
        approved_layout = QVBoxLayout(approved_tab)

        # Search + Filter bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Name, Phone Number, Email")
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(self.search_input, 1)
        approved_layout.addLayout(search_layout)

        self.approved_table = QTableWidget(0, 7)
        self.approved_table.setHorizontalHeaderLabels([
            "ID", "Full Name", "Email", "Phone Number", "Register Date", "Role", "Status"
        ])
        self.approved_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.approved_table.verticalHeader().setDefaultSectionSize(50)
        self.approved_table.verticalHeader().setVisible(False)
        self.approved_table.setShowGrid(False)
        self.approved_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.approved_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.approved_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.approved_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.approved_table.setItemDelegate(CenterDelegate(self.approved_table))
        approved_layout.addWidget(self.approved_table)

        # Edit/Delete Buttons
        action_layout_approved = QHBoxLayout()
        action_layout_approved.addStretch()
        self.edit_member_btn = QPushButton("Edit Member")
        self.delete_member_btn = QPushButton("Delete Member")
        self.edit_member_btn.setStyleSheet("background: #2e7dff; color: white; font-weight: bold;")
        self.delete_member_btn.setStyleSheet("background: #ff5f56; color: white; font-weight: bold;")
        self.edit_member_btn.setEnabled(False)
        self.delete_member_btn.setEnabled(False)
        action_layout_approved.addWidget(self.edit_member_btn)
        action_layout_approved.addWidget(self.delete_member_btn)
        approved_layout.addLayout(action_layout_approved)

        # Active when there a line is selected in table
        self.approved_table.itemSelectionChanged.connect(self.on_approved_selection_changed)

        # Connect Signal
        self.edit_member_btn.clicked.connect(self.edit_selected_member)
        self.delete_member_btn.clicked.connect(self.delete_selected_member)

        tabs.addTab(approved_tab, "Approved Members")

        # ------------ Tab 2: Pending Approvals ------------
        pending_tab = QWidget()
        pending_layout = QVBoxLayout(pending_tab)

        self.pending_table = QTableWidget(0, 6)
        self.pending_table.setHorizontalHeaderLabels([
            "ID", "Full Name", "Email", "Phone Number", "Register date", "Action"
        ])
        header = self.pending_table.horizontalHeader()
        for col in range(5):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

        self.pending_table.setColumnWidth(5, 220)
        self.pending_table.verticalHeader().setDefaultSectionSize(50)
        self.pending_table.verticalHeader().setVisible(False)
        self.pending_table.setShowGrid(False)

        self.pending_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.pending_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.pending_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.pending_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pending_table.setItemDelegate(CenterDelegate(self.pending_table))
        pending_layout.addWidget(self.pending_table)

        # Approve / Reject All Buttons
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        self.approve_all_btn = QPushButton("Approve All")
        self.reject_all_btn = QPushButton("Reject All")
        self.approve_all_btn.setStyleSheet("background: #2e7dff; color: white; font-weight: bold;")
        self.reject_all_btn.setStyleSheet("background: #ff5f56; color: white; font-weight: bold;")
        action_layout.addWidget(self.approve_all_btn)
        action_layout.addWidget(self.reject_all_btn)
        pending_layout.addLayout(action_layout)

        tabs.addTab(pending_tab, "Pending Members")

        main_layout.addWidget(tabs)

        # Connect Buttons
        self.approve_all_btn.clicked.connect(self.approve_all_pending)
        self.reject_all_btn.clicked.connect(self.reject_all_pending)

        # Load Data
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

                self.pending_table.setItem(row, 0, QTableWidgetItem(str(user_id)))
                self.pending_table.setItem(row, 1, QTableWidgetItem(full_name or ""))
                self.pending_table.setItem(row, 2, QTableWidgetItem(email or ""))
                self.pending_table.setItem(row, 3, QTableWidgetItem(phone or ""))
                self.pending_table.setItem(row, 4, QTableWidgetItem(reg_date or ""))
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
            btn_approve.setStyleSheet("background: #2e7dff; color: white; font-weight: bold;")
            btn_reject.setStyleSheet("background: #ff5f56; color: white; font-weight: bold;")
            btn_approve.setFixedWidth(100)
            btn_reject.setFixedWidth(90)

            btn_approve.clicked.connect(lambda checked, uid = user_id: self.approve_pending(uid))
            btn_reject.clicked.connect(lambda checked, uid = user_id: self.reject_pending(uid))

            hbox.addWidget(btn_approve)
            hbox.addWidget(btn_reject)
            hbox.addStretch(1)

            self.pending_table.setCellWidget(row, 5, action_widget)

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

# ------------ REJECT/APPROVE ------------
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

# ------------ EDIT/DELETE ---------------
    def get_selected_member_id(self):
        selected_rows = self.approved_table.selectionModel().selectedRows()
        row = selected_rows[0].row()
        id_item = self.approved_table.item(row, 0)
        if id_item and id_item.text().strip():
            try:
                return int(id_item.text())
            except ValueError:
                return None
        return None

    def on_approved_selection_changed(self):
        has_selection = self.approved_table.selectionModel().hasSelection()
        self.edit_member_btn.setEnabled(has_selection)
        self.delete_member_btn.setEnabled(has_selection)

    def delete_selected_member(self):
        user_id = self.get_selected_member_id()
        if user_id is None:
            return

        reply = QMessageBox.question(
            self,
            "Confirm",
            f"Are you sure to delete this member ID {user_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if Member.delete_member(user_id):
                QMessageBox.information(self, "Success", f"Deleted member ID {user_id}")
                self.load_approved_members()
            else:
                QMessageBox.critical(self, "Error", "Can't delete this member")

    def edit_selected_member(self):
        user_id = self.get_selected_member_id()
        if user_id is None:
            return

        member = Member.get_member_by_id(user_id)
        if not member:
            QMessageBox.critical(self, "Error", "Member ID not found.")
            return

        # Mở dialog chỉnh sửa
        dialog = MemberEditDialog(member, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_updated_data()

            if updated_data:
                success = Member.update_member(
                    user_id=user_id,
                    full_name=updated_data["full_name"],
                    email=updated_data["email"],
                    phone=updated_data["phone"],
                    role=updated_data["role"]
                )

                if success:
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Updated member ID {user_id}"
                    )
                    self.load_approved_members()
                else:
                    QMessageBox.critical(self, "Error", "Can't update this member")

# ------------ SEARCH -------------
    def filter_table(self):
        text = self.search_input.text().strip().lower()
        if not text:
            for r in range(self.approved_table.rowCount()):
                self.approved_table.setRowHidden(r, False)
            return

        for r in range(self.approved_table.rowCount()):
            name  = (self.approved_table.item(r, 1) or "").text().lower()
            email = (self.approved_table.item(r, 2) or "").text().lower()
            phone = (self.approved_table.item(r, 3) or "").text().lower()

            hide = not (text in name or text in phone or text in email)
            self.approved_table.setRowHidden(r, hide)

class MemberEditDialog(QDialog):
    def __init__(self, member_data: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Member Information")
        self.setMinimumWidth(450)

        self.member_data = member_data
        self.result = None

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.setSpacing(12)

        # Các trường nhập liệu
        self.full_name_edit = QLineEdit(self.member_data.get("full_name", ""))
        self.email_edit = QLineEdit(self.member_data.get("email", ""))
        self.phone_edit = QLineEdit(self.member_data.get("phone", ""))
        self.role_edit = QLineEdit(self.member_data.get("role", ""))

        self.full_name_edit.setObjectName("editMember")
        self.email_edit.setObjectName("editMember")
        self.phone_edit.setObjectName("editMember")
        self.role_edit.setObjectName("editMember")
        # Thêm vào form
        form_layout.addRow("Full Name:", self.full_name_edit)
        form_layout.addRow("Email:", self.email_edit)
        form_layout.addRow("Phone Number:", self.phone_edit)
        form_layout.addRow("Role:", self.role_edit)

        layout.addLayout(form_layout)

        # OK / Cancel Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.btn_ok = QPushButton("Save changes")
        self.btn_cancel = QPushButton("Cancel")

        self.btn_ok.setDefault(True)
        self.btn_ok.clicked.connect(self.validate_and_accept)
        self.btn_cancel.clicked.connect(self.reject)

        button_layout.addWidget(self.btn_ok)
        button_layout.addWidget(self.btn_cancel)

        layout.addLayout(button_layout)
        layout.addStretch()

    def validate_and_accept(self):
        full_name = self.full_name_edit.text().strip()
        email = self.email_edit.text().strip()
        phone = self.phone_edit.text().strip()
        role = self.role_edit.text().strip()

        if not full_name:
            QMessageBox.warning(self, "Error", "Full name can't be empty!")
            self.full_name_edit.setFocus()
            return

        if not email:
            QMessageBox.warning(self, "Error", "Email can't be empty!")
            self.email_edit.setFocus()
            return

        # Save new data
        self.result = {
            "full_name": full_name,
            "email": email,
            "phone": phone if phone else None,
            "role": role if role else None
        }

        self.accept()

    # Return new data
    def get_updated_data(self):
        return self.result