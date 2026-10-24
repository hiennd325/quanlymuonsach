"""
Theme & Styling System — Giao diện Sáng (Light Theme Only)
Phong cách hiện đại, tinh giản và thanh lịch:
- Nền sáng trang nhã (#F8FAFC, #FFFFFF)
- Các thẻ card bo tròn mềm mại (#FFFFFF, border #E2E8F0, radius 18)
- Nút bấm dạng viên thuốc (Pill shape, radius 20) với màu tím chủ đạo (#7857FF)
- Điểm nhấn phụ: Xanh ngọc (#0D9488), Cam (#EA580C), Đỏ (#E11D48)
- Ô nhập liệu nền sáng (#FFFFFF, border #CBD5E1)
- Bảng dữ liệu hiện đại, tương phản sắc nét
"""

THEME = {
    # Nền ứng dụng & Cấu trúc (Giao diện Sáng)
    "bg_window": "#F8FAFC",
    "bg_sidebar": "#FFFFFF",
    "bg_main": "#F8FAFC",
    "card_bg": "#FFFFFF",
    "card_border": "#E2E8F0",
    "card_inner": "#F1F5F9",

    # Ô nhập liệu (Input & Search)
    "input_bg": "#FFFFFF",
    "input_border": "#CBD5E1",
    "input_focus": "#7857FF",

    # Màu tím chủ đạo (Primary Purple / Violet)
    "primary": "#7857FF",
    "primary_hover": "#6C4AEB",
    "primary_pressed": "#5A39D6",
    "primary_subtle": "#EDE9FE",
    "primary_glow": "#6D28D9",

    # Màu phụ trợ (Secondary Accents)
    "accent_cyan": "#0D9488",
    "accent_cyan_hover": "#0F766E",
    "accent_cyan_subtle": "#CCFBF1",

    "accent_orange": "#EA580C",
    "accent_orange_hover": "#C2410C",
    "accent_orange_subtle": "#FFEDD5",

    "accent_red": "#E11D48",
    "accent_red_hover": "#BE123C",
    "accent_red_subtle": "#FFE4E6",

    # Nút thứ cấp & Nút phụ
    "btn_secondary": "#F1F5F9",
    "btn_secondary_hover": "#E2E8F0",
    "btn_secondary_text": "#334155",

    # Văn bản (Typography)
    "text_white": "#FFFFFF",
    "text_primary": "#0F172A",
    "text_secondary": "#475569",
    "text_muted": "#94A3B8",
    "text_dim": "#CBD5E1",

    # Bảng (Treeview)
    "tree_bg": "#FFFFFF",
    "tree_alt_bg": "#F8FAFC",
    "tree_fg": "#0F172A",
    "tree_head_bg": "#F1F5F9",
    "tree_head_fg": "#475569",
    "tree_selected_bg": "#7857FF",
    "tree_selected_fg": "#FFFFFF",
}

RADIUS = {
    "card": 18,
    "card_sm": 12,
    "pill": 20,
    "button": 18,
    "input": 12,
}
