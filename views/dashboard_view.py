"""
Dashboard View — Màn hình Tổng Quan giao diện LibMaster
"""
from tkinter import ttk
import customtkinter as ctk

from theme import THEME, RADIUS
from widgets import WavyChartWidget, DonutChartWidget, PillProgressBar, MiniBarWidget


class DashboardView(ctk.CTkScrollableFrame):
    """
    Màn hình Tổng Quan mô phỏng sát bố cục và phong cách trong ảnh mẫu:
    - Đồ thị sóng tím neon lượn sóng + Floating Badge thống kê
    - Donut Ring Chart + 3 thanh tiến trình bo tròn
    - Mini bar chart màu tím + Thao tác nhanh
    - Bảng hoạt động mượn trả gần nhất
    """
    def __init__(self, parent, app, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.controller = controller or getattr(app, "controllers", {}).get("dashboard")
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

        # 2. Lưới Widget chính (2 Cột)
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

        # Dock Thao Tác Nhanh
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
        if not self.controller:
            self.controller = getattr(self.app, "controllers", {}).get("dashboard")
        if not self.controller or (hasattr(self.app, "db") and self.app.db.connection_error):
            return

        data = self.controller.get_dashboard_data()
        b_total = data["books_total"]
        b_avail = data["books_available"]
        b_borrowed = data["books_borrowed"]
        m_cnt = data["members_count"]
        br_cnt = data["borrows_count"]

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

        for r in data["recent_borrows"]:
            self.tree.insert("", "end", values=(
                r["id"],
                r["member_name"],
                r["book_title"],
                r["borrow_date"],
                r["due_date"],
                r["display_status"]
            ))
