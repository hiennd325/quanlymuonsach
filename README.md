# Ứng Dụng Quản Lý Thư Viện (Library Management System)

Ứng dụng quản trị thư viện hiện đại viết bằng **Python** giao diện **CustomTkinter** kết nối cơ sở dữ liệu **MySQL**. Hỗ trợ quản lý sách, thể loại, độc giả, quy trình mượn/trả, cảnh báo sách quá hạn và gửi email thông báo.

---

## 📋 Mục Lục
1. [Yêu Cầu Hệ Thống](#-yêu-cầu-hệ-thống)
2. [Cài Đặt & Cấu Hình MySQL](#-cài-đặt--cấu-hình-mysql)
3. [Cài Đặt Thư Viện Python](#-cài-đặt-thư-viện-python)
4. [Cấu Hình Môi Trường (.env)](#-cấu-hình-môi-trường-env)
5. [Khởi Tạo Dữ Liệu](#-khởi-tạo-dữ-liệu)
6. [Cách Chạy Ứng Dụng](#-cách-chạy-ứng-dụng)
7. [Cấu Trúc Thư Mục Dự Án](#-cấu-trúc-thư-mục-dự-án)

---

## 💻 Yêu Cầu Hệ Thống

- **Python**: Phiên bản 3.10 trở lên.
- **MySQL Server** hoặc **MariaDB** (hoặc dùng XAMPP / WampServer / Docker).
- **Hệ điều hành**: Windows, Linux hoặc macOS.

---

## 🗄️ Cài Đặt & Cấu Hình MySQL

### Cách 1: Sử dụng MySQL Server có sẵn hoặc XAMPP
1. Mở dịch vụ MySQL Server (hoặc bật nút **Start** tại mục MySQL trên bảng điều khiển XAMPP).
2. Mở MySQL CLI / phpMyAdmin / MySQL Workbench / DBeaver và chạy nội dung file `schema.sql` để tạo database và các bảng:
   ```bash
   mysql -u root -p < schema.sql
   ```
   *(Nếu dùng phpMyAdmin: Tạo cơ sở dữ liệu mới hoặc bấm vào tab **Import** và chọn file `schema.sql`)*

### Cách 2: Sử dụng Docker (Nhanh & Tiện lợi)
Nếu bạn đã có Docker, chạy một dòng lệnh sau:
```bash
docker run -d --name library-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=Admin123 -e MYSQL_DATABASE=library_db mysql:8.0
```
Sau đó import schema:
```bash
docker exec -i library-mysql mysql -u root -pAdmin123 library_db < schema.sql
```

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
   - `mysql-connector-python`: Thư viện kết nối và làm việc với MySQL Database.

---

## ⚙️ Cấu Hình Môi Trường (.env)

Tạo file `.env` tại thư mục gốc của dự án (hoặc chỉnh sửa file `.env` có sẵn) theo thông tin MySQL của máy bạn:

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
> - Thay đổi `DB_USER` và `DB_PASSWORD` cho khớp với mật khẩu tài khoản MySQL trên máy bạn.
> - Cấu hình email là tuỳ chọn; nếu không dùng tính năng gửi mail, bạn có thể để nguyên giá trị mặc định.

---

## 🚀 Khởi Tạo Dữ Liệu

Dự án cung cấp sẵn 2 script hỗ trợ quản lý dữ liệu:

1. **Tạo dữ liệu mẫu ban đầu (Seed Data):**
   Chạy lệnh sau để tự động tạo danh mục, các đầu sách, độc giả và lịch sử mượn trả mẫu (bao gồm các phiếu quá hạn để kiểm thử tính năng):
   ```bash
   python seed_data.py
   ```

2. **Xóa trắng dữ liệu (Reset Database):**
   Nếu cần làm sạch dữ liệu trong cơ sở dữ liệu:
   ```bash
   python reset_db.py
   ```

---

## 🖥️ Cách Chạy Ứng Dụng

Sau khi cấu hình xong MySQL và cài đặt thư viện:

```bash
python main.py
```
*(hoặc chạy qua file đại diện `python app.py`)*

### Chạy ở chế độ kiểm thử tự động (Self Test)
Nếu muốn kiểm tra nhanh kết nối database, nạp dữ liệu và các module chức năng:
```bash
python app.py --test
```

---

## 📁 Cấu Trúc Thư Mục Dự Án

```text
├── controllers/          # Bộ điều khiển trung gian kết nối View và Model
├── models/               # Các mô hình dữ liệu (Sách, Thành viên, Mượn trả...)
├── views/                # Giao diện các màn hình (CustomTkinter)
├── app.py                # Điểm khởi chạy ứng dụng (Wrapper)
├── main.py               # Ứng dụng chính & Giao diện Dashboard tổng thể
├── database.py           # Quản lý kết nối và truy vấn MySQL
├── config.py             # Đọc cấu hình từ file .env
├── mailer.py             # Xử lý gửi email thông báo quá hạn
├── schema.sql            # Script SQL tạo cơ sở dữ liệu và bảng
├── seed_data.py          # Script chèn dữ liệu mẫu thử nghiệm
├── reset_db.py           # Script dọn dẹp/làm rỗng database
├── theme.py & widgets.py # Định nghĩa theme giao diện, bảng, thanh tìm kiếm
├── requirements.txt      # Danh sách thư viện Python cần thiết
└── .env                  # File cấu hình bảo mật môi trường
```
