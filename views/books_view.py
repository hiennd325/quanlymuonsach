"""
Books View — Màn hình Quản Lý Sách
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from theme import THEME, RADIUS


class BooksView(ctk.CTkFrame):
    def __init__(self, parent, app, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.controller = controller or getattr(app, "controllers", {}).get("book")
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left")
        ctk.CTkLabel(
            title_box,
            text="Quản Lý Kho Sách",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=THEME["text_white"]
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_box,
            text="Tra cứu, cập nhật danh mục và tình trạng sách trong kho",
            font=ctk.CTkFont(size=12),
            text_color=THEME["text_secondary"]
        ).pack(anchor="w")

        # Thanh tìm kiếm dạng viên thuốc
        search_box = ctk.CTkFrame(header, fg_color="transparent")
        search_box.pack(side="right")
        self.b_search_var = tk.StringVar()

        ctk.CTkEntry(
            search_box,
            placeholder_text="Tìm kiếm sách, tác giả, thể loại...",
            textvariable=self.b_search_var,
            width=270,
            height=38,
            fg_color=THEME["input_bg"],
            border_color=THEME["input_border"],
            border_width=1,
            corner_radius=RADIUS["pill"],
            text_color=THEME["text_white"],
            placeholder_text_color=THEME["text_muted"]
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            search_box,
            text="Tìm Kiếm",
            width=85,
            height=38,
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=RADIUS["pill"],
            command=self.load_data
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            search_box,
            text="Tất Cả",
            width=70,
            height=38,
            fg_color=THEME["btn_secondary"],
            hover_color=THEME["btn_secondary_hover"],
            text_color=THEME["btn_secondary_text"],
            font=ctk.CTkFont(size=12),
            corner_radius=RADIUS["pill"],
            command=lambda: [self.b_search_var.set(""), self.load_data()]
        ).pack(side="left", padx=3)

        # Thẻ Bảng Dữ Liệu
        tbl_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        tbl_card.pack(fill="both", expand=True, pady=(0, 16))

        self.tree = ttk.Treeview(tbl_card, columns=("id", "title", "author", "cat", "total", "avail"), show="headings")
        cols = [
            ("id", "ID", 60),
            ("title", "Tên Sách", 340),
            ("author", "Tác Giả", 200),
            ("cat", "Thể Loại", 140),
            ("total", "Tổng Số", 80),
            ("avail", "Sẵn Có", 80)
        ]
        for c, h, w in cols:
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="center" if c in ("id", "total", "avail") else "w")

        self.tree.pack(fill="both", expand=True, padx=14, pady=14)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Thẻ Form Thêm / Sửa
        form = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        form.pack(fill="x")

        self.b_id_var, self.b_title_var = tk.StringVar(), tk.StringVar()
        self.b_author_var, self.b_cat_var, self.b_total_var = tk.StringVar(), tk.StringVar(), tk.StringVar(value="1")

        grid_layout = [
            ("Tên sách:", self.b_title_var, 0, 0, 260),
            ("Tác giả:", self.b_author_var, 0, 2, 200),
            ("Thể loại:", self.b_cat_var, 1, 0, 260),
            ("Số lượng:", self.b_total_var, 1, 2, 200),
        ]
        for lbl, var, r, c, w in grid_layout:
            ctk.CTkLabel(
                form,
                text=lbl,
                font=ctk.CTkFont(size=12),
                text_color=THEME["text_secondary"]
            ).grid(row=r, column=c, padx=14, pady=10, sticky="e")

            ctk.CTkEntry(
                form,
                textvariable=var,
                width=w,
                height=34,
                fg_color=THEME["input_bg"],
                border_color=THEME["input_border"],
                border_width=1,
                corner_radius=RADIUS["input"],
                text_color=THEME["text_white"]
            ).grid(row=r, column=c+1, padx=6, pady=10, sticky="w")

        # Các nút bấm thao tác dạng viên thuốc
        btn_box = ctk.CTkFrame(form, fg_color="transparent")
        btn_box.grid(row=0, column=4, rowspan=2, padx=20, pady=10)

        ctk.CTkButton(
            btn_box,
            text="Thêm Mới",
            width=100,
            height=34,
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=RADIUS["pill"],
            command=self.add_book
        ).grid(row=0, column=0, padx=4, pady=4)

        ctk.CTkButton(
            btn_box,
            text="Cập Nhật",
            width=100,
            height=34,
            fg_color=THEME["accent_orange"],
            hover_color=THEME["accent_orange_hover"],
            text_color="#10141D",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=RADIUS["pill"],
            command=self.update_book
        ).grid(row=0, column=1, padx=4, pady=4)

        ctk.CTkButton(
            btn_box,
            text="Xóa",
            width=100,
            height=34,
            fg_color=THEME["accent_red"],
            hover_color=THEME["accent_red_hover"],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=RADIUS["pill"],
            command=self.delete_book
        ).grid(row=1, column=0, padx=4, pady=4)

        ctk.CTkButton(
            btn_box,
            text="Làm Mới",
            width=100,
            height=34,
            fg_color=THEME["btn_secondary"],
            hover_color=THEME["btn_secondary_hover"],
            text_color=THEME["btn_secondary_text"],
            font=ctk.CTkFont(size=12),
            corner_radius=RADIUS["pill"],
            command=self.clear_form
        ).grid(row=1, column=1, padx=4, pady=4)

    def load_data(self):
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("book")
        if not self.controller or (hasattr(self.app, "db") and self.app.db.connection_error):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        kw = self.b_search_var.get().strip()
        rows = self.controller.get_books(kw)
        for r in rows:
            self.tree.insert("", "end", values=(r["id"], r["title"], r["author"], r["category"], r["total"], r["available"]))

    def on_select(self, _):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0])["values"]
        self.b_id_var.set(v[0])
        self.b_title_var.set(v[1])
        self.b_author_var.set(v[2])
        self.b_cat_var.set(v[3])
        self.b_total_var.set(v[4])

    def clear_form(self):
        self.b_id_var.set("")
        self.b_title_var.set("")
        self.b_author_var.set("")
        self.b_cat_var.set("")
        self.b_total_var.set("1")

    def add_book(self):
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("book")

        ok, msg = self.controller.add_book(
            self.b_title_var.get(),
            self.b_author_var.get(),
            self.b_cat_var.get(),
            self.b_total_var.get()
        )
        if not ok:
            messagebox.showwarning("Lỗi", msg)
            return

        self.clear_form()
        self.load_data()
        self.app.refresh_stats()

    def update_book(self):
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("book")

        b_id = self.b_id_var.get()
        ok, msg = self.controller.update_book(
            b_id,
            self.b_title_var.get(),
            self.b_author_var.get(),
            self.b_cat_var.get(),
            self.b_total_var.get()
        )
        if not ok:
            messagebox.showwarning("Lỗi", msg)
            return

        self.clear_form()
        self.load_data()
        self.app.refresh_stats()

    def delete_book(self):
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("book")

        b_id = self.b_id_var.get()
        if not b_id:
            messagebox.showwarning("Lỗi", "Hãy chọn sách cần xóa.")
            return

        if not messagebox.askyesno("Xác nhận", "Xóa sách này khỏi kho?"):
            return

        ok, msg = self.controller.delete_book(b_id)
        if not ok:
            messagebox.showerror("Lỗi", msg)
            return

        self.clear_form()
        self.load_data()
        self.app.refresh_stats()
