"""
Overdue Controller — Điều phối xử lý cảnh báo quá hạn và gửi email
"""
import threading
from datetime import datetime, date
from mailer import send_reminder_email


class OverdueController:
    def __init__(self, borrow_model, cfg):
        self.borrow_model = borrow_model
        self.cfg = cfg

    def get_overdue_data(self):
        today_date = date.today()
        today_str = today_date.strftime("%Y-%m-%d")
        rows = self.borrow_model.get_overdue_list(today_str)

        total_fine = 0
        rate = self.cfg.get("fine_per_day", 5000)
        items = []

        for r in rows:
            if isinstance(r["due_date"], str):
                d_date = datetime.strptime(r["due_date"], "%Y-%m-%d").date()
            else:
                d_date = r["due_date"]

            over_days = (today_date - d_date).days
            fine = over_days * rate
            total_fine += fine

            item = dict(r)
            item["overdue_days"] = over_days
            item["fine_amount"] = fine
            items.append(item)

        return items, total_fine

    def send_single_reminder_async(self, recipient, name, book_title, due_date, fine_str, callback):
        def worker():
            ok = send_reminder_email(self.cfg, recipient, name, book_title, due_date, fine_str)
            if callback:
                callback(ok, recipient)

        threading.Thread(target=worker, daemon=True).start()

    def send_bulk_reminders_async(self, callback):
        today_str = date.today().strftime("%Y-%m-%d")
        rows = self.borrow_model.get_due_or_overdue_today(today_str)
        if not rows:
            if callback:
                callback(0, 0)
            return

        def bulk_worker():
            success = 0
            for r in rows:
                if send_reminder_email(self.cfg, r["email"], r["name"], r["title"], r["due_date"]):
                    success += 1
            if callback:
                callback(success, len(rows))

        threading.Thread(target=bulk_worker, daemon=True).start()
