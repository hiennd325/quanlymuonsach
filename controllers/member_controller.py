"""
Member Controller — Điều phối xử lý nghiệp vụ quản lý độc giả
"""


class MemberController:
    def __init__(self, member_model):
        self.member_model = member_model

    def get_members(self):
        return self.member_model.get_all_with_active_borrows()

    def add_member(self, name, email, phone):
        n = (name or "").strip()
        e = (email or "").strip()
        p = (phone or "").strip()

        if not n or "@" not in e:
            return False, "Vui lòng nhập họ tên và email hợp lệ."

        try:
            self.member_model.add(n, e, p)
            return True, "Thêm độc giả thành công."
        except Exception as ex:
            return False, f"Lỗi khi thêm độc giả: {ex}"

    def delete_member(self, member_id):
        if not member_id:
            return False, "Chưa chọn độc giả để xóa."

        try:
            self.member_model.delete(member_id)
            return True, "Xóa độc giả thành công."
        except Exception as ex:
            return False, f"Lỗi khi xóa độc giả: {ex}"
