from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit,
    QPushButton, QGridLayout, QHBoxLayout
)

class BookDialog(QDialog):
    def __init__(self, parent=None, book=None):
        super().__init__(parent)
        self.setWindowTitle("Book Information")
        self.resize(350, 200)

        layout = QGridLayout(self)
        self.inputs = {}

        fields = ["Title", "Author", "Category", "Publisher", "Year"]
        for i, field in enumerate(fields):
            layout.addWidget(QLabel(field), i, 0)
            edit = QLineEdit()
            layout.addWidget(edit, i, 1)
            self.inputs[field.lower()] = edit

        if book:
            for k, v in book.items():
                if k in self.inputs:
                    self.inputs[k].setText(str(v))

        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("Save")
        btn_cancel = QPushButton("Cancel")

        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout, len(fields), 0, 1, 2)

    def get_data(self):
        return {k: v.text() for k, v in self.inputs.items()}
