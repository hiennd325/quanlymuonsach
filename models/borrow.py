"""
Borrow Model — Quản lý các giao dịch mượn/trả sách trong cơ sở dữ liệu
"""
from datetime import datetime, date


class BorrowModel:
    def __init__(self, db, book_model=None):
        self.db = db
        self.book_model = book_model

    def get_all(self):
        sql = """
            SELECT b.id, m.name as member_name, bk.title as book_title,
                   b.borrow_date, b.due_date, b.return_date, b.status, b.fine_amount
            FROM borrows b
            JOIN members m ON b.member_id = m.id
            JOIN books bk ON b.book_id = bk.id
            ORDER BY b.id DESC
        """
        return self.db.query(sql)

    def get_recent(self, limit=8):
        sql = """
            SELECT b.id, m.name as member_name, bk.title as book_title,
                   b.borrow_date, b.due_date, b.status
            FROM borrows b
            JOIN members m ON b.member_id = m.id
            JOIN books bk ON b.book_id = bk.id
            ORDER BY b.id DESC LIMIT %s
        """
        return self.db.query(sql, (limit,))

    def get_by_id(self, borrow_id):
        rows = self.db.query("SELECT * FROM borrows WHERE id=%s", (borrow_id,))
        return rows[0] if rows else None

    def create_borrow(self, book_id, member_id, borrow_date_str, due_date_str):
        # Trừ số lượng sẵn có của sách
        sql_borrow = """
            INSERT INTO borrows (book_id, member_id, borrow_date, due_date, status)
            VALUES (%s, %s, %s, %s, 'borrowed')
        """
        borrow_id = self.db.execute(sql_borrow, (book_id, member_id, borrow_date_str, due_date_str))
        self.db.execute("UPDATE books SET available = available - 1 WHERE id=%s", (book_id,))
        return borrow_id

    def return_borrow(self, borrow_id, fine_per_day=5000):
        borrow = self.get_by_id(borrow_id)
        if not borrow:
            raise ValueError(f"Không tìm thấy phiếu mượn ID: {borrow_id}")
        if borrow["status"] == "returned":
            raise ValueError("Sách này đã được trả trước đó.")

        ret_date = date.today()
        # Chuyển due_date thành date object nếu là string hoặc date
        if isinstance(borrow["due_date"], str):
            due_date = datetime.strptime(borrow["due_date"], "%Y-%m-%d").date()
        else:
            due_date = borrow["due_date"]

        overdue_days = max(0, (ret_date - due_date).days)
        fine = overdue_days * fine_per_day

        ret_date_str = ret_date.strftime("%Y-%m-%d")
        sql = "UPDATE borrows SET return_date=%s, fine_amount=%s, status='returned' WHERE id=%s"
        self.db.execute(sql, (ret_date_str, fine, borrow_id))
        self.db.execute("UPDATE books SET available = available + 1 WHERE id=%s", (borrow["book_id"],))

        return {
            "borrow_id": borrow_id,
            "return_date": ret_date_str,
            "overdue_days": overdue_days,
            "fine_amount": fine
        }

    def get_overdue_list(self, today_str=None):
        if not today_str:
            today_str = date.today().strftime("%Y-%m-%d")
        sql = """
            SELECT b.id, m.name, m.email, bk.title, b.due_date
            FROM borrows b
            JOIN members m ON b.member_id = m.id
            JOIN books bk ON b.book_id = bk.id
            WHERE b.status = 'borrowed' AND b.due_date < %s
            ORDER BY b.due_date ASC
        """
        return self.db.query(sql, (today_str,))

    def get_due_or_overdue_today(self, today_str=None):
        if not today_str:
            today_str = date.today().strftime("%Y-%m-%d")
        sql = """
            SELECT m.name, m.email, bk.title, b.due_date
            FROM borrows b
            JOIN members m ON b.member_id = m.id
            JOIN books bk ON b.book_id = bk.id
            WHERE b.status = 'borrowed' AND b.due_date <= %s
        """
        return self.db.query(sql, (today_str,))

    def count(self):
        res = self.db.query("SELECT COUNT(*) as c FROM borrows")
        return res[0]["c"] if res else 0

    def get_total_fines(self):
        res = self.db.query("SELECT SUM(fine_amount) as s FROM borrows")
        val = res[0]["s"] if res else 0
        return val or 0
