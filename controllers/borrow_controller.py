"""
Borrow Controller — Điều phối xử lý nghiệp vụ mượn & trả sách
"""
from datetime import datetime, date, timedelta


class BorrowController:
    def __init__(self, borrow_model, book_model, cfg):
        self.borrow_model = borrow_model
        self.book_model = book_model
        self.cfg = cfg

    def get_borrows(self):
        rows = self.borrow_model.get_all()
        today = date.today().strftime("%Y-%m-%d")
        # Format lại trạng thái hiển thị
        for r in rows:
            is_overdue = r["status"] == "borrowed" and str(r["due_date"]) < today
            r["display_status"] = "Quá hạn" if is_overdue else ("Đang mượn" if r["status"] == "borrowed" else "Đã trả")
        return rows

    def borrow_book(self, member_id_str, book_id_str, days_str):
        try:
            m_id = int(str(member_id_str).strip())
            b_id = int(str(book_id_str).strip())
            # Parse ngày mượn ví dụ: "14 ngày" -> 14
            days = int(str(days_str).strip().split()[0])
        except (ValueError, IndexError, AttributeError):
            return False, "Vui lòng nhập đúng ID độc giả và ID sách (dạng số)."

        book = self.book_model.get_by_id(b_id)
        if not book:
            return False, f"Không tìm thấy sách có mã {b_id}."
        if book["available"] <= 0:
            return False, "Sách này hiện đã được mượn hết."

        b_date = date.today()
        d_date = b_date + timedelta(days=days)
        b_date_str = b_date.strftime("%Y-%m-%d")
        d_date_str = d_date.strftime("%Y-%m-%d")

        try:
            self.borrow_model.create_borrow(b_id, m_id, b_date_str, d_date_str)
            return True, f"Đã ghi nhận mượn sách. Hạn trả: {d_date_str}"
        except Exception as e:
            return False, f"Lỗi khi ghi nhận mượn: {e}"

    def return_book(self, borrow_id):
        if not borrow_id:
            return False, "Vui lòng chọn giao dịch cần trả."

        try:
            fine_rate = self.cfg.get("fine_per_day", 5000)
            res = self.borrow_model.return_borrow(borrow_id, fine_rate)
            ret_date = res["return_date"]
            overdue_days = res["overdue_days"]
            fine = res["fine_amount"]

            msg = f"Đã trả sách ngày {ret_date}."
            if fine > 0:
                msg += f"\nQuá hạn {overdue_days} ngày. Phí phạt: {fine:,} VND."
            return True, msg
        except ValueError as ve:
            return False, str(ve)
        except Exception as e:
            return False, f"Lỗi khi trả sách: {e}"
