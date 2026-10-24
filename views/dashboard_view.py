"""
Dashboard View — Màn hình Tổng Quan giao diện LibMaster
"""
from tkinter import ttk
import customtkinter as ctk

from theme import THEME, RADIUS
from widgets import DonutChartWidget, PillProgressBar


class DashboardView(ctk.CTkScrollableFrame):
    """
    Màn hình Tổng Quan:
    - 4 Thẻ KPI thống kê số liệu thực tế từ cơ sở dữ liệu
    - Thẻ Phân bổ kho sách (Donut Ring Chart + Thanh tiến trình tỷ lệ)
    - Dock thao tác nhanh điều hướng các chức năng
    - Bảng danh sách giao dịch mượn trả mới nhất
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
            text_color=THEME["text_primary"]
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
            text_color=THEME["text_white"],
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36,
            corner_radius=RADIUS["pill"]
        ).pack(side="left", padx=4)

        # 2. Hàng 4 Thẻ KPI thống kê
        kpi_grid = ctk.CTkFrame(self, fg_color="transparent")
        kpi_grid.pack(fill="x", pady=(0, 16))
        kpi_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.kpi_widgets = {}
        kpi_defs = [
            ("books", "Tổng Đầu Sách", THEME["primary"]),
            ("total", "Tổng Bản Sách", THEME["accent_cyan"]),
            ("borrowed", "Đang Cho Mượn", THEME["accent_orange"]),
            ("members", "Bạn Đọc Đăng Ký", THEME["primary_glow"]),
        ]
        for idx, (k, title, color) in enumerate(kpi_defs):
            card = ctk.CTkFrame(
                kpi_grid,
                fg_color=THEME["card_bg"],
                corner_radius=RADIUS["card"],
                border_color=THEME["card_border"],
                border_width=1
            )
            card.grid(row=0, column=idx, padx=6 if idx in (1, 2) else (0 if idx == 0 else 0), sticky="ew")
            if idx == 0:
                card.grid(row=0, column=0, padx=(0, 6), sticky="ew")
            elif idx == 3:
                card.grid(row=0, column=3, padx=(6, 0), sticky="ew")

            top_row = ctk.CTkFrame(card, fg_color="transparent")
            top_row.pack(fill="x", padx=16, pady=(14, 4))

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
            val_lbl.pack(anchor="w", padx=16, pady=(0, 14))
            self.kpi_widgets[k] = val_lbl

        # 3. Khu vực Thống kê Phân bổ kho & Thao tác nhanh
        middle_grid = ctk.CTkFrame(self, fg_color="transparent")
        middle_grid.pack(fill="x", pady=(0, 16))
        middle_grid.grid_columnconfigure(0, weight=3)
        middle_grid.grid_columnconfigure(1, weight=2)

        # Cột trái: Phân bổ kho sách (Donut chart + 3 progress bars)
        dist_card = ctk.CTkFrame(
            middle_grid,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        dist_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        dist_head = ctk.CTkFrame(dist_card, fg_color="transparent")
        dist_head.pack(fill="x", padx=18, pady=(16, 6))
        ctk.CTkLabel(
            dist_head,
            text="Phân Bổ & Trạng Thái Kho Sách",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=THEME["text_primary"]
        ).pack(side="left")

        inner_dist = ctk.CTkFrame(dist_card, fg_color="transparent")
        inner_dist.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        inner_dist.grid_columnconfigure(0, weight=1)
        inner_dist.grid_columnconfigure(1, weight=1)

        self.donut_widget = DonutChartWidget(inner_dist, title="", center_text="0", center_sub="Bản sách")
        self.donut_widget.grid(row=0, column=0, padx=6, pady=4, sticky="nsew")

        bars_box = ctk.CTkFrame(inner_dist, fg_color="transparent")
        bars_box.grid(row=0, column=1, padx=6, pady=4, sticky="nsew")

        self.pbar_avail = PillProgressBar(bars_box, label="Sách Sẵn Có", percent=0.85, color=THEME["primary"])
        self.pbar_avail.pack(fill="x", pady=6)

        self.pbar_borrow = PillProgressBar(bars_box, label="Đang Cho Mượn", percent=0.15, color=THEME["accent_orange"])
        self.pbar_borrow.pack(fill="x", pady=6)

        self.pbar_members = PillProgressBar(bars_box, label="Bạn Đọc Hoạt Động", percent=0.6, color=THEME["accent_cyan"])
        self.pbar_members.pack(fill="x", pady=6)

        # Cột phải: Thao Tác Nhanh
        quick_dock = ctk.CTkFrame(
            middle_grid,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1
        )
        quick_dock.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        quick_head = ctk.CTkFrame(quick_dock, fg_color="transparent")
        quick_head.pack(fill="x", padx=18, pady=(16, 12))
        ctk.CTkLabel(
            quick_head,
            text="Phím Tắt Chức Năng",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=THEME["text_primary"]
        ).pack(side="left")

        dock_inner = ctk.CTkFrame(quick_dock, fg_color="transparent")
        dock_inner.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        dock_inner.grid_columnconfigure((0, 1), weight=1)

        dock_actions = [
            ("Thêm Sách Mới", "books", THEME["primary"], THEME["text_white"]),
            ("Quản Lý Bạn Đọc", "members", THEME["card_inner"], THEME["btn_secondary_text"]),
            ("Mượn / Trả Sách", "borrows", THEME["card_inner"], THEME["btn_secondary_text"]),
            ("Kiểm Tra Quá Hạn", "overdue", THEME["card_inner"], THEME["btn_secondary_text"]),
        ]
        for i, (txt, target, bg, tc) in enumerate(dock_actions):
            r = i // 2
            c = i % 2
            btn = ctk.CTkButton(
                dock_inner,
                text=txt,
                height=42,
                fg_color=bg,
                hover_color=THEME["primary_hover"] if bg == THEME["primary"] else THEME["btn_secondary_hover"],
                text_color=tc,
                font=ctk.CTkFont(size=12, weight="bold"),
                corner_radius=RADIUS["pill"],
                command=lambda t=target: self.app.show_page(t)
            )
            btn.grid(row=r, column=c, padx=5, pady=6, sticky="ew")

        # 4. Bảng Giao Dịch Gần Nhất
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
            text_color=THEME["text_primary"]
        ).pack(side="left")

        ctk.CTkButton(
            t_head,
            text="Xem Tất Cả  →",
            height=28,
            width=110,
            fg_color=THEME["btn_secondary"],
            hover_color=THEME["btn_secondary_hover"],
            text_color=THEME["btn_secondary_text"],
            corner_radius=RADIUS["pill"],
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda: self.app.show_page("borrows")
        ).pack(side="right")

        self.tree = ttk.Treeview(
            table_container,
            columns=("id", "member", "book", "borrow_date", "due_date", "status"),
            show="headings",
            height=6
        )
        cols = [
            ("id", "ID", 50),
            ("member", "Tên Độc Giả", 180),
            ("book", "Tên Sách", 280),
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
        b_cnt = data["books_count"]
        b_total = data["books_total"]
        b_avail = data["books_available"]
        b_borrowed = data["books_borrowed"]
        m_cnt = data["members_count"]

        # Cập nhật KPI Cards
        self.kpi_widgets["books"].configure(text=f"{b_cnt:,}")
        self.kpi_widgets["total"].configure(text=f"{b_total:,}")
        self.kpi_widgets["borrowed"].configure(text=f"{b_borrowed:,}")
        self.kpi_widgets["members"].configure(text=f"{m_cnt:,}")

        # Cập nhật Donut Chart
        display_books = f"{b_total:,}" if b_total < 10000 else f"{b_total//1000}k"
        self.donut_widget.update_center(display_books, "Bản sách")

        # Cập nhật Progress Bars
        if b_total > 0:
            avail_pct = b_avail / b_total
            borrow_pct = b_borrowed / b_total
        else:
            avail_pct, borrow_pct = 1.0, 0.0

        self.pbar_avail.set_progress(avail_pct, f"{b_avail}/{b_total}")
        self.pbar_borrow.set_progress(borrow_pct, f"{b_borrowed}/{b_total}")
        self.pbar_members.set_progress(min(1.0, m_cnt / 50.0 if m_cnt else 0.1), f"{m_cnt} bạn đọc")

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
