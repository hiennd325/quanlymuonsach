"""
Report Model — Cung cấp các thống kê và phân tích số liệu
"""


class ReportModel:
    def __init__(self, db):
        self.db = db

    def get_kpis(self):
        b_cnt = self.db.query("SELECT COUNT(*) as c FROM books")[0]["c"]
        m_cnt = self.db.query("SELECT COUNT(*) as c FROM members")[0]["c"]
        br_cnt = self.db.query("SELECT COUNT(*) as c FROM borrows")[0]["c"]
        fine_sum = self.db.query("SELECT SUM(fine_amount) as s FROM borrows")[0]["s"] or 0
        return {
            "books_count": b_cnt,
            "members_count": m_cnt,
            "borrows_count": br_cnt,
            "fines_total": int(fine_sum)
        }

    def get_top_books(self, limit=10):
        sql = """
            SELECT bk.title, COUNT(b.id) as cnt
            FROM borrows b
            JOIN books bk ON b.book_id = bk.id
            GROUP BY bk.id, bk.title
            ORDER BY cnt DESC
            LIMIT %s
        """
        return self.db.query(sql, (limit,))

    def get_top_categories(self, limit=10):
        sql = """
            SELECT bk.category, COUNT(b.id) as cnt
            FROM borrows b
            JOIN books bk ON b.book_id = bk.id
            GROUP BY bk.category
            ORDER BY cnt DESC
            LIMIT %s
        """
        return self.db.query(sql, (limit,))
