"""
Category Model — Quản lý danh mục thể loại sách trong cơ sở dữ liệu
"""


class CategoryModel:
    def __init__(self, db):
        self.db = db

    def get_all(self, keyword=None):
        if keyword:
            raw_kw = keyword.strip()
            kw = f"%{raw_kw}%"
            sql = """
                SELECT c.id, c.name, COUNT(b.id) AS book_count
                FROM categories c
                LEFT JOIN books b ON b.category = c.name
                WHERE CAST(c.id AS CHAR) = %s OR c.name LIKE %s
                GROUP BY c.id, c.name
                ORDER BY c.name ASC
            """
            return self.db.query(sql, (raw_kw, kw))

        sql = """
            SELECT c.id, c.name, COUNT(b.id) AS book_count
            FROM categories c
            LEFT JOIN books b ON b.category = c.name
            GROUP BY c.id, c.name
            ORDER BY c.name ASC
        """
        return self.db.query(sql)

    def get_names(self):
        rows = self.db.query("SELECT name FROM categories ORDER BY name ASC")
        return [r["name"] for r in rows]

    def get_by_id(self, cat_id):
        rows = self.db.query("SELECT * FROM categories WHERE id=%s", (cat_id,))
        return rows[0] if rows else None

    def get_by_name(self, name):
        rows = self.db.query("SELECT * FROM categories WHERE LOWER(name)=LOWER(%s)", (name.strip(),))
        return rows[0] if rows else None

    def add(self, name):
        sql = "INSERT INTO categories (name) VALUES (%s)"
        return self.db.execute(sql, (name.strip(),))

    def update(self, cat_id, new_name):
        old = self.get_by_id(cat_id)
        if not old:
            raise ValueError(f"Không tìm thấy thể loại với ID: {cat_id}")
        clean_new = new_name.strip()
        # Cập nhật tên ở bảng categories
        self.db.execute("UPDATE categories SET name=%s WHERE id=%s", (clean_new, cat_id))
        # Đồng bộ đổi tên ở bảng books nếu đang có sách dùng tên cũ
        self.db.execute("UPDATE books SET category=%s WHERE category=%s", (clean_new, old["name"]))
        return True

    def delete(self, cat_id):
        cat = self.get_by_id(cat_id)
        if not cat:
            raise ValueError(f"Không tìm thấy thể loại với ID: {cat_id}")
        # Kiểm tra xem có sách nào đang dùng thể loại này không
        check = self.db.query("SELECT COUNT(*) AS cnt FROM books WHERE category=%s", (cat["name"],))
        if check and check[0]["cnt"] > 0:
            raise ValueError(f"Không thể xóa thể loại '{cat['name']}' vì đang có {check[0]['cnt']} cuốn sách thuộc thể loại này.")
        return self.db.execute("DELETE FROM categories WHERE id=%s", (cat_id,))
