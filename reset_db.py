"""
Script Reset Database — Xóa trắng toàn bộ dữ liệu và đặt lại ID về 1
"""
import sys
from config import load_config
from database import Database


def reset_database():
    cfg = load_config()
    db = Database(cfg)
    if db.connection_error:
        print(f"Lỗi kết nối MySQL: {db.connection_error}")
        sys.exit(1)

    print(f"Đang reset database: {cfg['db_name']}...")
    conn = db.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cur.execute("TRUNCATE TABLE borrows;")
            cur.execute("TRUNCATE TABLE members;")
            cur.execute("TRUNCATE TABLE books;")
            cur.execute("TRUNCATE TABLE categories;")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print("Reset thành công: Đã dọn sạch bảng borrows, members, books, categories.")
    except Exception as e:
        print(f"Lỗi khi reset: {e}")
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    reset_database()
