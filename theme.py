"""
Theme & Styling System
Lấy cảm hứng từ phong cách Dark Obsidian & Neon Violet / Purple Glow trong ảnh mẫu:
- Nền đen than chì / xanh đen sâu thẳm (#0F121E, #0B0E17)
- Các thẻ khối card bo tròn mềm mại (#161B28, border #22293C, radius 18)
- Nút bấm dạng viên thuốc (Pill shape, radius 20) với màu tím neon (#7857FF)
- Điểm nhấn phụ: Xanh ngọc (#00D2B4), Cam vàng (#FFA940), Đỏ san hô (#FF5C75)
- Ô nhập liệu chìm tối (#111522, border #262F43)
- Bảng dữ liệu hiện đại, hàng cao thoáng, viền phẳng
"""

THEME = {
    # Nền ứng dụng & Cấu trúc
    "bg_window": "#0F121E",
    "bg_sidebar": "#0B0E17",
    "bg_main": "#0F121E",
    "card_bg": "#161B28",
    "card_border": "#22293C",
    "card_inner": "#111522",
    
    # Ô nhập liệu (Input & Search)
    "input_bg": "#111522",
    "input_border": "#262F43",
    "input_focus": "#7857FF",
    
    # Màu tím chủ đạo (Primary Purple / Violet)
    "primary": "#7857FF",
    "primary_hover": "#8C6EFF",
    "primary_pressed": "#6545EB",
    "primary_subtle": "#252044",
    "primary_glow": "#9B70FF",
    
    # Màu phụ trợ (Secondary Accents)
    "accent_cyan": "#00D2B4",
    "accent_cyan_hover": "#05E6C6",
    "accent_cyan_subtle": "#142F30",
    
    "accent_orange": "#FFA940",
    "accent_orange_hover": "#FFB85C",
    "accent_orange_subtle": "#332616",
    
    "accent_red": "#FF5C75",
    "accent_red_hover": "#FF758B",
    "accent_red_subtle": "#361922",
    
    # Nút thứ cấp & Nút tối
    "btn_secondary": "#1E2536",
    "btn_secondary_hover": "#283147",
    "btn_secondary_text": "#CBD5E1",
    
    # Văn bản (Typography)
    "text_white": "#FFFFFF",
    "text_primary": "#E2E8F0",
    "text_secondary": "#A0AEC0",
    "text_muted": "#718096",
    "text_dim": "#4A5568",
    
    # Bảng (Treeview)
    "tree_bg": "#161B28",
    "tree_alt_bg": "#131722",
    "tree_fg": "#E2E8F0",
    "tree_head_bg": "#0E121B",
    "tree_head_fg": "#8E9AA8",
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
