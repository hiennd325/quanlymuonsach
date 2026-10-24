"""
Members View — Màn hình Quản Lý Bạn Đọc
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from theme import THEME, RADIUS


class MembersView(ctk.CTkFrame):
    def __init__(self, parent, app, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.controller = controller or getattr(app, "controllers", {}).get("member")
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left")
        ctk.CTkLabel(
            title_box,
            text="Quản Lý Bạn Đọc",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=THEME["text_primary"]
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_box,
            text="Hồ sơ thành viên, thông tin liên hệ và lịch sử mượn trả",
            font=ctk.CTkFont(size=12),
            text_color=THEME["text_secondary"]
        ).pack(anchor="w")

        # Form thêm bạn đọc
        top = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        top.pack(fill="x", pady=(0, 16))

        self.m_name_var, self.m_email_var, self.m_phone_var = tk.StringVar(), tk.StringVar(), tk.StringVar()
        fields = [
            ("Họ và tên:", self.m_name_var, 200),
            ("Email:", self.m_email_var, 220),
            ("Số ĐT:", self.m_phone_var, 150)
        ]
        for i, (l, v, w) in enumerate(fields):
            ctk.CTkLabel(
                top,
                text=l,
                font=ctk.CTkFont(size=12),
                text_color=THEME["text_secondary"]
            ).grid(row=0, column=i*2, padx=10, pady=14, sticky="e")

            ctk.CTkEntry(
                top,
                textvariable=v,
                width=w,
                height=36,
                fg_color=THEME["input_bg"],
                border_color=THEME["input_border"],
                border_width=1,
                corner_radius=RADIUS["input"],
                text_color=THEME["text_primary"]
            ).grid(row=0, column=i*2+1, padx=6, pady=14)

        ctk.CTkButton(
            top,
            text="Thêm Bạn Đọc",
            width=110,
            height=36,
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=RADIUS["pill"],
            command=self.add_member
        ).grid(row=0, column=6, padx=8)

        ctk.CTkButton(
            top,
            text="Xóa Đã Chọn",
            width=100,
            height=36,
            fg_color=THEME["accent_red"],
            hover_color=THEME["accent_red_hover"],
            text_color=THEME["text_white"],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=RADIUS["pill"],
            command=self.delete_member
        ).grid(row=0, column=7, padx=8)

        # Bảng dữ liệu bạn đọc
        tbl_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        tbl_card.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tbl_card, columns=("id", "name", "email", "phone", "active"), show="headings")
        cols = [
            ("id", "Mã", 60),
            ("name", "Tên Độc Giả", 240),
            ("email", "Email", 280),
            ("phone", "Điện Thoại", 160),
            ("active", "Đang Mượn", 110)
        ]
        for c, h, w in cols:
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="center" if c in ("id", "active") else "w")

        self.tree.pack(fill="both", expand=True, padx=14, pady=14)

    def load_data(self):
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("member")
        if not self.controller or (hasattr(self.app, "db") and self.app.db.connection_error):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        members = self.controller.get_members()
        for m in members:
            self.tree.insert("", "end", values=(m["id"], m["name"], m["email"], m["phone"], m.get("active_borrows", 0)))

    def add_member(self):
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("member")

        ok, msg = self.controller.add_member(
            self.m_name_var.get(),
            self.m_email_var.get(),
            self.m_phone_var.get()
        )
        if not ok:
            messagebox.showwarning("Lỗi", msg)
            return

        self.m_name_var.set("")
        self.m_email_var.set("")
        self.m_phone_var.set("")
        self.load_data()
        self.app.refresh_stats()

    def delete_member(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chọn mục", "Vui lòng chọn độc giả cần xóa.")
            return

        if not messagebox.askyesno("Xác nhận", "Xóa độc giả này?"):
            return

        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("member")

        m_id = self.tree.item(sel[0])["values"][0]
        ok, msg = self.controller.delete_member(m_id)
        if not ok:
            messagebox.showerror("Lỗi", msg)
            return

        self.load_data()
        self.app.refresh_stats()
