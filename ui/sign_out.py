def sign_out(self):
    reply = QMessageBox.question(
        self,
        "Sign Out",
        "Are you sure you want to sign out?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )

    if reply == QMessageBox.StandardButton.Yes:
        print(f"User {self.current_user['name']} signed out")

        self.close()