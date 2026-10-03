"""
Dịch vụ gửi email nhắc nhở trả sách qua SMTP
"""
import smtplib
from email.message import EmailMessage

def send_reminder_email(cfg, recipient, name, book, due_date, fine=None):
    try:
        msg = EmailMessage()
        msg["Subject"] = f"[Thư Viện] Nhắc nhở trả sách: {book}"
        msg["From"] = cfg["smtp_email"]
        msg["To"] = recipient

        fine_str = f"Phí phạt quá hạn hiện tại: {fine}\n" if fine else ""
        msg.set_content(f"""Xin chào {name},

Hệ thống thư viện xin nhắc nhở bạn về cuốn sách đang mượn:
- Tên sách: {book}
- Hạn trả: {due_date}
{fine_str}
Vui lòng mang sách đến trả tại thư viện đúng hạn.

Trân trọng,
Ban Quản Lý Thư Viện""")

        with smtplib.SMTP(cfg["smtp_server"], int(cfg["smtp_port"]), timeout=6) as server:
            server.starttls()
            server.login(cfg["smtp_email"], cfg["smtp_password"])
            server.send_message(msg)
        return True
    except Exception as e:
        print("Lỗi SMTP:", e)
        return False
