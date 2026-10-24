"""
Custom Canvas Widgets lấy cảm hứng trực tiếp từ ảnh mẫu:
1. WavyChartWidget: Đồ thị dạng sóng cong màu tím neon, có vùng phủ gradient mờ, nhãn tháng và huy hiệu thống kê nổi bật.
2. DonutChartWidget: Biểu đồ vành khăn (Donut Ring) 3 màu phân đoạn (Tím, Cam, Xanh) với nhãn số ở tâm (VD: '6k').
3. PillProgressBar: Thanh tiến trình bo tròn mềm mại dạng viên thuốc (giống Food, Savings, Rent).
4. MiniBarWidget: Cột sóng mini màu tím bo góc tròn (giống widget Transaction).
"""
import tkinter as tk
import customtkinter as ctk
from theme import THEME, RADIUS


class WavyChartWidget(ctk.CTkFrame):
    """
    Card hiển thị đồ thị đường cong màu tím sóng lượn giống ảnh mẫu:
    - Đường neon tím (#9B70FF) uốn lượn
    - Vùng gradient đổ bóng tím bên dưới
    - Điểm sáng (glow dot) tại tháng gần nhất
    - Badge 'Hôm nay / Tháng này' kèm chỉ số tăng trưởng '+5.3% ↗'
    """
    def __init__(self, parent, title="Xu Hướng Hoạt Động Thư Viện", **kwargs):
        super().__init__(
            parent,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1,
            **kwargs
        )
        self.months = ["Jan", "Feb", "Mar", "Apr", "May"]
        self.values = [35, 68, 48, 92, 75]  # Tỷ lệ chiều cao đồ thị

        # Header card
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(16, 6))

        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=THEME["text_primary"]
        ).pack(side="left")

        # Canvas vẽ sóng
        self.canvas_h = 130
        self.canvas = tk.Canvas(
            self,
            height=self.canvas_h,
            bg=THEME["card_bg"],
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill="x", padx=12, pady=(0, 4))
        self.canvas.bind("<Configure>", self._on_resize)

        # Floating badge thống kê bên dưới đồ thị (như thẻ Today $62,970 trong ảnh)
        self.stat_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_inner"],
            corner_radius=RADIUS["card_sm"],
            border_color=THEME["card_border"],
            border_width=1
        )
        self.stat_card.pack(fill="x", padx=16, pady=(4, 16))

        info_box = ctk.CTkFrame(self.stat_card, fg_color="transparent")
        info_box.pack(side="left", padx=14, pady=10)

        ctk.CTkLabel(
            info_box,
            text="Hôm nay / Tuần này",
            font=ctk.CTkFont(size=11),
            text_color=THEME["text_muted"]
        ).pack(anchor="w")

        self.stat_val_lbl = ctk.CTkLabel(
            info_box,
            text="62,970",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=THEME["text_primary"]
        )
        self.stat_val_lbl.pack(anchor="w")

        # Badge tăng trưởng màu tím
        badge_box = ctk.CTkFrame(self.stat_card, fg_color="transparent")
        badge_box.pack(side="right", padx=14, pady=10)

        self.trend_pill = ctk.CTkFrame(
            badge_box,
            fg_color=THEME["primary_subtle"],
            corner_radius=12
        )
        self.trend_pill.pack()

        self.trend_lbl = ctk.CTkLabel(
            self.trend_pill,
            text="+5.3%  ↑",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=THEME["primary_glow"]
        )
        self.trend_lbl.pack(padx=10, pady=4)

    def set_data(self, stat_label="Lượt tương tác", stat_val="1,420", trend="+12.4%  ↑"):
        self.stat_val_lbl.configure(text=stat_val)
        self.trend_lbl.configure(text=trend)

    def _on_resize(self, event):
        self.draw_wave(event.width, event.height)

    def draw_wave(self, w, h):
        self.canvas.delete("all")
        if w < 50:
            return

        pad_x = 24
        pad_top = 20
        pad_bottom = 30
        usable_w = w - pad_x * 2
        usable_h = h - pad_top - pad_bottom

        n = len(self.values)
        step_x = usable_w / (n - 1)

        pts = []
        for i, val in enumerate(self.values):
            x = pad_x + i * step_x
            y = pad_top + usable_h - (val / 100.0 * usable_h)
            pts.extend([x, y])

        # 1. Vẽ vùng gradient / polygon đổ bóng tím bên dưới (nền sáng)
        poly_pts = [pts[0], h - pad_bottom] + pts + [pts[-2], h - pad_bottom]
        self.canvas.create_polygon(poly_pts, fill="#F3EEFF", outline="", smooth=True)

        # 2. Vẽ đường sóng tím chính
        self.canvas.create_line(pts, fill=THEME["primary"], width=3, smooth=True)

        # 3. Điểm nhấn tại tháng mới nhất (tháng cuối cùng)
        last_x, last_y = pts[-2], pts[-1]
        self.canvas.create_oval(
            last_x - 7, last_y - 7, last_x + 7, last_y + 7,
            fill="#DDD6FE", outline=""
        )
        self.canvas.create_oval(
            last_x - 3.5, last_y - 3.5, last_x + 3.5, last_y + 3.5,
            fill=THEME["primary"], outline=""
        )

        # 4. Nhãn tháng phía dưới
        for i, m in enumerate(self.months):
            x = pad_x + i * step_x
            color = THEME["text_primary"] if i == n - 1 else THEME["text_muted"]
            font_spec = ("Segoe UI", 9, "bold") if i == n - 1 else ("Segoe UI", 9)
            self.canvas.create_text(x, h - 12, text=m, fill=color, font=font_spec)


class DonutChartWidget(ctk.CTkFrame):
    """
    Card biểu đồ vành khăn (Donut Ring) 3 màu + số lượng ở tâm giống ảnh mẫu.
    """
    def __init__(self, parent, title="Phân Bổ Thư Viện", center_text="6k", center_sub="Tổng sách", **kwargs):
        super().__init__(
            parent,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1,
            **kwargs
        )
        self.center_text = center_text
        self.center_sub = center_sub

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(16, 6))

        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=THEME["text_primary"]
        ).pack(side="left")

        # Container biểu đồ
        self.canvas_size = 140
        self.canvas = tk.Canvas(
            self,
            width=self.canvas_size,
            height=self.canvas_size,
            bg=THEME["card_bg"],
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(pady=10)
        self.draw_donut()

    def update_center(self, main_txt, sub_txt="Tổng sách"):
        self.center_text = main_txt
        self.center_sub = sub_txt
        self.draw_donut()

    def draw_donut(self):
        self.canvas.delete("all")
        cx = self.canvas_size / 2
        cy = self.canvas_size / 2
        r_out = 60
        r_in = 42

        # 3 phân đoạn màu: Tím (190°), Cam (90°), Xanh ngọc (80°)
        self.canvas.create_arc(
            cx - r_out, cy - r_out, cx + r_out, cy + r_out,
            start=30, extent=200, outline="", fill=THEME["primary"]
        )
        self.canvas.create_arc(
            cx - r_out, cy - r_out, cx + r_out, cy + r_out,
            start=230, extent=75, outline="", fill=THEME["accent_orange"]
        )
        self.canvas.create_arc(
            cx - r_out, cy - r_out, cx + r_out, cy + r_out,
            start=305, extent=85, outline="", fill=THEME["accent_cyan"]
        )

        # Lỗ khoét ở giữa
        self.canvas.create_oval(
            cx - r_in, cy - r_in, cx + r_in, cy + r_in,
            fill=THEME["card_bg"], outline=""
        )

        # Chữ ở tâm (giống 6k)
        self.canvas.create_text(
            cx, cy - 6,
            text=self.center_text,
            fill=THEME["text_primary"],
            font=("Segoe UI", 16, "bold")
        )
        self.canvas.create_text(
            cx, cy + 14,
            text=self.center_sub,
            fill=THEME["text_muted"],
            font=("Segoe UI", 8)
        )


class PillProgressBar(ctk.CTkFrame):
    """
    Thanh tiến trình bo tròn mềm mại giống các thanh Food, Savings, Rent trong ảnh mẫu.
    """
    def __init__(self, parent, label="Mục", percent=0.7, color=THEME["primary"], **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.color = color
        self.percent = max(0.0, min(1.0, percent))

        top_row = ctk.CTkFrame(self, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 4))

        self.lbl = ctk.CTkLabel(
            top_row,
            text=label,
            font=ctk.CTkFont(size=11),
            text_color=THEME["text_secondary"]
        )
        self.lbl.pack(side="left")

        self.val_lbl = ctk.CTkLabel(
            top_row,
            text=f"{int(self.percent * 100)}%",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=color
        )
        self.val_lbl.pack(side="right")

        # Track nền
        self.bar_bg = ctk.CTkFrame(
            self,
            height=10,
            fg_color=THEME["card_inner"],
            corner_radius=5
        )
        self.bar_bg.pack(fill="x")

        # Thanh màu lấp đầy
        self.fill_bar = ctk.CTkFrame(
            self.bar_bg,
            height=10,
            fg_color=color,
            corner_radius=5
        )
        self.fill_bar.place(relx=0, rely=0, relwidth=self.percent, relheight=1.0)

    def set_progress(self, percent, text_info=None):
        self.percent = max(0.0, min(1.0, percent))
        self.fill_bar.place_configure(relwidth=self.percent)
        if text_info:
            self.val_lbl.configure(text=text_info)
        else:
            self.val_lbl.configure(text=f"{int(self.percent * 100)}%")


class MiniBarWidget(ctk.CTkFrame):
    """
    Widget mini bar chart màu tím bo tròn dạng viên thuốc kèm nút Transaction.
    """
    def __init__(self, parent, title="Giao Dịch Gần Đây", on_click=None, **kwargs):
        super().__init__(
            parent,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["card_border"],
            border_width=1,
            **kwargs
        )
        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=12)

        # Canvas vẽ 5 cột tím bo tròn
        self.canvas = tk.Canvas(
            inner,
            width=90,
            height=40,
            bg=THEME["card_bg"],
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(side="left")
        self.draw_bars()

        # Nút Transaction dạng viên thuốc
        ctk.CTkButton(
            inner,
            text=title,
            command=on_click,
            height=32,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=THEME["card_inner"],
            hover_color=THEME["btn_secondary_hover"],
            text_color=THEME["text_secondary"],
            corner_radius=RADIUS["pill"]
        ).pack(side="right", padx=(8, 0))

    def draw_bars(self):
        bars = [0.45, 0.7, 0.9, 0.6, 0.85]
        bar_w = 8
        spacing = 7
        for i, val in enumerate(bars):
            x = 8 + i * (bar_w + spacing)
            h = 36 * val
            y = 38 - h
            # Vẽ thanh bo tròn
            self.canvas.create_rectangle(
                x, y, x + bar_w, 38,
                fill=THEME["primary"],
                outline=""
            )
