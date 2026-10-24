"""
Script chèn dữ liệu hoạt động giả lập (Seed Data) cho LibMaster
Bao gồm: Sách đa dạng thể loại, Bạn đọc, Lịch sử mượn trả, Đang mượn, và Quá hạn
"""
import sys
from datetime import date, timedelta
from config import load_config
from database import Database


BOOKS = [
    # Công nghệ thông tin
    ("Lập Trình Python Cơ Bản & Nâng Cao", "Nguyễn Văn Hoài", "Công Nghệ Thông Tin", 5),
    ("Clean Code — Nghệ Thuật Viết Mã Sạch", "Robert C. Martin", "Công Nghệ Thông Tin", 4),
    ("Thiết Kế Hệ Thống Phân Tán Quy Mô Lớn", "Alex Xu", "Công Nghệ Thông Tin", 3),
    ("Cấu Trúc Dữ Liệu & Giải Thuật Thực Chiến", "Trần Đình Quế", "Công Nghệ Thông Tin", 6),
    ("Nhập Môn Trí Tuệ Nhân Tạo & Deep Learning", "Andrew Ng", "Công Nghệ Thông Tin", 4),

    # Kinh tế & Quản trị
    ("Đắc Nhân Tâm", "Dale Carnegie", "Kỹ Năng & Kinh Tế", 8),
    ("Cha Giàu Cha Nghèo", "Robert T. Kiyosaki", "Kỹ Năng & Kinh Tế", 6),
    ("Kinh Tế Học Hài Hước", "Steven D. Levitt", "Kỹ Năng & Kinh Tế", 5),
    ("Tư Duy Nhanh Và Chậm", "Daniel Kahneman", "Kỹ Năng & Kinh Tế", 4),
    ("Khởi Nghiệp Tinh Gọn (The Lean Startup)", "Eric Ries", "Kỹ Năng & Kinh Tế", 5),

    # Văn học
    ("Số Đỏ", "Vũ Trọng Phụng", "Văn Học", 6),
    ("Dế Mèn Phiêu Lưu Ký", "Tô Hoài", "Văn Học", 7),
    ("Tuổi Thơ Dữ Dội", "Phùng Quán", "Văn Học", 5),
    ("Rừng Na Uy", "Haruki Murakami", "Văn Học", 4),
    ("Nhà Giả Kim", "Paulo Coelho", "Văn Học", 10),

    # Khoa học & Lịch sử
    ("Sapiens — Lược Sử Loài Người", "Yuval Noah Harari", "Khoa Học & Lịch Sử", 6),
    ("Vũ Trụ Trong Vỏ Hạt Dẻ", "Stephen Hawking", "Khoa Học & Lịch Sử", 4),
    ("Vũ Trụ — Cosmos", "Carl Sagan", "Khoa Học & Lịch Sử", 5),
]

MEMBERS = [
    ("Nguyễn Hoàng Long", "long.nh@example.com", "0901234567"),
    ("Trần Thị Mai Anh", "maianh.tran@example.com", "0912345678"),
    ("Lê Quang Huy", "huy.le@example.com", "0923456789"),
    ("Phạm Minh Tuấn", "tuan.pham@example.com", "0934567890"),
    ("Đỗ Phương Thảo", "thao.dophuong@example.com", "0945678901"),
    ("Vũ Đức Thịnh", "thinh.vu@example.com", "0956789012"),
    ("Bùi Thu Hà", "ha.bui@example.com", "0967890123"),
    ("Hoàng Gia Bảo", "bao.hoang@example.com", "0978901234"),
    ("Đặng Thanh Hằng", "hang.dang@example.com", "0989012345"),
    ("Ngô Quốc Hùng", "hung.ngo@example.com", "0990123456"),
    ("Nguyễn Thu Trang", "trang.nt@example.com", "0909876543"),
    ("Đinh Trọng Nghĩa", "nghia.dt@example.com", "0918765432"),
]


def seed():
    cfg = load_config()
    db = Database(cfg)
    if db.connection_error:
        print(f"Lỗi kết nối MySQL: {db.connection_error}")
        sys.exit(1)

    print("Đang khởi tạo lại các bảng và xóa dữ liệu cũ...")
    conn = db.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cur.execute("TRUNCATE TABLE borrows;")
            cur.execute("TRUNCATE TABLE members;")
            cur.execute("TRUNCATE TABLE books;")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1;")

            # 1. Chèn Sách
            book_ids = []
            for title, author, cat, total in BOOKS:
                cur.execute(
                    "INSERT INTO books (title, author, category, total, available) VALUES (%s, %s, %s, %s, %s)",
                    (title, author, cat, total, total)
                )
                book_ids.append(cur.lastrowid)

            # 2. Chèn Bạn Đọc
            member_ids = []
            for name, email, phone in MEMBERS:
                cur.execute(
                    "INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)",
                    (name, email, phone)
                )
                member_ids.append(cur.lastrowid)

            # 3. Tạo dữ liệu mượn/trả
            today = date.today()
            rate = cfg.get("fine_per_day", 5000)

            borrows_data = [
                # Giao dịch đã hoàn tất đúng hạn (fine = 0)
                (book_ids[0], member_ids[0], today - timedelta(days=40), today - timedelta(days=26), today - timedelta(days=30), 0, "returned"),
                (book_ids[1], member_ids[1], today - timedelta(days=35), today - timedelta(days=21), today - timedelta(days=22), 0, "returned"),
                (book_ids[4], member_ids[2], today - timedelta(days=30), today - timedelta(days=16), today - timedelta(days=18), 0, "returned"),
                (book_ids[5], member_ids[3], today - timedelta(days=28), today - timedelta(days=14), today - timedelta(days=14), 0, "returned"),
                (book_ids[9], member_ids[4], today - timedelta(days=25), today - timedelta(days=11), today - timedelta(days=12), 0, "returned"),
                (book_ids[14], member_ids[5], today - timedelta(days=20), today - timedelta(days=6), today - timedelta(days=8), 0, "returned"),

                # Giao dịch đã trả nhưng trễ hạn (có tính phạt)
                (book_ids[2], member_ids[6], today - timedelta(days=30), today - timedelta(days=16), today - timedelta(days=12), 4 * rate, "returned"),
                (book_ids[7], member_ids[7], today - timedelta(days=24), today - timedelta(days=10), today - timedelta(days=5), 5 * rate, "returned"),
                (book_ids[10], member_ids[8], today - timedelta(days=18), today - timedelta(days=4), today - timedelta(days=1), 3 * rate, "returned"),

                # Giao dịch đang mượn còn hạn
                (book_ids[0], member_ids[9], today - timedelta(days=4), today + timedelta(days=10), None, 0, "borrowed"),
                (book_ids[3], member_ids[10], today - timedelta(days=2), today + timedelta(days=12), None, 0, "borrowed"),
                (book_ids[6], member_ids[11], today - timedelta(days=5), today + timedelta(days=9), None, 0, "borrowed"),
                (book_ids[11], member_ids[0], today - timedelta(days=1), today + timedelta(days=13), None, 0, "borrowed"),
                (book_ids[14], member_ids[1], today - timedelta(days=3), today + timedelta(days=11), None, 0, "borrowed"),

                # Giao dịch đang mượn nhưng đã QUÁ HẠN (để màn hình Cảnh Báo Quá Hạn hiển thị)
                (book_ids[1], member_ids[2], today - timedelta(days=24), today - timedelta(days=10), None, 0, "borrowed"),
                (book_ids[5], member_ids[3], today - timedelta(days=20), today - timedelta(days=6), None, 0, "borrowed"),
                (book_ids[8], member_ids[4], today - timedelta(days=18), today - timedelta(days=4), None, 0, "borrowed"),
                (book_ids[12], member_ids[5], today - timedelta(days=16), today - timedelta(days=2), None, 0, "borrowed"),
            ]

            for b_id, m_id, b_date, d_date, r_date, fine, status in borrows_data:
                cur.execute(
                    """
                    INSERT INTO borrows (book_id, member_id, borrow_date, due_date, return_date, fine_amount, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (b_id, m_id, b_date, d_date, r_date, fine, status)
                )

            # 4. Đồng bộ lại số lượng khả dụng (available = total - số đang mượn)
            cur.execute("""
                UPDATE books bk
                SET available = total - (
                    SELECT COUNT(*) FROM borrows b
                    WHERE b.book_id = bk.id AND b.status = 'borrowed'
                )
            """)

        print(f"Chèn dữ liệu thành công:")
        print(f"  - Sách: {len(BOOKS)} đầu sách")
        print(f"  - Bạn đọc: {len(MEMBERS)} thành viên")
        print(f"  - Phiếu mượn: {len(borrows_data)} lượt (Đã trả: 9, Đang mượn: 5, Quá hạn: 4)")
    except Exception as e:
        print(f"Lỗi khi chèn dữ liệu: {e}")
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    seed()
