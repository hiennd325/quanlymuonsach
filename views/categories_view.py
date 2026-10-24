"""
Categories View — Màn hình Quản Lý Thể Loại Sách
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from theme import THEME, RADIUS


class CategoriesView(ctk.CTkFrame):
    def __init__(self, parent, app, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.controller = controller or getattr(app, "controllers", {}).get("category")
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left")
        ctk.CTkLabel(
            title_box,
            text="Quản Lý Thể Loại Sách",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=THEME["text_primary"]
        ).pack(anchor="w")

        # Thanh tìm kiếm dạng viên thuốc
        search_box = ctk.CTkFrame(header, fg_color="transparent")
        search_box.pack(side="right")
        self.c_search_var = tk.StringVar()

        c_search_entry = ctk.CTkEntry(
            search_box,
            placeholder_text="Tìm theo ID, Tên thể loại...",
            textvariable=self.c_search_var,
            width=260,
            height=38,
            fg_color=THEME["input_bg"],
            border_color=THEME["input_border"],
            border_width=1,
            corner_radius=RADIUS["pill"],
            text_color=THEME["text_primary"],
            placeholder_text_color=THEME["text_muted"]
        )
        c_search_entry.pack(side="left", padx=6)
        c_search_entry.bind("<Return>", lambda _: self.load_data())

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
            command=lambda: [self.c_search_var.set(""), self.load_data()]
        ).pack(side="left", padx=3)

        # Form thao tác thể loại
        top = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        top.pack(fill="x", pady=(0, 16))

        self.c_id_var = tk.StringVar()
        self.c_name_var = tk.StringVar()

        ctk.CTkLabel(
            top,
            text="Tên thể loại:",
            font=ctk.CTkFont(size=12),
            text_color=THEME["text_secondary"]
        ).grid(row=0, column=0, padx=(16, 8), pady=14, sticky="e")

        ctk.CTkEntry(
            top,
            textvariable=self.c_name_var,
            width=260,
            height=36,
            fg_color=THEME["input_bg"],
            border_color=THEME["input_border"],
            border_width=1,
            corner_radius=RADIUS["input"],
            text_color=THEME["text_primary"],
            placeholder_text="Ví dụ: Khoa Học, Văn Học, ..."
        ).grid(row=0, column=1, padx=6, pady=14)

        ctk.CTkButton(
            top,
            text="Thêm Mới",
            width=100,
            height=36,
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=RADIUS["pill"],
            command=self.add_category
        ).grid(row=0, column=2, padx=6)

        ctk.CTkButton(
            top,
            text="Cập Nhật",
            width=100,
            height=36,
            fg_color=THEME["accent_orange"],
            hover_color=THEME["accent_orange_hover"],
            text_color=THEME["text_white"],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=RADIUS["pill"],
            command=self.update_category
        ).grid(row=0, column=3, padx=6)

        ctk.CTkButton(
            top,
            text="Xóa",
            width=80,
            height=36,
            fg_color=THEME["accent_red"],
            hover_color=THEME["accent_red_hover"],
            text_color=THEME["text_white"],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=RADIUS["pill"],
            command=self.delete_category
        ).grid(row=0, column=4, padx=6)

        ctk.CTkButton(
            top,
            text="Làm Mới",
            width=90,
            height=36,
            fg_color=THEME["btn_secondary"],
            hover_color=THEME["btn_secondary_hover"],
            text_color=THEME["btn_secondary_text"],
            font=ctk.CTkFont(size=12),
            corner_radius=RADIUS["pill"],
            command=self.clear_form
        ).grid(row=0, column=5, padx=6)

        # Bảng dữ liệu thể loại
        tbl_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        tbl_card.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tbl_card, columns=("id", "name", "book_count"), show="headings")
        cols = [
            ("id", "Mã", 80),
            ("name", "Tên Thể Loại", 400),
            ("book_count", "Số Lượng Đầu Sách", 160)
        ]
        for c, h, w in cols:
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="center" if c in ("id", "book_count") else "w")

        self.tree.pack(fill="both", expand=True, padx=14, pady=14)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def load_data(self):
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("category")
        if not self.controller or (hasattr(self.app, "db") and self.app.db.connection_error):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        kw = self.c_search_var.get().strip() if hasattr(self, "c_search_var") else None
        categories = self.controller.get_categories(kw)
        for cat in categories:
            self.tree.insert("", "end", values=(cat["id"], cat["name"], cat.get("book_count", 0)))

    def on_select(self, _):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0])["values"]
        self.c_id_var.set(v[0])
        self.c_name_var.set(v[1])

    def clear_form(self):
        self.c_id_var.set("")
        self.c_name_var.set("")
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

    def add_category(self):
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("category")

        ok, msg = self.controller.add_category(self.c_name_var.get())
        if not ok:
            messagebox.showwarning("Lỗi", msg)
            return

        self.clear_form()
        self.load_data()
        self._notify_changes()

    def update_category(self):
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("category")

        cat_id = self.c_id_var.get()
        if not cat_id:
            messagebox.showwarning("Chọn mục", "Vui lòng chọn thể loại cần cập nhật từ danh sách.")
            return

        ok, msg = self.controller.update_category(cat_id, self.c_name_var.get())
        if not ok:
            messagebox.showwarning("Lỗi", msg)
            return

        self.clear_form()
        self.load_data()
        self._notify_changes()

    def delete_category(self):
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("category")

        cat_id = self.c_id_var.get()
        if not cat_id:
            messagebox.showwarning("Chọn mục", "Vui lòng chọn thể loại cần xóa từ danh sách.")
            return

        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa thể loại này?"):
            return

        ok, msg = self.controller.delete_category(cat_id)
        if not ok:
            messagebox.showerror("Không thể xóa", msg)
            return

        self.clear_form()
        self.load_data()
        self._notify_changes()

    def _notify_changes(self):
        # Đồng bộ danh sách thể loại sang view Sách và cập nhật thống kê
        if hasattr(self.app, "views") and "books" in self.app.views:
            if hasattr(self.app.views["books"], "refresh_categories"):
                self.app.views["books"].refresh_categories()
        if hasattr(self.app, "refresh_stats"):
            self.app.refresh_stats()
