"""
Kiểm thử tự động toàn diện mô hình MVC cho LibMaster
"""
import sys
import unittest
from config import load_config
from database import Database
from models import BookModel, MemberModel, BorrowModel, ReportModel
from controllers import (
    BookController,
    MemberController,
    BorrowController,
    OverdueController,
    DashboardController,
    ReportController
)
from views import (
    DashboardView,
    BooksView,
    MembersView,
    BorrowsView,
    OverdueView,
    ReportsView
)


class TestMVCArchitecture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = load_config()
        cls.db = Database(cls.cfg)
        if cls.db.connection_error:
            raise RuntimeError(f"Database error: {cls.db.connection_error}")

        cls.book_model = BookModel(cls.db)
        cls.member_model = MemberModel(cls.db)
        cls.borrow_model = BorrowModel(cls.db, cls.book_model)
        cls.report_model = ReportModel(cls.db)

        cls.book_ctrl = BookController(cls.book_model)
        cls.member_ctrl = MemberController(cls.member_model)
        cls.borrow_ctrl = BorrowController(cls.borrow_model, cls.book_model, cls.cfg)
        cls.overdue_ctrl = OverdueController(cls.borrow_model, cls.cfg)
        cls.dash_ctrl = DashboardController(cls.book_model, cls.member_model, cls.borrow_model)
        cls.report_ctrl = ReportController(cls.report_model)

    def test_01_models_and_controllers_books(self):
        # 1. Thêm sách qua controller
        ok, msg = self.book_ctrl.add_book("Sách Test MVC", "Tác Giả Test", "Công Nghệ", "5")
        self.assertTrue(ok, msg)

        # 2. Tìm kiếm sách
        books = self.book_ctrl.get_books("Sách Test MVC")
        self.assertGreater(len(books), 0)
        book_id = books[0]["id"]
        self.assertEqual(books[0]["total"], 5)
        self.assertEqual(books[0]["available"], 5)

        # 3. Cập nhật sách
        ok, msg = self.book_ctrl.update_book(book_id, "Sách Test MVC Đã Sửa", "Tác Giả Test", "Công Nghệ", "8")
        self.assertTrue(ok, msg)
        book = self.book_model.get_by_id(book_id)
        self.assertEqual(book["title"], "Sách Test MVC Đã Sửa")
        self.assertEqual(book["total"], 8)
        self.assertEqual(book["available"], 8)

        # 4. Xóa sách
        ok, msg = self.book_ctrl.delete_book(book_id)
        self.assertTrue(ok, msg)
        book = self.book_model.get_by_id(book_id)
        self.assertIsNone(book)

    def test_02_member_mvc(self):
        # Thêm bạn đọc
        ok, msg = self.member_ctrl.add_member("Độc Giả Test", "test_mvc@example.com", "0901234567")
        self.assertTrue(ok, msg)

        members = self.member_ctrl.get_members()
        matched = [m for m in members if m["email"] == "test_mvc@example.com"]
        self.assertGreater(len(matched), 0)
        member_id = matched[0]["id"]

        # Xóa bạn đọc
        ok, msg = self.member_ctrl.delete_member(member_id)
        self.assertTrue(ok, msg)

    def test_03_borrow_flow(self):
        # Tạo sách và độc giả tạm thời
        ok, _ = self.book_ctrl.add_book("Sách Mượn Test", "Tác Giả", "Khoa Học", "2")
        self.assertTrue(ok)
        b_id = self.book_ctrl.get_books("Sách Mượn Test")[0]["id"]

        ok, _ = self.member_ctrl.add_member("Bạn Mượn Test", "borrower@example.com", "0911111111")
        self.assertTrue(ok)
        members = self.member_ctrl.get_members()
        m_id = [m for m in members if m["email"] == "borrower@example.com"][0]["id"]

        # Mượn sách
        ok, msg = self.borrow_ctrl.borrow_book(m_id, b_id, "14 ngày")
        self.assertTrue(ok, msg)

        # Kiểm tra số lượng tồn giảm
        book = self.book_model.get_by_id(b_id)
        self.assertEqual(book["available"], 1)

        # Lấy danh sách mượn
        borrows = self.borrow_ctrl.get_borrows()
        user_borrows = [b for b in borrows if b["member_name"] == "Bạn Mượn Test"]
        self.assertGreater(len(user_borrows), 0)
        br_id = user_borrows[0]["id"]

        # Trả sách
        ok, msg = self.borrow_ctrl.return_book(br_id)
        self.assertTrue(ok, msg)

        # Kiểm tra số lượng tồn phục hồi
        book = self.book_model.get_by_id(b_id)
        self.assertEqual(book["available"], 2)

        # Dọn dẹp
        self.book_ctrl.delete_book(b_id)
        self.member_ctrl.delete_member(m_id)

    def test_04_dashboard_and_reports(self):
        dash_data = self.dash_ctrl.get_dashboard_data()
        self.assertIn("books_total", dash_data)
        self.assertIn("books_available", dash_data)
        self.assertIn("members_count", dash_data)
        self.assertIn("recent_borrows", dash_data)

        report_data = self.report_ctrl.get_report_data()
        self.assertIn("kpis", report_data)
        self.assertIn("top_books", report_data)
        self.assertIn("top_categories", report_data)

    def test_05_views_exports(self):
        # Đảm bảo các View class import được đầy đủ và đúng chuẩn
        views = [DashboardView, BooksView, MembersView, BorrowsView, OverdueView, ReportsView]
        self.assertEqual(len(views), 6)


if __name__ == "__main__":
    unittest.main()
