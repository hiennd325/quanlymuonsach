"""
Quản lý kết nối & thao tác cơ sở dữ liệu MySQL (Thuần MySQL, không SQLite)
"""
import pymysql


class Database:
    def __init__(self, cfg):
        self.cfg = cfg
        self.connection_error = None
        self.init_db()

    def get_connection(self):
        return pymysql.connect(
            host=self.cfg["db_host"],
            port=int(self.cfg["db_port"]),
            user=self.cfg["db_user"],
            password=self.cfg["db_password"],
            database=self.cfg["db_name"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def init_db(self):
        try:
            # 1. Kết nối không cần DB trước để tự động tạo DATABASE nếu chưa có
            temp_conn = pymysql.connect(
                host=self.cfg["db_host"],
                port=int(self.cfg["db_port"]),
                user=self.cfg["db_user"],
                password=self.cfg["db_password"],
                autocommit=True
            )
            with temp_conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE IF NOT EXISTS `{self.cfg['db_name']}` DEFAULT CHARACTER SET utf8mb4;")
            temp_conn.close()

            # 2. Tạo bảng nếu chưa tồn tại
            conn = self.get_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS categories (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL UNIQUE
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS books (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        author VARCHAR(255) NOT NULL,
                        category VARCHAR(100) NOT NULL,
                        total INT DEFAULT 1,
                        available INT DEFAULT 1
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS members (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        phone VARCHAR(50) NOT NULL
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS borrows (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        book_id INT NOT NULL,
                        member_id INT NOT NULL,
                        borrow_date DATE NOT NULL,
                        due_date DATE NOT NULL,
                        return_date DATE NULL,
                        fine_amount INT DEFAULT 0,
                        status VARCHAR(20) DEFAULT 'borrowed',
                        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
                        FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
                    )
                """)
                cur.execute("""
                    INSERT IGNORE INTO categories (name)
                    SELECT DISTINCT category FROM books
                    WHERE category IS NOT NULL AND TRIM(category) != ''
                """)
            conn.close()
            self.connection_error = None
        except Exception as e:
            self.connection_error = str(e)

    def query(self, sql, params=()):
        if self.connection_error:
            raise RuntimeError(f"Chưa kết nối được MySQL: {self.connection_error}")
        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
        conn.close()
        return rows

    def execute(self, sql, params=()):
        if self.connection_error:
            raise RuntimeError(f"Chưa kết nối được MySQL: {self.connection_error}")
        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute(sql, params)
            last_id = cur.lastrowid
        conn.close()
        return last_id
