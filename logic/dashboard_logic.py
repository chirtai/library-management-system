# logic/dashboard_logic.py

class DashboardLogic:
    def __init__(self):
        pass

    # ===== SUMMARY CARDS =====
    def get_summary_stats(self):
        return {
            "total_books": 1247,
            "borrowed": 156,
            "overdue": 23,
            "members": 482,
            "available": 800,
            "fines": 1_850_000
        }

    # ===== LINE CHART =====
    def get_borrowing_trends(self):
        return {
            "months": [
                "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
            ],
            "values": [85, 92, 110, 105, 130, 145, 160, 152, 138, 125, 115, 140]
        }

    # ===== BAR CHART =====
    def get_books_by_category(self):
        return {
            "categories": ["Fiction", "Science", "History", "Tech", "Other"],
            "values": [420, 280, 190, 150, 97]
        }
