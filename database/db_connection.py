import pyodbc

class Database:
    def __init__(self):
        # Thay đổi thông tin kết nối theo máy bạn
        self.conn_str = (
            r"DRIVER={ODBC Driver 17 for SQL Server};"
            r"SERVER=localhost\SQLEXPRESS;"               # hoặc tên server của bạn (.\SQLEXPRESS, IP,...)
            r"DATABASE=LibraryManagement;"
            r"Trusted_Connection=yes;"         # dùng Windows Authentication
            # Nếu dùng SQL Authentication thì thay bằng:
            # r"UID=sa;PWD=your_password;"
        )
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = pyodbc.connect(self.conn_str)
            self.cursor = self.conn.cursor()
            print("Kết nối SQL Server thành công!")
        except Exception as e:
            print("Lỗi kết nối database:", e)
            return False
        return True

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=None, fetch=False, commit=False):
        if not self.conn:
            if not self.connect():
                return None

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            if commit:
                self.conn.commit()

            if fetch:
                return self.cursor.fetchall()
            elif fetch == "one":
                return self.cursor.fetchone()
            return True
        except Exception as e:
            print("Lỗi truy vấn:", e)
            self.conn.rollback()
            return None

    def __del__(self):
        self.disconnect()

# Tạo instance dùng chung (singleton style)
db = Database()