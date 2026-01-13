from database.db_connection import db
import bcrypt

class AuthService:
    @staticmethod
    def register_user(data: dict) -> tuple[bool, str]:
        try:
            exists = db.execute_query(
                "SELECT 1 FROM Users WHERE username = ? OR email = ?",
                (data['username'], data['email']),
                fetch="one"
            )
            if exists:
                return False, "Username and email are already exists"

            # Hash password
            hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            hashed_str = hashed.decode('utf-8')

            query = """
            INSERT INTO Users (username, password, full_name, email, phone, role, status)
            VALUES (?, ?, ?, ?, ?, 'MEMBER', 'PENDING')
            """
            success = db.execute_query(query, (
                data['username'],
                hashed_str,
                data['full_name'],
                data['email'],
                data.get('phone'),
            ), commit=True)

            if success:
                return True, "Register Successfully, Waiting for Approval..."
            return False, "Register Failed"
        except Exception as e:
            print("Register error:", e)
            return False, f"System Error: {str(e)}"

    @staticmethod
    def login(username: str, password: str) -> tuple[bool, dict | None, str]:
        result = db.execute_query(
            "SELECT user_id, username, full_name, role, status, password FROM Users WHERE username = ?",
            (username,),
            fetch="one"
        )
        if not result:
            return False, None, "Account not exist"

        user_id, uname, full_name, role, status, hashed_pw = result

        if status != 'ACTIVE':
            return False, None, f"Account is not activated (status: {status})"

        if not bcrypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8')):
            return False, None, "Wrong password!"

        user_info = {
            'user_id': user_id,
            'username': uname,
            'full_name': full_name,
            'role': role
        }
        return True, user_info, "Sign In Successfully"