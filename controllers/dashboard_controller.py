"""
Dashboard Controller — Điều phối dữ liệu tổng quan cho trang Dashboard
"""
from datetime import date


class DashboardController:
    def __init__(self, book_model, member_model, borrow_model):
        self.book_model = book_model
        self.member_model = member_model
        self.borrow_model = borrow_model

    def get_dashboard_data(self):
        inv = self.book_model.get_inventory_stats()
        b_cnt = inv["c"]
        b_total = inv["tot"]
        b_avail = inv["av"]
        b_borrowed = max(0, b_total - b_avail)

        m_cnt = self.member_model.count()
        br_cnt = self.borrow_model.count()

        recent_rows = self.borrow_model.get_recent(8)
        today = date.today().strftime("%Y-%m-%d")
        for r in recent_rows:
            is_overdue = r["status"] == "borrowed" and str(r["due_date"]) < today
            r["display_status"] = "Quá hạn" if is_overdue else ("Đang mượn" if r["status"] == "borrowed" else "Đã trả")

        return {
            "books_count": b_cnt,
            "books_total": b_total,
            "books_available": b_avail,
            "books_borrowed": b_borrowed,
            "members_count": m_cnt,
            "borrows_count": br_cnt,
            "recent_borrows": recent_rows
        }
