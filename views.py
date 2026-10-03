"""
Giao diện các màn hình chức năng (Views)
Thiết kế theo phong cách Obsidian & Neon Purple Glow (Không sử dụng emoji):
- Kiểu dáng phẳng, tối giản, sang trọng chuẩn phần mềm doanh nghiệp (Enterprise Grade)
- Nút bấm dạng viên thuốc (Pill shape) màu tím neon (#7857FF)
- Ô nhập liệu chìm tối (#111522)
- Các thành phần đồ họa trực quan (Đồ thị sóng tím, Donut ring, Progress bars, Mini bars)
"""
import threading
from datetime import datetime, date, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from theme import THEME, RADIUS
from widgets import WavyChartWidget, DonutChartWidget, PillProgressBar, MiniBarWidget
from mailer import send_reminder_email


class DashboardView(ctk.CTkScrollableFrame):
    """
    Màn hình Tổng Quan mô phỏng sát bố cục và phong cách trong ảnh mẫu:
    - Đồ thị sóng tím neon lượn sóng + Floating Badge thống kê
    - Donut Ring Chart + 3 thanh tiến trình bo tròn
    - Mini bar chart màu tím + Thao tác nhanh
    - Bảng hoạt động mượn trả gần nhất
    """
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.db = app.db
        self.setup_ui()

    def setup_ui(self):
        # 1. Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left")
        ctk.CTkLabel(
            title_box,
            text="Tổng Quan Hệ Thống",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=THEME["text_white"]
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_box,
            text="Theo dõi chỉ số vận hành và giao dịch lưu thông thư viện",
            font=ctk.CTkFont(size=12),
            text_color=THEME["text_secondary"]
        ).pack(anchor="w")

        # Nút hành động nhanh trên header
        action_bar = ctk.CTkFrame(header, fg_color="transparent")
        action_bar.pack(side="right")
        ctk.CTkButton(
            action_bar,
            text="Mượn Sách Nhanh",
            command=lambda: self.app.show_page("borrows"),
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36,
            corner_radius=RADIUS["pill"]
        ).pack(side="left", padx=4)

        # 2. Lưới Widget chính (2 Cột lấy cảm hứng từ ảnh mẫu)
        grid_top = ctk.CTkFrame(self, fg_color="transparent")
        grid_top.pack(fill="x", pady=(0, 16))
        grid_top.grid_columnconfigure((0, 1), weight=1, uniform="dash_cols")

        # Cột trái: Đồ thị sóng tím + Mini bar transaction
        left_col = ctk.CTkFrame(grid_top, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.wavy_card = WavyChartWidget(left_col, title="Xu Hướng Mượn Sách 5 Tháng Gần Nhất")
        self.wavy_card.pack(fill="x", pady=(0, 12))

        self.mini_bar_card = MiniBarWidget(
            left_col,
            title="Xem Giao Dịch  →",
            on_click=lambda: self.app.show_page("borrows")
        )
        self.mini_bar_card.pack(fill="x")

        # Cột phải: Thẻ Thống kê & Phân Bổ (Donut Chart + Progress Bars)
        right_col = ctk.CTkFrame(grid_top, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        dist_card = ctk.CTkFrame(
            right_col,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        dist_card.pack(fill="both", expand=True)

        dist_head = ctk.CTkFrame(dist_card, fg_color="transparent")
        dist_head.pack(fill="x", padx=18, pady=(16, 6))
        ctk.CTkLabel(
            dist_head,
            text="Phân Bổ & Trạng Thái Kho",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=THEME["text_white"]
        ).pack(side="left")

        inner_dist = ctk.CTkFrame(dist_card, fg_color="transparent")
        inner_dist.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        inner_dist.grid_columnconfigure(0, weight=1)
        inner_dist.grid_columnconfigure(1, weight=1)

        # Biểu đồ Donut bên trái thẻ
        self.donut_widget = DonutChartWidget(inner_dist, title="", center_text="0", center_sub="Đầu sách")
        self.donut_widget.grid(row=0, column=0, padx=6, pady=4, sticky="nsew")

        # 3 Thanh Progress Bars
        bars_box = ctk.CTkFrame(inner_dist, fg_color="transparent")
        bars_box.grid(row=0, column=1, padx=6, pady=4, sticky="nsew")

        self.pbar_avail = PillProgressBar(bars_box, label="Sách Sẵn Có", percent=0.85, color=THEME["primary"])
        self.pbar_avail.pack(fill="x", pady=6)

        self.pbar_borrow = PillProgressBar(bars_box, label="Đang Cho Mượn", percent=0.15, color=THEME["accent_orange"])
        self.pbar_borrow.pack(fill="x", pady=6)

        self.pbar_members = PillProgressBar(bars_box, label="Bạn Đọc Hoạt Động", percent=0.6, color=THEME["accent_cyan"])
        self.pbar_members.pack(fill="x", pady=6)

        # Dock Thao Tác Nhanh (Thanh nút bo tròn tinh gọn)
        quick_dock = ctk.CTkFrame(
            right_col,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        quick_dock.pack(fill="x", pady=(12, 0))

        dock_inner = ctk.CTkFrame(quick_dock, fg_color="transparent")
        dock_inner.pack(fill="x", padx=12, pady=10)
        dock_inner.grid_columnconfigure((0, 1, 2, 3), weight=1)

        dock_actions = [
            ("Thêm Sách", "books", THEME["card_inner"]),
            ("Bạn Đọc", "members", THEME["card_inner"]),
            ("Trả Sách", "borrows", THEME["primary"]),
            ("Quá Hạn", "overdue", THEME["card_inner"]),
        ]
        for i, (txt, target, bg) in enumerate(dock_actions):
            btn = ctk.CTkButton(
                dock_inner,
                text=txt,
                height=34,
                fg_color=bg,
                hover_color=THEME["primary_hover"] if bg == THEME["primary"] else THEME["btn_secondary_hover"],
                text_color=THEME["text_white"],
                font=ctk.CTkFont(size=11, weight="bold"),
                corner_radius=RADIUS["pill"],
                command=lambda t=target: self.app.show_page(t)
            )
            btn.grid(row=0, column=i, padx=4, sticky="ew")

        # 3. Bảng Giao Dịch Gần Nhất
        table_container = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        table_container.pack(fill="both", expand=True, pady=(0, 10))

        t_head = ctk.CTkFrame(table_container, fg_color="transparent")
        t_head.pack(fill="x", padx=18, pady=(16, 8))
        ctk.CTkLabel(
            t_head,
            text="Giao Dịch Mượn Sách Mới Nhất",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=THEME["text_white"]
        ).pack(side="left")

        ctk.CTkButton(
            t_head,
            text="Xem Tất Cả",
            height=28,
            width=90,
            fg_color=THEME["btn_secondary"],
            hover_color=THEME["btn_secondary_hover"],
            text_color=THEME["btn_secondary_text"],
            corner_radius=RADIUS["pill"],
            font=ctk.CTkFont(size=11),
            command=lambda: self.app.show_page("borrows")
        ).pack(side="right")

        self.tree = ttk.Treeview(
            table_container,
            columns=("id", "member", "book", "borrow_date", "due_date", "status"),
            show="headings",
            height=6
        )
        cols = [
            ("id", "Mã", 60),
            ("member", "Bạn Đọc", 220),
            ("book", "Tên Sách", 320),
            ("borrow_date", "Ngày Mượn", 110),
            ("due_date", "Hạn Trả", 110),
            ("status", "Trạng Thái", 130),
        ]
        for c, h, w in cols:
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="center" if c in ("id", "borrow_date", "due_date", "status") else "w")

        self.tree.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    def load_data(self):
        if self.db.connection_error:
            return

        b_cnt_res = self.db.query("SELECT COUNT(*) as c, COALESCE(SUM(total), 0) as tot, COALESCE(SUM(available), 0) as av FROM books")
        b_cnt = b_cnt_res[0]["c"]
        b_total = b_cnt_res[0]["tot"]
        b_avail = b_cnt_res[0]["av"]
        b_borrowed = max(0, b_total - b_avail)

        m_cnt = self.db.query("SELECT COUNT(*) as c FROM members")[0]["c"]
        br_cnt = self.db.query("SELECT COUNT(*) as c FROM borrows")[0]["c"]

        # Cập nhật Donut Chart
        display_books = f"{b_total:,}" if b_total < 10000 else f"{b_total//1000}k"
        self.donut_widget.update_center(display_books, "Tổng bản sách")

        # Cập nhật Progress Bars
        if b_total > 0:
            avail_pct = b_avail / b_total
            borrow_pct = b_borrowed / b_total
        else:
            avail_pct, borrow_pct = 1.0, 0.0

        self.pbar_avail.set_progress(avail_pct, f"{b_avail}/{b_total}")
        self.pbar_borrow.set_progress(borrow_pct, f"{b_borrowed}/{b_total}")
        self.pbar_members.set_progress(min(1.0, m_cnt / 50.0 if m_cnt else 0.1), f"{m_cnt} bạn đọc")

        # Cập nhật Wavy Chart Badge
        self.wavy_card.set_data(
            stat_label="Lượt mượn tích lũy",
            stat_val=f"{br_cnt:,}",
            trend="+8.5%  ↑"
        )

        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.db.query("""
            SELECT b.id, m.name as member_name, bk.title as book_title, b.borrow_date, b.due_date, b.status
            FROM borrows b
            JOIN members m ON b.member_id = m.id
            JOIN books bk ON b.book_id = bk.id
            ORDER BY b.id DESC LIMIT 8
        """)
        today = date.today().strftime("%Y-%m-%d")
        for r in rows:
            st = "Quá hạn" if r["status"] == "borrowed" and r["due_date"] < today else ("Đang mượn" if r["status"] == "borrowed" else "Đã trả")
            self.tree.insert("", "end", values=(r["id"], r["member_name"], r["book_title"], r["borrow_date"], r["due_date"], st))


class BooksView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.db = app.db
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
        for item in self.tree.get_children():
            self.tree.delete(item)
        kw = f"%{self.b_search_var.get().strip()}%"
        rows = self.db.query("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR category LIKE %s ORDER BY id DESC", (kw, kw, kw))
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
        t, a, c = self.b_title_var.get().strip(), self.b_author_var.get().strip(), self.b_cat_var.get().strip()
        try:
            total = int(self.b_total_var.get())
            if not t or total <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên sách và số lượng hợp lệ.")
            return
        self.db.execute("INSERT INTO books (title, author, category, total, available) VALUES (%s, %s, %s, %s, %s)", (t, a, c, total, total))
        self.clear_form()
        self.load_data()
        self.app.refresh_stats()

    def update_book(self):
        b_id = self.b_id_var.get()
        if not b_id:
            messagebox.showwarning("Lỗi", "Hãy chọn sách cần cập nhật.")
            return
        t, a, c = self.b_title_var.get().strip(), self.b_author_var.get().strip(), self.b_cat_var.get().strip()
        total = int(self.b_total_var.get())
        old = self.db.query("SELECT total, available FROM books WHERE id=%s", (b_id,))[0]
        new_avail = max(0, old["available"] + (total - old["total"]))
        self.db.execute("UPDATE books SET title=%s, author=%s, category=%s, total=%s, available=%s WHERE id=%s", (t, a, c, total, new_avail, b_id))
        self.clear_form()
        self.load_data()
        self.app.refresh_stats()

    def delete_book(self):
        b_id = self.b_id_var.get()
        if not b_id or not messagebox.askyesno("Xác nhận", "Xóa sách này khỏi kho?"):
            return
        self.db.execute("DELETE FROM books WHERE id=%s", (b_id,))
        self.clear_form()
        self.load_data()
        self.app.refresh_stats()


class MembersView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.db = app.db
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
            text_color=THEME["text_white"]
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
                text_color=THEME["text_white"]
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
        for item in self.tree.get_children():
            self.tree.delete(item)
        members = self.db.query("SELECT * FROM members ORDER BY id DESC")
        for m in members:
            active = self.db.query("SELECT COUNT(*) as cnt FROM borrows WHERE member_id=%s AND status='borrowed'", (m["id"],))[0]["cnt"]
            self.tree.insert("", "end", values=(m["id"], m["name"], m["email"], m["phone"], active))

    def add_member(self):
        name = self.m_name_var.get().strip()
        email = self.m_email_var.get().strip()
        phone = self.m_phone_var.get().strip()
        if not name or "@" not in email:
            messagebox.showwarning("Lỗi", "Vui lòng nhập họ tên và email hợp lệ.")
            return
        self.db.execute("INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        self.m_name_var.set("")
        self.m_email_var.set("")
        self.m_phone_var.set("")
        self.load_data()
        self.app.refresh_stats()

    def delete_member(self):
        sel = self.tree.selection()
        if not sel or not messagebox.askyesno("Xác nhận", "Xóa độc giả này?"):
            return
        m_id = self.tree.item(sel[0])["values"][0]
        self.db.execute("DELETE FROM members WHERE id=%s", (m_id,))
        self.load_data()
        self.app.refresh_stats()


class BorrowsView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.db = app.db
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
            text_color=THEME["text_white"]
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
            text_color=THEME["text_white"]
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
            text_color=THEME["text_white"]
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
            text_color=THEME["text_white"],
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
            text_color="#0B0E17",
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
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = self.db.query("""
            SELECT b.id, m.name as member_name, bk.title as book_title, b.borrow_date, b.due_date, b.return_date, b.status, b.fine_amount
            FROM borrows b JOIN members m ON b.member_id = m.id JOIN books bk ON b.book_id = bk.id
            ORDER BY b.id DESC
        """)
        today = date.today().strftime("%Y-%m-%d")
        for r in rows:
            st = "Quá hạn" if r["status"] == "borrowed" and r["due_date"] < today else ("Đang mượn" if r["status"] == "borrowed" else "Đã trả")
            self.tree.insert("", "end", values=(r["id"], r["member_name"], r["book_title"], r["borrow_date"], r["due_date"], r["return_date"] or "-", st, f"{r['fine_amount']:,}đ"))

    def do_borrow(self):
        try:
            m_id = int(self.borrow_mem_id.get())
            b_id = int(self.borrow_book_id.get())
            days = int(self.borrow_days.get().split()[0])
        except ValueError:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đúng ID độc giả và ID sách.")
            return
        book = self.db.query("SELECT * FROM books WHERE id=%s", (b_id,))
        if not book or book[0]["available"] <= 0:
            messagebox.showerror("Hết sách", "Sách này hiện đã được mượn hết.")
            return
        b_date = date.today()
        d_date = b_date + timedelta(days=days)
        self.db.execute("INSERT INTO borrows (book_id, member_id, borrow_date, due_date, status) VALUES (%s, %s, %s, %s, 'borrowed')",
                        (b_id, m_id, b_date.strftime("%Y-%m-%d"), d_date.strftime("%Y-%m-%d")))
        self.db.execute("UPDATE books SET available = available - 1 WHERE id=%s", (b_id,))
        messagebox.showinfo("Thành công", f"Đã ghi nhận mượn sách. Hạn trả: {d_date.strftime('%Y-%m-%d')}")
        self.load_data()
        self.app.views["books"].load_data()
        self.app.refresh_stats()

    def do_return(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chọn mục", "Vui lòng chọn giao dịch cần trả.")
            return
        b_id = self.tree.item(sel[0])["values"][0]
        borrow = self.db.query("SELECT * FROM borrows WHERE id=%s", (b_id,))[0]
        if borrow["status"] == "returned":
            messagebox.showinfo("Thông báo", "Sách này đã được trả.")
            return
        ret_date = date.today()
        due_date = datetime.strptime(borrow["due_date"], "%Y-%m-%d").date()
        overdue_days = max(0, (ret_date - due_date).days)
        fine = overdue_days * self.app.cfg.get("fine_per_day", 5000)

        self.db.execute("UPDATE borrows SET return_date=%s, fine_amount=%s, status='returned' WHERE id=%s",
                        (ret_date.strftime("%Y-%m-%d"), fine, b_id))
        self.db.execute("UPDATE books SET available = available + 1 WHERE id=%s", (borrow["book_id"],))
        msg = f"Đã trả sách ngày {ret_date.strftime('%Y-%m-%d')}."
        if fine > 0:
            msg += f"\nQuá hạn {overdue_days} ngày. Phí phạt: {fine:,} VND."
        messagebox.showinfo("Hoàn tất", msg)
        self.load_data()
        self.app.views["books"].load_data()
        self.app.views["overdue"].load_data()
        self.app.refresh_stats()


class OverdueView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.db = app.db
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
            text_color=THEME["text_white"]
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
            text_color="#10141D",
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
            text_color=THEME["text_white"]
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
        for item in self.tree.get_children():
            self.tree.delete(item)
        today = date.today().strftime("%Y-%m-%d")
        rows = self.db.query("""
            SELECT b.id, m.name, m.email, bk.title, b.due_date
            FROM borrows b JOIN members m ON b.member_id = m.id JOIN books bk ON b.book_id = bk.id
            WHERE b.status = 'borrowed' AND b.due_date < %s
            ORDER BY b.due_date ASC
        """, (today,))

        total_fine = 0
        rate = self.app.cfg.get("fine_per_day", 5000)
        today_date = date.today()

        for r in rows:
            d_date = datetime.strptime(r["due_date"], "%Y-%m-%d").date()
            over_days = (today_date - d_date).days
            fine = over_days * rate
            total_fine += fine
            self.tree.insert("", "end", values=(r["id"], r["name"], r["email"], r["title"], r["due_date"], f"{over_days} ngày", f"{fine:,} VND"))

        if len(rows) > 0:
            self.overdue_banner.configure(fg_color=THEME["accent_red_subtle"], border_color=THEME["accent_red"])
            self.overdue_summary.configure(text=f"Phát hiện {len(rows)} lượt mượn quá hạn  |  Tổng tiền phạt ước tính: {total_fine:,} VND")
        else:
            self.overdue_banner.configure(fg_color=THEME["accent_cyan_subtle"], border_color=THEME["accent_cyan"])
            self.overdue_summary.configure(text="Hiện không có lượt mượn nào bị quá hạn.")

    def send_single_reminder(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chọn mục", "Vui lòng chọn 1 dòng để gửi email.")
            return
        v = self.tree.item(sel[0])["values"]

        def worker():
            ok = send_reminder_email(self.app.cfg, v[2], v[1], v[3], v[4], v[6])
            if ok:
                messagebox.showinfo("Thành công", f"Đã gửi email nhắc nhở tới {v[2]}.")
            else:
                messagebox.showerror("Thất bại", f"Không thể gửi email tới {v[2]}. Kiểm tra .env.")

        threading.Thread(target=worker, daemon=True).start()

    def send_bulk_reminders(self):
        today = date.today().strftime("%Y-%m-%d")
        rows = self.db.query("""
            SELECT m.name, m.email, bk.title, b.due_date
            FROM borrows b JOIN members m ON b.member_id = m.id JOIN books bk ON b.book_id = bk.id
            WHERE b.status = 'borrowed' AND b.due_date <= %s
        """, (today,))
        if not rows:
            messagebox.showinfo("Thông báo", "Không có bạn đọc nào đến hạn hoặc quá hạn hôm nay.")
            return

        def bulk_worker():
            success = 0
            for r in rows:
                if send_reminder_email(self.app.cfg, r["email"], r["name"], r["title"], r["due_date"]):
                    success += 1
            messagebox.showinfo("Hoàn tất", f"Đã gửi nhắc nhở email thành công cho {success}/{len(rows)} bạn đọc.")

        threading.Thread(target=bulk_worker, daemon=True).start()


class ReportsView(ctk.CTkScrollableFrame):
    """
    Màn hình Báo Cáo & Phân Tích Thống Kê cao cấp:
    - 4 Thẻ KPI bo góc thiết kế tối giản, thanh lịch
    - Phân tích Top Sách & Top Thể Loại
    """
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.db = app.db
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left")
        ctk.CTkLabel(
            title_box,
            text="Báo Cáo & Phân Tích Thống Kê",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=THEME["text_white"]
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_box,
            text="Tổng hợp số liệu vận hành, tỷ lệ mượn và cơ cấu danh mục sách",
            font=ctk.CTkFont(size=12),
            text_color=THEME["text_secondary"]
        ).pack(anchor="w")

        # 4 Thẻ KPI bo góc chuẩn phong cách phẳng
        cards_grid = ctk.CTkFrame(self, fg_color="transparent")
        cards_grid.pack(fill="x", pady=(0, 16))
        cards_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.kpi_widgets = {}
        kpi_defs = [
            ("books", "Tổng Đầu Sách", THEME["primary"]),
            ("members", "Tổng Bạn Đọc", THEME["accent_cyan"]),
            ("borrows", "Tổng Lượt Mượn", THEME["primary_glow"]),
            ("fines", "Tiền Phạt Thu Về", THEME["accent_orange"])
        ]
        for idx, (k, title, color) in enumerate(kpi_defs):
            card = ctk.CTkFrame(
                cards_grid,
                fg_color=THEME["card_bg"],
                corner_radius=RADIUS["card"],
                border_color=THEME["card_border"],
                border_width=1
            )
            card.grid(row=0, column=idx, padx=6, sticky="ew")

            top_row = ctk.CTkFrame(card, fg_color="transparent")
            top_row.pack(fill="x", padx=16, pady=(16, 4))

            ctk.CTkLabel(
                top_row,
                text=title,
                font=ctk.CTkFont(size=12),
                text_color=THEME["text_secondary"]
            ).pack(side="left")

            val_lbl = ctk.CTkLabel(
                card,
                text="0",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=color
            )
            val_lbl.pack(anchor="w", padx=16, pady=(0, 16))
            self.kpi_widgets[k] = val_lbl

        # Bảng Top Sách & Top Thể Loại
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        grid_frame.grid_columnconfigure((0, 1), weight=1)

        c1 = ctk.CTkFrame(
            grid_frame,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        c1.grid(row=0, column=0, padx=6, sticky="nsew")

        ctk.CTkLabel(
            c1,
            text="Top Sách Được Mượn Nhiều Nhất",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=THEME["text_white"]
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.top_books_tree = ttk.Treeview(c1, columns=("title", "count"), show="headings", height=8)
        self.top_books_tree.heading("title", text="Tên Sách")
        self.top_books_tree.heading("count", text="Lượt Mượn")
        self.top_books_tree.column("title", width=280)
        self.top_books_tree.column("count", width=80, anchor="center")
        self.top_books_tree.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        c2 = ctk.CTkFrame(
            grid_frame,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        c2.grid(row=0, column=1, padx=6, sticky="nsew")

        ctk.CTkLabel(
            c2,
            text="Thể Loại Sách Phổ Biến Nhất",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=THEME["text_white"]
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.top_cats_tree = ttk.Treeview(c2, columns=("cat", "count"), show="headings", height=8)
        self.top_cats_tree.heading("cat", text="Thể Loại")
        self.top_cats_tree.heading("count", text="Tổng Mượn")
        self.top_cats_tree.column("cat", width=220)
        self.top_cats_tree.column("count", width=80, anchor="center")
        self.top_cats_tree.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    def load_data(self):
        if self.db.connection_error:
            return

        b_cnt = self.db.query("SELECT COUNT(*) as c FROM books")[0]["c"]
        m_cnt = self.db.query("SELECT COUNT(*) as c FROM members")[0]["c"]
        br_cnt = self.db.query("SELECT COUNT(*) as c FROM borrows")[0]["c"]
        fine_sum = self.db.query("SELECT SUM(fine_amount) as s FROM borrows")[0]["s"] or 0

        self.kpi_widgets["books"].configure(text=str(b_cnt))
        self.kpi_widgets["members"].configure(text=str(m_cnt))
        self.kpi_widgets["borrows"].configure(text=str(br_cnt))
        self.kpi_widgets["fines"].configure(text=f"{int(fine_sum):,}đ")

        for item in self.top_books_tree.get_children():
            self.top_books_tree.delete(item)
        for r in self.db.query("""
            SELECT bk.title, COUNT(b.id) as cnt
            FROM borrows b JOIN books bk ON b.book_id = bk.id
            GROUP BY bk.id, bk.title ORDER BY cnt DESC LIMIT 10
        """):
            self.top_books_tree.insert("", "end", values=(r["title"], r["cnt"]))

        for item in self.top_cats_tree.get_children():
            self.top_cats_tree.delete(item)
        for r in self.db.query("""
            SELECT bk.category, COUNT(b.id) as cnt
            FROM borrows b JOIN books bk ON b.book_id = bk.id
            GROUP BY bk.category ORDER BY cnt DESC LIMIT 10
        """):
            self.top_cats_tree.insert("", "end", values=(r["category"], r["cnt"]))
