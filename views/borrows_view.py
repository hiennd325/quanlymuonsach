"""
Borrows View — Màn hình Mượn & Trả Sách
"""
from tkinter import ttk, messagebox
import customtkinter as ctk

from theme import THEME, RADIUS


class BorrowsView(ctk.CTkFrame):
    def __init__(self, parent, app, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.controller = controller or getattr(app, "controllers", {}).get("borrow")
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left")
        ctk.CTkLabel(
            title_box,
            text="Giao Dịch Mượn & Trả Sách",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=THEME["text_primary"]
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_box,
            text="Thực hiện ghi mượn, trả sách và tính phí phạt tự động",
            font=ctk.CTkFont(size=12),
            text_color=THEME["text_secondary"]
        ).pack(anchor="w")

        # Thẻ Thao tác Mượn / Trả
        top = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        top.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            top,
            text="Mã Độc Giả:",
            font=ctk.CTkFont(size=12),
            text_color=THEME["text_secondary"]
        ).grid(row=0, column=0, padx=10, pady=14, sticky="e")

        self.borrow_mem_id = ctk.CTkEntry(
            top,
            width=90,
            height=36,
            fg_color=THEME["input_bg"],
            border_color=THEME["input_border"],
            border_width=1,
            corner_radius=RADIUS["input"],
            text_color=THEME["text_primary"]
        )
        self.borrow_mem_id.grid(row=0, column=1, padx=6, pady=14)

        ctk.CTkLabel(
            top,
            text="Mã Sách:",
            font=ctk.CTkFont(size=12),
            text_color=THEME["text_secondary"]
        ).grid(row=0, column=2, padx=10, pady=14, sticky="e")

        self.borrow_book_id = ctk.CTkEntry(
            top,
            width=90,
            height=36,
            fg_color=THEME["input_bg"],
            border_color=THEME["input_border"],
            border_width=1,
            corner_radius=RADIUS["input"],
            text_color=THEME["text_primary"]
        )
        self.borrow_book_id.grid(row=0, column=3, padx=6, pady=14)

        ctk.CTkLabel(
            top,
            text="Thời hạn:",
            font=ctk.CTkFont(size=12),
            text_color=THEME["text_secondary"]
        ).grid(row=0, column=4, padx=10, pady=14, sticky="e")

        self.borrow_days = ctk.CTkComboBox(
            top,
            values=["7 ngày", "14 ngày", "30 ngày"],
            width=110,
            height=36,
            fg_color=THEME["input_bg"],
            border_color=THEME["input_border"],
            border_width=1,
            corner_radius=RADIUS["input"],
            text_color=THEME["text_primary"],
            button_color=THEME["primary"],
            button_hover_color=THEME["primary_hover"]
        )
        self.borrow_days.set("14 ngày")
        self.borrow_days.grid(row=0, column=5, padx=6, pady=14)

        ctk.CTkButton(
            top,
            text="Xác Nhận Mượn",
            command=self.do_borrow,
            height=36,
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=RADIUS["pill"]
        ).grid(row=0, column=6, padx=10)

        ctk.CTkButton(
            top,
            text="Trả Sách Đã Chọn",
            command=self.do_return,
            height=36,
            fg_color=THEME["accent_cyan"],
            hover_color=THEME["accent_cyan_hover"],
            text_color=THEME["text_white"],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=RADIUS["pill"]
        ).grid(row=0, column=7, padx=6)

        # Bảng Giao Dịch
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
            columns=("id", "member", "book", "borrow_date", "due_date", "return_date", "status", "fine"),
            show="headings"
        )
        cols = [
            ("id", "Mã", 50),
            ("member", "Độc Giả", 180),
            ("book", "Tên Sách", 240),
            ("borrow_date", "Ngày Mượn", 100),
            ("due_date", "Hạn Trả", 100),
            ("return_date", "Ngày Trả", 100),
            ("status", "Trạng Thái", 110),
            ("fine", "Tiền Phạt", 100)
        ]
        for c, h, w in cols:
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="center" if c in ("id", "borrow_date", "due_date", "return_date", "status", "fine") else "w")

        self.tree.pack(fill="both", expand=True, padx=14, pady=14)

    def load_data(self):
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("borrow")
        if not self.controller or (hasattr(self.app, "db") and self.app.db.connection_error):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.controller.get_borrows()
        for r in rows:
            self.tree.insert("", "end", values=(
                r["id"],
                r["member_name"],
                r["book_title"],
                r["borrow_date"],
                r["due_date"],
                r["return_date"] or "-",
                r["display_status"],
                f"{r['fine_amount']:,}đ"
            ))

    def do_borrow(self):
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("borrow")

        ok, msg = self.controller.borrow_book(
            self.borrow_mem_id.get(),
            self.borrow_book_id.get(),
            self.borrow_days.get()
        )
        if not ok:
            messagebox.showerror("Lỗi", msg)
            return

        messagebox.showinfo("Thành công", msg)
        self.load_data()
        if "books" in self.app.views:
            self.app.views["books"].load_data()
        self.app.refresh_stats()

    def do_return(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chọn mục", "Vui lòng chọn giao dịch cần trả.")
            return

        b_id = self.tree.item(sel[0])["values"][0]

        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("borrow")

        ok, msg = self.controller.return_book(b_id)
        if not ok:
            messagebox.showinfo("Thông báo", msg)
            return

        messagebox.showinfo("Hoàn tất", msg)
        self.load_data()
        if "books" in self.app.views:
            self.app.views["books"].load_data()
        if "overdue" in self.app.views:
            self.app.views["overdue"].load_data()
        self.app.refresh_stats()
