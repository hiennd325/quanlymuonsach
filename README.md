# Ứng Dụng Quản Lý Thư Viện (Library Management System)

Ứng dụng quản trị thư viện hiện đại viết bằng **Python** giao diện **CustomTkinter** kết nối cơ sở dữ liệu **MySQL**. Hỗ trợ quản lý sách, thể loại, độc giả, quy trình mượn/trả, cảnh báo sách quá hạn và gửi email thông báo.

---

## 📋 Mục Lục
1. [Yêu Cầu Hệ Thống](#-yêu-cầu-hệ-thống)
2. [Cài Đặt Thư Viện Python](#-cài-đặt-thư-viện-python)
3. [Cấu Hình Môi Trường (.env)](#-cấu-hình-môi-trường-env)
4. [Cơ Sở Dữ Liệu MySQL](#-cơ-sở-dữ-liệu-mysql)
5. [Khởi Tạo Dữ Liệu](#-khởi-tạo-dữ-liệu)
6. [Cách Chạy Ứng Dụng](#-cách-chạy-ứng-dụng)
7. [Chạy Kiểm Thử (Unit Tests)](#-chạy-kiểm-thử-unit-tests)
8. [Cấu Trúc Thư Mục Dự Án](#-cấu-trúc-thư-mục-dự-án)

---

## 💻 Yêu Cầu Hệ Thống

- **Python**: Phiên bản 3.10 trở lên.
- **MySQL Server** hoặc **MariaDB** (hoặc dùng qua XAMPP / WampServer / Docker).
- **Hệ điều hành**: Windows, Linux hoặc macOS.

---

## 📦 Cài Đặt Thư Viện Python

1. **Khởi tạo và kích hoạt môi trường ảo (Virtual Environment - Khuyến nghị):**
   - Trên **Linux / macOS**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Trên **Windows (CMD / PowerShell)**:
     ```cmd
     python -m venv .venv
     .venv\Scripts\activate
     ```

2. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   *Các thư viện chính bao gồm:*
   - `customtkinter`: Giao diện người dùng hiện đại, hỗ trợ Dark/Light mode.
   - `mysql-connector-python`: Thư viện chính thức từ Oracle để kết nối và làm việc với MySQL Database.

---

## ⚙️ Cấu Hình Môi Trường (.env)

Tạo file `.env` tại thư mục gốc của dự án (hoặc chỉnh sửa file `.env` có sẵn) theo thông tin tài khoản MySQL trên máy bạn:

```env
# Cấu hình Cơ Sở Dữ Liệu MySQL
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=Admin123
DB_NAME=library_db

# Cấu hình phí phạt trả trễ hạn (VND/ngày)
FINE_PER_DAY=5000

# Cấu hình Gửi Email Thông Báo Quá Hạn (SMTP Gmail / Tuỳ chọn)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

> **Lưu ý:**
> - Thay đổi `DB_USER` và `DB_PASSWORD` cho khớp với mật khẩu tài khoản MySQL của bạn.
> - Cấu hình email là tuỳ chọn; nếu không dùng tính năng gửi mail, bạn có thể để nguyên giá trị mặc định.

---

## 🗄️ Cơ Sở Dữ Liệu MySQL

> [!IMPORTANT]
> **Bạn KHÔNG cần phải vào SQL để chạy file `schema.sql` thủ công!**  
> Khi ứng dụng khởi động hoặc khi chạy lệnh tạo dữ liệu mẫu, hệ thống sẽ **tự động kết nối và tạo mới Database (`library_db`) cùng toàn bộ các bảng** (`categories`, `books`, `members`, `borrows`) nếu chưa tồn tại.

Bạn chỉ cần đảm bảo dịch vụ MySQL đang hoạt động:

### Cách 1: Sử dụng MySQL Server có sẵn hoặc XAMPP
- Bật dịch vụ MySQL Server trên máy (hoặc nhấn nút **Start** tại mục MySQL trong bảng điều khiển XAMPP).
- Cấu hình đúng `DB_USER` và `DB_PASSWORD` trong file `.env`.

### Cách 2: Sử dụng Docker
Nếu máy bạn có Docker, chỉ cần khởi chạy container MySQL:
```bash
docker run -d --name library-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=Admin123 -e MYSQL_DATABASE=library_db mysql:8.0
```

*(File `schema.sql` được đính kèm sẵn trong mã nguồn chỉ đóng vai trò dự phòng nếu bạn muốn tự import thủ công qua phpMyAdmin / Workbench / DBeaver).*

---

## 🚀 Khởi Tạo Dữ Liệu

Dự án cung cấp sẵn các script hỗ trợ quản lý dữ liệu:

1. **Tạo dữ liệu mẫu ban đầu (Seed Data - Khuyến nghị khi mới cài đặt):**
   Tự động khởi tạo cấu trúc database, nạp danh mục, 18 đầu sách, 12 độc giả cùng các giao dịch mượn/trả và quá hạn để kiểm thử đầy đủ các chức năng:
   ```bash
   python seed_data.py
   ```

2. **Xóa trắng dữ liệu (Reset Database):**
   Nếu cần làm sạch toàn bộ dữ liệu trong các bảng và đưa ID về 1:
   ```bash
   python reset_db.py
   ```

---

## 🖥️ Cách Chạy Ứng Dụng

Sau khi cấu hình xong file `.env`:

```bash
python main.py
```
*(hoặc chạy qua file đại diện `python app.py`)*

### Chạy ở chế độ kiểm thử nhanh giao diện (Self Test)
Nếu muốn kiểm tra nhanh nạp module và khởi động:
```bash
python app.py --test
```

---

## 🧪 Chạy Kiểm Thử (Unit Tests)

Dự án tích hợp bộ kiểm thử tự động toàn diện mô hình MVC (Model - View - Controller):

```bash
python -m unittest discover tests
```

---

## 📁 Cấu Trúc Thư Mục Dự Án

```text
├── controllers/          # Bộ điều khiển trung gian kết nối View và Model
├── models/               # Các mô hình dữ liệu (Sách, Thành viên, Mượn trả...)
├── views/                # Giao diện các màn hình (CustomTkinter)
├── tests/                # Bộ kiểm thử tự động MVC
├── app.py                # Điểm khởi chạy ứng dụng (Wrapper)
├── main.py               # Ứng dụng chính & Giao diện Dashboard tổng thể
├── database.py           # Quản lý kết nối và truy vấn MySQL (mysql-connector-python)
├── config.py             # Đọc cấu hình từ file .env
├── mailer.py             # Xử lý gửi email thông báo quá hạn
├── schema.sql            # Script SQL dự phòng tạo cấu trúc database
├── seed_data.py          # Script chèn dữ liệu mẫu thử nghiệm
├── reset_db.py           # Script dọn dẹp/làm rỗng database
├── theme.py & widgets.py # Định nghĩa theme giao diện, bảng, thanh tìm kiếm
├── requirements.txt      # Danh sách thư viện Python cần thiết
└── .env                  # File cấu hình bảo mật môi trường
```
