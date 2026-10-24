"""
Book Controller — Điều phối xử lý nghiệp vụ quản lý sách
"""


class BookController:
    def __init__(self, book_model):
        self.book_model = book_model

    def get_books(self, keyword=None):
        return self.book_model.get_all(keyword)

    def add_book(self, title, author, category, total_str):
        t = (title or "").strip()
        a = (author or "").strip()
        c = (category or "").strip()

        if not c or c == "(Chưa có thể loại)":
            return False, "Vui lòng chọn thể loại sách."

        try:
            total = int(total_str)
            if not t or total <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return False, "Vui lòng nhập tên sách và số lượng hợp lệ (lớn hơn 0)."

        try:
            self.book_model.add(t, a, c, total)
            return True, "Thêm sách thành công."
        except Exception as e:
            return False, f"Lỗi khi thêm sách: {e}"

    def update_book(self, book_id, title, author, category, total_str):
        if not book_id:
            return False, "Hãy chọn sách cần cập nhật."

        t = (title or "").strip()
        a = (author or "").strip()
        c = (category or "").strip()

        if not c or c == "(Chưa có thể loại)":
            return False, "Vui lòng chọn thể loại sách."

        try:
            total = int(total_str)
            if not t or total <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return False, "Vui lòng nhập tên sách và số lượng hợp lệ."

        try:
            self.book_model.update(book_id, t, a, c, total)
            return True, "Cập nhật sách thành công."
        except Exception as e:
            return False, f"Lỗi khi cập nhật sách: {e}"

    def delete_book(self, book_id):
        if not book_id:
            return False, "Hãy chọn sách cần xóa."
        try:
            self.book_model.delete(book_id)
            return True, "Xóa sách thành công."
        except Exception as e:
            return False, f"Lỗi khi xóa sách: {e}"
