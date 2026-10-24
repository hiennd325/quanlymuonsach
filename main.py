"""
LibMaster — Entry point ứng dụng Quản Lý Thư Viện (Thuần MySQL)
Thiết kế theo phong cách Obsidian & Neon Purple Glow (Không sử dụng emoji)
"""
import sys
from tkinter import ttk, messagebox
import customtkinter as ctk

from config import load_config
from database import Database
from theme import THEME, RADIUS
from models import BookModel, MemberModel, BorrowModel, ReportModel
from controllers import (
    BookController,
    MemberController,
    BorrowController,
    OverdueController,
    DashboardController,
    ReportController
)
from views import (
    DashboardView,
    BooksView,
    MembersView,
    BorrowsView,
    OverdueView,
    ReportsView
)


class ModernLibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        self.db = Database(self.cfg)

        self.title("LibMaster — Hệ Thống Quản Lý Thư Viện")
        self.geometry("1240x760")
        self.minsize(1020, 660)

        # Cài đặt giao diện sáng (Light Mode Only)
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=THEME["bg_window"])

        self.style_tables()
        self.init_mvc()
        self.setup_layout()

        if self.db.connection_error:
            self.show_db_error_screen()
        else:
            self.show_page("dashboard")
            self.refresh_all()

    def style_tables(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=THEME["tree_bg"],
            foreground=THEME["tree_fg"],
            fieldbackground=THEME["tree_bg"],
            borderwidth=0,
            rowheight=36,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background=THEME["tree_head_bg"],
            foreground=THEME["tree_head_fg"],
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
            padding=8
        )
        style.map(
            "Treeview",
            background=[("selected", THEME["tree_selected_bg"])],
            foreground=[("selected", THEME["tree_selected_fg"])]
        )

    def setup_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 1. Sidebar bên trái (Giao diện Sáng)
        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0,
            fg_color=THEME["bg_sidebar"],
            border_color=THEME["card_border"],
            border_width=1
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)

        # Logo & Brand Header
        logo_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_box.grid(row=0, column=0, padx=20, pady=(28, 24), sticky="w")

        ctk.CTkLabel(
            logo_box,
            text="LibMaster",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=THEME["text_primary"]
        ).pack(anchor="w")

        tag_box = ctk.CTkFrame(logo_box, fg_color=THEME["primary_subtle"], corner_radius=8)
        tag_box.pack(anchor="w", pady=(4, 0))
        ctk.CTkLabel(
            tag_box,
            text="ENTERPRISE",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=THEME["primary_glow"]
        ).pack(padx=8, pady=2)

        # Danh sách các trang điều hướng dạng viên thuốc (Không dùng emoji)
        self.nav_buttons = {}
        pages = [
            ("dashboard", "Tổng Quan"),
            ("books", "Quản Lý Sách"),
            ("members", "Bạn Đọc"),
            ("borrows", "Mượn & Trả Sách"),
            ("overdue", "Cảnh Báo Quá Hạn"),
            ("reports", "Báo Cáo & Thống Kê"),
        ]

        for i, (key, label) in enumerate(pages, start=1):
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                anchor="w",
                font=ctk.CTkFont(size=13, weight="bold"),
                height=44,
                corner_radius=RADIUS["pill"],
                fg_color="transparent",
                hover_color=THEME["card_inner"],
                text_color=THEME["text_secondary"],
                command=lambda k=key: self.show_page(k)
            )
            btn.grid(row=i, column=0, padx=14, pady=4, sticky="ew")
            self.nav_buttons[key] = btn

        # Footer Sidebar (Trạng thái MySQL)
        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer.grid(row=9, column=0, padx=14, pady=20, sticky="ew")

        # Thẻ trạng thái MySQL dạng viên thuốc
        db_card = ctk.CTkFrame(
            footer,
            fg_color=THEME["card_inner"],
            corner_radius=RADIUS["card_sm"],
            border_color=THEME["card_border"],
            border_width=1
        )
        db_card.pack(fill="x")

        if self.db.connection_error:
            db_txt = "MySQL: Ngoại Tuyến"
            db_color = THEME["accent_red"]
        else:
            db_txt = f"MySQL: {self.cfg['db_name']}"
            db_color = THEME["accent_cyan"]

        self.db_badge = ctk.CTkLabel(
            db_card,
            text=db_txt,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=db_color
        )
        self.db_badge.pack(padx=12, pady=8, anchor="w")

        # 2. Vùng chứa nội dung chính (Main Container)
        self.main_container = ctk.CTkFrame(self, fg_color=THEME["bg_main"], corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Màn hình báo lỗi kết nối MySQL
        self.error_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.build_error_screen()

        # Khởi tạo các Views
        self.views = {
            "dashboard": DashboardView(self.main_container, self, self.controllers["dashboard"]),
            "books": BooksView(self.main_container, self, self.controllers["book"]),
            "members": MembersView(self.main_container, self, self.controllers["member"]),
            "borrows": BorrowsView(self.main_container, self, self.controllers["borrow"]),
            "overdue": OverdueView(self.main_container, self, self.controllers["overdue"]),
            "reports": ReportsView(self.main_container, self, self.controllers["report"]),
        }

    def init_mvc(self):
        # 1. Models
        self.models = {
            "book": BookModel(self.db),
            "member": MemberModel(self.db),
            "borrow": BorrowModel(self.db, BookModel(self.db)),
            "report": ReportModel(self.db),
        }
        # 2. Controllers
        self.controllers = {
            "book": BookController(self.models["book"]),
            "member": MemberController(self.models["member"]),
            "borrow": BorrowController(self.models["borrow"], self.models["book"], self.cfg),
            "overdue": OverdueController(self.models["borrow"], self.cfg),
            "dashboard": DashboardController(self.models["book"], self.models["member"], self.models["borrow"]),
            "report": ReportController(self.models["report"]),
        }

    def build_error_screen(self):
        box = ctk.CTkFrame(
            self.error_frame,
            fg_color=THEME["card_bg"],
            corner_radius=RADIUS["card"],
            border_color=THEME["accent_red"],
            border_width=1,
            width=650
        )
        box.place(relx=0.5, rely=0.5, anchor="center")

        err_tag = ctk.CTkFrame(box, fg_color=THEME["accent_red_subtle"], corner_radius=RADIUS["pill"])
        err_tag.pack(pady=(30, 10))
        ctk.CTkLabel(
            err_tag,
            text="CONNECTION FAILED",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=THEME["accent_red"]
        ).pack(padx=16, pady=5)

        ctk.CTkLabel(
            box,
            text="Không Thể Kết Nối Tới MySQL",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=THEME["text_primary"]
        ).pack(pady=(0, 10))

        desc = (
            "Hệ thống yêu cầu máy chủ MySQL đang chạy để hoạt động.\n"
            "Vui lòng kiểm tra lại thông tin cấu hình trong file .env."
        )
        ctk.CTkLabel(
            box,
            text=desc,
            font=ctk.CTkFont(size=13),
            text_color=THEME["text_secondary"],
            justify="center"
        ).pack(padx=30, pady=(0, 15))

        self.err_detail_box = ctk.CTkTextbox(
            box,
            width=540,
            height=100,
            corner_radius=RADIUS["input"],
            fg_color=THEME["input_bg"],
            text_color=THEME["accent_red"]
        )
        self.err_detail_box.pack(padx=20, pady=10)

        ctk.CTkButton(
            box,
            text="Tải Lại Cấu Hình & Kết Nối Lại",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=42,
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            corner_radius=RADIUS["pill"],
            command=self.retry_connection
        ).pack(pady=(15, 30))

    def show_db_error_screen(self):
        for v in self.views.values():
            v.grid_remove()
        for b in self.nav_buttons.values():
            b.configure(state="disabled", fg_color="transparent")

        self.err_detail_box.delete("1.0", "end")
        err_msg = (
            f"Chi tiết lỗi: {self.db.connection_error}\n\n"
            f"Thông tin kết nối hiện tại:\n"
            f"- Host: {self.cfg['db_host']}:{self.cfg['db_port']}\n"
            f"- User: {self.cfg['db_user']}\n"
            f"- Database: {self.cfg['db_name']}"
        )
        self.err_detail_box.insert("1.0", err_msg)
        self.err_detail_box.configure(state="disabled")

        self.db_badge.configure(text="MySQL: Ngoại Tuyến", text_color=THEME["accent_red"])
        self.error_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def retry_connection(self):
        self.cfg = load_config()
        self.db = Database(self.cfg)
        if self.db.connection_error:
            self.err_detail_box.configure(state="normal")
            self.show_db_error_screen()
            messagebox.showerror("Kết nối thất bại", f"Vẫn chưa thể kết nối tới MySQL:\n{self.db.connection_error}")
        else:
            self.error_frame.grid_remove()
            for b in self.nav_buttons.values():
                b.configure(state="normal")
            self.db_badge.configure(text=f"MySQL: {self.cfg['db_name']}", text_color=THEME["accent_cyan"])
            self.init_mvc()
            if "dashboard" in self.views:
                self.views["dashboard"].controller = self.controllers["dashboard"]
            if "books" in self.views:
                self.views["books"].controller = self.controllers["book"]
            if "members" in self.views:
                self.views["members"].controller = self.controllers["member"]
            if "borrows" in self.views:
                self.views["borrows"].controller = self.controllers["borrow"]
            if "overdue" in self.views:
                self.views["overdue"].controller = self.controllers["overdue"]
            if "reports" in self.views:
                self.views["reports"].controller = self.controllers["report"]
            messagebox.showinfo("Thành công", "Đã kết nối thành công tới MySQL.")
            self.show_page("dashboard")
            self.refresh_all()

    def show_page(self, name):
        if self.db.connection_error:
            return

        for k, v in self.views.items():
            v.grid_remove()
            if k in self.nav_buttons:
                self.nav_buttons[k].configure(
                    fg_color="transparent",
                    text_color=THEME["text_secondary"]
                )

        if name in self.views:
            self.views[name].grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            if name in self.nav_buttons:
                self.nav_buttons[name].configure(
                    fg_color=THEME["primary"],
                    text_color=THEME["text_white"]
                )
            self.views[name].load_data()

    def refresh_stats(self):
        if not self.db.connection_error:
            if "dashboard" in self.views:
                self.views["dashboard"].load_data()
            if "reports" in self.views:
                self.views["reports"].load_data()

    def refresh_all(self):
        if not self.db.connection_error:
            for v in self.views.values():
                v.load_data()


def self_test():
    cfg = load_config()
    db = Database(cfg)
    if db.connection_error:
        print(f"Self-test: MySQL connection error caught cleanly -> {db.connection_error}")
    else:
        print("Self-test: Connected to MySQL successfully.")


if __name__ == "__main__":
    if "--test" in sys.argv:
        self_test()
    else:
        app = ModernLibraryApp()
        app.mainloop()
