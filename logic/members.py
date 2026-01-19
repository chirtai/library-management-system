from database.db_connection import db

class Member:

# -------- APPROVE/REJECT ----------
    @staticmethod
    def get_pending_members():
        query = """
        SELECT 
            user_id, 
            full_name, 
            email, 
            phone, 
            CONVERT(varchar, created_at, 23) AS reg_date,
            ISNULL(reject_reason, '') AS reject_reason
        FROM Users 
        WHERE status = 'PENDING'
        ORDER BY created_at DESC
        """
        results = db.execute_query(query, fetch="all")
        return results or []

    @staticmethod
    def get_approved_members():
        query = """
        SELECT 
            user_id, 
            full_name, 
            email, 
            phone, 
            CONVERT(varchar, created_at, 23) AS reg_date,
            role,
            status
        FROM Users 
        WHERE status = 'ACTIVE'
        ORDER BY created_at DESC
        """
        return db.execute_query(query, fetch="all") or []

    @staticmethod
    def approve_member(user_id: int) -> bool:
        query = "UPDATE Users SET status = 'ACTIVE' WHERE user_id = ?"
        return db.execute_query(query, (user_id,), commit=True)

    @staticmethod
    def reject_member(user_id: int, reason: str = "") -> bool:
        query = """
        UPDATE Users 
        SET status = 'BLOCKED', 
            reject_reason = ?
        WHERE user_id = ?
        """
        return db.execute_query(query, (reason, user_id), commit=True)

    @staticmethod
    def approve_multiple_members(user_ids: list[int]) -> int:
        success_count = 0
        for uid in user_ids:
            if Member.approve_member(uid):
                success_count += 1
        return success_count

    @staticmethod
    def reject_multiple_members(user_ids: list[int], reason: str = "") -> int:
        success_count = 0
        for uid in user_ids:
            if Member.reject_member(uid, reason):
                success_count += 1
        return success_count

# ----------- EDIT/DELETE SELECTED MEMBER -----------
    @staticmethod
    def delete_member(user_id: int) -> bool:
        try:
            query = "DELETE FROM Users WHERE user_id = ?"
            success = db.execute_query(query, (user_id,), commit=True)
            return success
        except Exception as e:
            print(f"Error deleting member {user_id}: {str(e)}")
            return False

    @staticmethod
    def update_member(user_id: int,
                      full_name: str = None,
                      email: str = None,
                      phone: str = None,
                      role: str = None) -> bool:
        if not any([full_name, email, phone, role]):
            return False

        fields = []
        values = []

        if full_name is not None:
            fields.append("full_name = ?")
            values.append(full_name)
        if email is not None:
            fields.append("email = ?")
            values.append(email)
        if phone is not None:
            fields.append("phone = ?")
            values.append(phone)
        if role is not None:
            fields.append("role = ?")
            values.append(role)

        if not fields:
            return False

        query = f"""
            UPDATE Users 
            SET {', '.join(fields)}
            WHERE user_id = ?
            """

        values.append(user_id)

        try:
            success = db.execute_query(query, tuple(values), commit=True)
            return success
        except Exception as e:
            print(f"Error updating member {user_id}: {str(e)}")
            return False

    @staticmethod
    def get_member_by_id(user_id: int) -> dict | None:
        query = """
        SELECT 
            user_id, full_name, email, phone, role, status,
            CONVERT(varchar, created_at, 23) AS reg_date
        FROM Users 
        WHERE user_id = ?
        """
        result = db.execute_query(query, (user_id,), fetch="one")
        if result:
            keys = ["user_id", "full_name", "email", "phone", "role", "status", "reg_date"]
            return dict(zip(keys, result))
        return None