from database.db_connection import db

class Member:
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
        SET status = 'INACTIVE', 
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