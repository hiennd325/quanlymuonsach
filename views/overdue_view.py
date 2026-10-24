"""
Overdue View — Màn hình Cảnh Báo Quá Hạn & Quản Lý Phạt
"""
from tkinter import ttk, messagebox
import customtkinter as ctk

from theme import THEME, RADIUS


class OverdueView(ctk.CTkFrame):
    def __init__(self, parent, app, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.controller = controller or getattr(app, "controllers", {}).get("overdue")
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left")
        ctk.CTkLabel(
            title_box,
            text="Cảnh Báo Quá Hạn & Quản Lý Phạt",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=THEME["text_primary"]
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_box,
            text="Gửi email thông báo tự động và theo dõi phí phạt của bạn đọc",
            font=ctk.CTkFont(size=12),
            text_color=THEME["text_secondary"]
        ).pack(anchor="w")

        # Nút gửi email
        actions = ctk.CTkFrame(header, fg_color="transparent")
        actions.pack(side="right")

        ctk.CTkButton(
            actions,
            text="Gửi Mail Mục Chọn",
            height=38,
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=RADIUS["pill"],
            command=self.send_single_reminder
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            actions,
            text="Gửi Toàn Bộ Quá Hạn",
            height=38,
            fg_color=THEME["accent_orange"],
            hover_color=THEME["accent_orange_hover"],
            text_color=THEME["text_white"],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=RADIUS["pill"],
            command=self.send_bulk_reminders
        ).pack(side="left", padx=4)

        # Banner thông báo quá hạn
        self.overdue_banner = ctk.CTkFrame(
            self,
            fg_color=THEME["accent_red_subtle"],
            corner_radius=RADIUS["card_sm"],
            border_color=THEME["accent_red"],
            border_width=1
        )
        self.overdue_banner.pack(fill="x", pady=(0, 16))

        self.overdue_summary = ctk.CTkLabel(
            self.overdue_banner,
            text="...",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=THEME["accent_red"]
        )
        self.overdue_summary.pack(padx=16, pady=12)

        # Bảng dữ liệu quá hạn
        tbl_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        tbl_card.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            tbl_card,
            columns=("id", "member", "email", "book", "due_date", "days", "fine"),
            show="headings"
        )
        cols = [
            ("id", "Mã", 50),
            ("member", "Tên Độc Giả", 180),
            ("email", "Email", 240),
            ("book", "Tên Sách", 240),
            ("due_date", "Hạn Trả", 100),
            ("days", "Số Ngày Quá Hạn", 120),
            ("fine", "Tiền Phạt Tạm Tính", 140)
        ]
        for c, h, w in cols:
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="center" if c in ("id", "due_date", "days", "fine") else "w")

        self.tree.pack(fill="both", expand=True, padx=14, pady=14)

    def load_data(self):
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("overdue")
        if not self.controller or (hasattr(self.app, "db") and self.app.db.connection_error):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        rows, total_fine = self.controller.get_overdue_data()

        for r in rows:
            self.tree.insert("", "end", values=(
                r["id"],
                r["name"],
                r["email"],
                r["title"],
                r["due_date"],
                f"{r['overdue_days']} ngày",
                f"{r['fine_amount']:,} VND"
            ))

        if len(rows) > 0:
            self.overdue_banner.configure(fg_color=THEME["accent_red_subtle"], border_color=THEME["accent_red"])
            self.overdue_summary.configure(
                text=f"Phát hiện {len(rows)} lượt mượn quá hạn  |  Tổng tiền phạt ước tính: {total_fine:,} VND",
                text_color=THEME["accent_red"]
            )
        else:
            self.overdue_banner.configure(fg_color=THEME["accent_cyan_subtle"], border_color=THEME["accent_cyan"])
            self.overdue_summary.configure(
                text="Hiện không có lượt mượn nào bị quá hạn.",
                text_color=THEME["accent_cyan"]
            )

    def send_single_reminder(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chọn mục", "Vui lòng chọn 1 dòng để gửi email.")
            return

        v = self.tree.item(sel[0])["values"]

        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("overdue")

        def callback(ok, recipient):
            if ok:
                messagebox.showinfo("Thành công", f"Đã gửi email nhắc nhở tới {recipient}.")
            else:
                messagebox.showerror("Thất bại", f"Không thể gửi email tới {recipient}. Kiểm tra .env.")

        self.controller.send_single_reminder_async(
            recipient=v[2],
            name=v[1],
            book_title=v[3],
            due_date=v[4],
            fine_str=v[6],
            callback=callback
        )

    def send_bulk_reminders(self):
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("overdue")

        def callback(success, total):
            if total == 0:
                messagebox.showinfo("Thông báo", "Không có bạn đọc nào đến hạn hoặc quá hạn hôm nay.")
            else:
                messagebox.showinfo("Hoàn tất", f"Đã gửi nhắc nhở email thành công cho {success}/{total} bạn đọc.")

        self.controller.send_bulk_reminders_async(callback=callback)
