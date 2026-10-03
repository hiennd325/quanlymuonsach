"""
LibMaster — Entry point ứng dụng Quản Lý Thư Viện (Thuần MySQL)
"""
import sys
from tkinter import ttk, messagebox
import customtkinter as ctk

from config import load_config
from database import Database
from views import BooksView, MembersView, BorrowsView, OverdueView, ReportsView


class ModernLibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        self.db = Database(self.cfg)

        self.title("LibMaster — Hệ Thống Quản Lý Thư Viện (MySQL)")
        self.geometry("1180x720")
        self.minsize(980, 620)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.style_tables()
        self.setup_layout()

        if self.db.connection_error:
            self.show_db_error_screen()
        else:
            self.show_page("books")
            self.refresh_all()

    def style_tables(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#242424",
                        foreground="#EAEAEA",
                        fieldbackground="#242424",
                        borderwidth=0,
                        rowheight=30,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background="#1A365D",
                        foreground="#FFFFFF",
                        relief="flat",
                        font=("Segoe UI", 10, "bold"),
                        padding=6)
        style.map("Treeview",
                  background=[("selected", "#2B6CB0")],
                  foreground=[("selected", "#FFFFFF")])

    def setup_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=230, corner_radius=0, fg_color="#18191A")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)

        logo_label = ctk.CTkLabel(self.sidebar, text="📚 LibMaster", font=ctk.CTkFont(size=22, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(25, 20), sticky="w")

        self.nav_buttons = {}
        pages = [
            ("books", "📖  Quản Lý Sách"),
            ("members", "👥  Bạn Đọc"),
            ("borrows", "🔄  Mượn & Trả Sách"),
            ("overdue", "⚠️  Cảnh Báo Quá Hạn"),
            ("reports", "📊  Báo Cáo & Thống Kê"),
        ]

        for i, (key, label) in enumerate(pages, start=1):
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                anchor="w",
                font=ctk.CTkFont(size=14),
                height=42,
                corner_radius=8,
                fg_color="transparent",
                hover_color="#2A2B2D",
                command=lambda k=key: self.show_page(k)
            )
            btn.grid(row=i, column=0, padx=12, pady=4, sticky="ew")
            self.nav_buttons[key] = btn

        # Footer
        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer.grid(row=8, column=0, padx=12, pady=15, sticky="ew")

        if self.db.connection_error:
            db_txt = "● Lỗi MySQL"
            db_color = "#E53E3E"
        else:
            db_txt = f"● MySQL: {self.cfg['db_name']}"
            db_color = "#48BB78"

        self.db_badge = ctk.CTkLabel(footer, text=db_txt, font=ctk.CTkFont(size=12, weight="bold"), text_color=db_color)
        self.db_badge.pack(anchor="w", pady=(0, 8))

        theme_switch = ctk.CTkOptionMenu(footer, values=["Dark", "Light", "System"], command=ctk.set_appearance_mode, height=28)
        theme_switch.pack(fill="x")

        # Main Container
        self.main_container = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Màn hình báo lỗi kết nối MySQL
        self.error_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.build_error_screen()

        # Các views chính
        self.views = {
            "books": BooksView(self.main_container, self),
            "members": MembersView(self.main_container, self),
            "borrows": BorrowsView(self.main_container, self),
            "overdue": OverdueView(self.main_container, self),
            "reports": ReportsView(self.main_container, self),
        }

    def build_error_screen(self):
        box = ctk.CTkFrame(self.error_frame, fg_color="#242424", corner_radius=16, width=650)
        box.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(box, text="❌", font=ctk.CTkFont(size=56)).pack(pady=(30, 10))
        ctk.CTkLabel(box, text="Không Thể Kết Nối Tới MySQL", font=ctk.CTkFont(size=22, weight="bold"), text_color="#E53E3E").pack(pady=(0, 10))

        desc = (
            "Hệ thống đã tắt SQLite hoàn toàn và chỉ chấp nhận kết nối MySQL.\n"
            "Vui lòng kiểm tra lại thông tin máy chủ và tài khoản trong file .env."
        )
        ctk.CTkLabel(box, text=desc, font=ctk.CTkFont(size=13), text_color="#A0AEC0", justify="center").pack(padx=30, pady=(0, 15))

        # Chi tiết lỗi
        self.err_detail_box = ctk.CTkTextbox(box, width=540, height=100, corner_radius=8, fg_color="#18191A", text_color="#FC8181")
        self.err_detail_box.pack(padx=20, pady=10)

        # Button kết nối lại
        ctk.CTkButton(
            box,
            text="🔄 Tải Lại Cấu Hình & Thử Kết Nối Lại",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=self.retry_connection
        ).pack(pady=(15, 30))

    def show_db_error_screen(self):
        for v in self.views.values():
            v.grid_remove()
        for b in self.nav_buttons.values():
            b.configure(state="disabled", fg_color="transparent")

        self.err_detail_box.delete("1.0", "end")
        err_msg = (
            f"Lỗi: {self.db.connection_error}\n\n"
            f"Thông tin kết nối hiện tại:\n"
            f"• Host: {self.cfg['db_host']}:{self.cfg['db_port']}\n"
            f"• User: {self.cfg['db_user']}\n"
            f"• Database: {self.cfg['db_name']}"
        )
        self.err_detail_box.insert("1.0", err_msg)
        self.err_detail_box.configure(state="disabled")

        self.db_badge.configure(text="● Lỗi MySQL", text_color="#E53E3E")
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
            self.db_badge.configure(text=f"● MySQL: {self.cfg['db_name']}", text_color="#48BB78")
            # Cập nhật db instance cho các views
            for v in self.views.values():
                v.db = self.db
            messagebox.showinfo("Thành công", "Đã kết nối thành công tới MySQL!")
            self.show_page("books")
            self.refresh_all()

    def show_page(self, name):
        if self.db.connection_error:
            return
        for k, v in self.views.items():
            v.grid_remove()
            self.nav_buttons[k].configure(fg_color="transparent")
        self.views[name].grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.nav_buttons[name].configure(fg_color="#2B6CB0")
        self.views[name].load_data()

    def refresh_stats(self):
        if not self.db.connection_error and "reports" in self.views:
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
