"""
Category Controller — Điều phối xử lý nghiệp vụ quản lý thể loại sách
"""


class CategoryController:
    def __init__(self, category_model, book_model=None):
        self.category_model = category_model
        self.book_model = book_model

    def get_categories(self, keyword=None):
        return self.category_model.get_all(keyword)

    def get_category_names(self):
        return self.category_model.get_names()

    def add_category(self, name):
        clean_name = (name or "").strip()
        if not clean_name:
            return False, "Vui lòng nhập tên thể loại."

        existing = self.category_model.get_by_name(clean_name)
        if existing:
            return False, f"Thể loại '{clean_name}' đã tồn tại."

        try:
            self.category_model.add(clean_name)
            return True, f"Thêm thể loại '{clean_name}' thành công."
        except Exception as e:
            return False, f"Lỗi khi thêm thể loại: {e}"

    def update_category(self, cat_id, new_name):
        if not cat_id:
            return False, "Vui lòng chọn thể loại cần cập nhật."

        clean_name = (new_name or "").strip()
        if not clean_name:
            return False, "Tên thể loại không được để trống."

        existing = self.category_model.get_by_name(clean_name)
        if existing and str(existing["id"]) != str(cat_id):
            return False, f"Tên thể loại '{clean_name}' đã được sử dụng."

        try:
            self.category_model.update(cat_id, clean_name)
            return True, "Cập nhật thể loại thành công."
        except Exception as e:
            return False, f"Lỗi khi cập nhật thể loại: {e}"

    def delete_category(self, cat_id):
        if not cat_id:
            return False, "Vui lòng chọn thể loại cần xóa."

        try:
            self.category_model.delete(cat_id)
            return True, "Xóa thể loại thành công."
        except ValueError as ve:
            return False, str(ve)
        except Exception as e:
            return False, f"Lỗi khi xóa thể loại: {e}"
