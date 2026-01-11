def sign_out(self):
    """Xử lý đăng xuất"""
    reply = QMessageBox.question(
        self,
        "Đăng xuất",
        "Bạn có chắc muốn đăng xuất không?\nTất cả session sẽ bị xóa.",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )

    if reply == QMessageBox.StandardButton.Yes:
        # TODO: Xóa session, token, lưu "remember me" nếu cần
        print(f"User {self.current_user['name']} signed out")

        # Đóng MainWindow và mở LoginWindow
        self.close()

        # Mở lại Login (nếu bạn có file login_ui.py)
        # from login_ui import LoginWindow
        # login_window = LoginWindow()
        # login_window.show()

        # Hoặc chỉ thoát app
        # QApplication.quit()