import pyodbc

class Database:
    def __init__(self):
        self.conn_str = (
            r"DRIVER={ODBC Driver 17 for SQL Server};"
            r"SERVER=localhost\SQLEXPRESS;"    
            r"DATABASE=LibraryManagement;"
            r"Trusted_Connection=yes;"
        )
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = pyodbc.connect(self.conn_str)
            self.cursor = self.conn.cursor()
            print("Connected to database!")
        except Exception as e:
            print("Database connection error!", e)
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
                return True

            elif fetch == "one":
                return self.cursor.fetchone()
            elif fetch:
                return self.cursor.fetchall()  # list of tuples
            else:
                return True
        except Exception as e:
            print("Error", e)
            self.conn.rollback()
            return None

    def __del__(self):
        self.disconnect()
db = Database()