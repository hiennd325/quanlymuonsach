"""
Member Model — Quản lý dữ liệu bạn đọc trong cơ sở dữ liệu
"""


class MemberModel:
    def __init__(self, db):
        self.db = db

    def get_all(self, keyword=None):
        if keyword:
            raw_kw = keyword.strip()
            kw = f"%{raw_kw}%"
            sql = "SELECT * FROM members WHERE CAST(id AS CHAR) = %s OR name LIKE %s OR phone LIKE %s OR email LIKE %s ORDER BY id DESC"
            return self.db.query(sql, (raw_kw, kw, kw, kw))
        return self.db.query("SELECT * FROM members ORDER BY id DESC")

    def get_all_with_active_borrows(self, keyword=None):
        members = self.get_all(keyword)
        for m in members:
            res = self.db.query(
                "SELECT COUNT(*) as cnt FROM borrows WHERE member_id=%s AND status='borrowed'",
                (m["id"],)
            )
            m["active_borrows"] = res[0]["cnt"] if res else 0
        return members

    def get_by_id(self, member_id):
        rows = self.db.query("SELECT * FROM members WHERE id=%s", (member_id,))
        return rows[0] if rows else None

    def add(self, name, email, phone):
        sql = "INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)"
        return self.db.execute(sql, (name, email, phone))

    def delete(self, member_id):
        return self.db.execute("DELETE FROM members WHERE id=%s", (member_id,))

    def count(self):
        res = self.db.query("SELECT COUNT(*) as c FROM members")
        return res[0]["c"] if res else 0
