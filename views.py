"""
Giao diện các màn hình chức năng (Views)
"""
import threading
from datetime import datetime, date, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from mailer import send_reminder_email


class BooksView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.db = app.db
        self.setup_ui()

    def setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(header, text="Quản Lý Kho Sách", font=ctk.CTkFont(size=22, weight="bold")).pack(side="left")

        search_box = ctk.CTkFrame(header, fg_color="transparent")
        search_box.pack(side="right")
        self.b_search_var = tk.StringVar()
        ctk.CTkEntry(search_box, placeholder_text="Tìm sách, tác giả, thể loại...", textvariable=self.b_search_var, width=280, height=36).pack(side="left", padx=6)
        ctk.CTkButton(search_box, text="Tìm", width=70, height=36, command=self.load_data).pack(side="left", padx=3)
        ctk.CTkButton(search_box, text="Tất cả", width=70, height=36, fg_color="#4A5568", command=lambda: [self.b_search_var.set(""), self.load_data()]).pack(side="left", padx=3)

        tbl_card = ctk.CTkFrame(self, fg_color="#242424", corner_radius=12)
        tbl_card.pack(fill="both", expand=True, pady=(0, 15))

        self.tree = ttk.Treeview(tbl_card, columns=("id", "title", "author", "cat", "total", "avail"), show="headings")
        cols = [("id", "ID", 60), ("title", "Tên Sách", 340), ("author", "Tác Giả", 200), ("cat", "Thể Loại", 140), ("total", "Tổng", 70), ("avail", "Sẵn Có", 70)]
        for c, h, w in cols:
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="center" if c in ("id", "total", "avail") else "w")
        self.tree.pack(fill="both", expand=True, padx=12, pady=12)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        form = ctk.CTkFrame(self, fg_color="#242424", corner_radius=12)
        form.pack(fill="x")

        self.b_id_var, self.b_title_var = tk.StringVar(), tk.StringVar()
        self.b_author_var, self.b_cat_var, self.b_total_var = tk.StringVar(), tk.StringVar(), tk.StringVar(value="1")

        grid_layout = [
            ("Tên sách:", self.b_title_var, 0, 0, 260),
            ("Tác giả:", self.b_author_var, 0, 2, 180),
            ("Thể loại:", self.b_cat_var, 1, 0, 260),
            ("Số lượng:", self.b_total_var, 1, 2, 180),
        ]
        for lbl, var, r, c, w in grid_layout:
            ctk.CTkLabel(form, text=lbl, font=ctk.CTkFont(size=12)).grid(row=r, column=c, padx=12, pady=8, sticky="e")
            ctk.CTkEntry(form, textvariable=var, width=w, height=32).grid(row=r, column=c+1, padx=6, pady=8, sticky="w")

        btn_box = ctk.CTkFrame(form, fg_color="transparent")
        btn_box.grid(row=0, column=4, rowspan=2, padx=20, pady=8)
        ctk.CTkButton(btn_box, text="+ Thêm Mới", width=100, height=32, command=self.add_book).grid(row=0, column=0, padx=4, pady=4)
        ctk.CTkButton(btn_box, text="✏️ Cập Nhật", width=100, height=32, fg_color="#D69E2E", hover_color="#B7791F", command=self.update_book).grid(row=0, column=1, padx=4, pady=4)
        ctk.CTkButton(btn_box, text="🗑 Xóa", width=100, height=32, fg_color="#E53E3E", hover_color="#C53030", command=self.delete_book).grid(row=1, column=0, padx=4, pady=4)
        ctk.CTkButton(btn_box, text="Làm Trắng", width=100, height=32, fg_color="#4A5568", hover_color="#2D3748", command=self.clear_form).grid(row=1, column=1, padx=4, pady=4)

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        kw = f"%{self.b_search_var.get().strip()}%"
        rows = self.db.query("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR category LIKE %s ORDER BY id DESC", (kw, kw, kw))
        for r in rows:
            self.tree.insert("", "end", values=(r["id"], r["title"], r["author"], r["category"], r["total"], r["available"]))

    def on_select(self, _):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel[0])["values"]
        self.b_id_var.set(v[0]); self.b_title_var.set(v[1]); self.b_author_var.set(v[2]); self.b_cat_var.set(v[3]); self.b_total_var.set(v[4])

    def clear_form(self):
        self.b_id_var.set(""); self.b_title_var.set(""); self.b_author_var.set(""); self.b_cat_var.set(""); self.b_total_var.set("1")

    def add_book(self):
        t, a, c = self.b_title_var.get().strip(), self.b_author_var.get().strip(), self.b_cat_var.get().strip()
        try:
            total = int(self.b_total_var.get())
            if not t or total <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên sách và số lượng hợp lệ!"); return
        self.db.execute("INSERT INTO books (title, author, category, total, available) VALUES (%s, %s, %s, %s, %s)", (t, a, c, total, total))
        self.clear_form(); self.load_data(); self.app.refresh_stats()

    def update_book(self):
        b_id = self.b_id_var.get()
        if not b_id:
            messagebox.showwarning("Lỗi", "Hãy chọn sách cần cập nhật!"); return
        t, a, c = self.b_title_var.get().strip(), self.b_author_var.get().strip(), self.b_cat_var.get().strip()
        total = int(self.b_total_var.get())
        old = self.db.query("SELECT total, available FROM books WHERE id=%s", (b_id,))[0]
        new_avail = max(0, old["available"] + (total - old["total"]))
        self.db.execute("UPDATE books SET title=%s, author=%s, category=%s, total=%s, available=%s WHERE id=%s", (t, a, c, total, new_avail, b_id))
        self.clear_form(); self.load_data()

    def delete_book(self):
        b_id = self.b_id_var.get()
        if not b_id or not messagebox.askyesno("Xác nhận", "Xóa sách này khỏi kho?"): return
        self.db.execute("DELETE FROM books WHERE id=%s", (b_id,))
        self.clear_form(); self.load_data(); self.app.refresh_stats()


class MembersView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.db = app.db
        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self, text="Quản Lý Độc Giả", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", pady=(0, 15))

        top = ctk.CTkFrame(self, fg_color="#242424", corner_radius=12)
        top.pack(fill="x", pady=(0, 15))

        self.m_name_var, self.m_email_var, self.m_phone_var = tk.StringVar(), tk.StringVar(), tk.StringVar()
        for i, (l, v, w) in enumerate([("Họ tên:", self.m_name_var, 220), ("Email:", self.m_email_var, 240), ("Số ĐT:", self.m_phone_var, 160)]):
            ctk.CTkLabel(top, text=l).grid(row=0, column=i*2, padx=8, pady=12, sticky="e")
            ctk.CTkEntry(top, textvariable=v, width=w, height=34).grid(row=0, column=i*2+1, padx=6, pady=12)

        ctk.CTkButton(top, text="+ Thêm", width=80, height=34, command=self.add_member).grid(row=0, column=6, padx=8)
        ctk.CTkButton(top, text="Xóa", width=80, height=34, fg_color="#E53E3E", command=self.delete_member).grid(row=0, column=7, padx=8)

        tbl_card = ctk.CTkFrame(self, fg_color="#242424", corner_radius=12)
        tbl_card.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tbl_card, columns=("id", "name", "email", "phone", "active"), show="headings")
        for c, h, w in [("id", "Mã", 60), ("name", "Tên Độc Giả", 240), ("email", "Email", 280), ("phone", "Điện Thoại", 160), ("active", "Đang Mượn", 110)]:
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="center" if c in ("id", "active") else "w")
        self.tree.pack(fill="both", expand=True, padx=12, pady=12)

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        members = self.db.query("SELECT * FROM members ORDER BY id DESC")
        for m in members:
            active = self.db.query("SELECT COUNT(*) as cnt FROM borrows WHERE member_id=%s AND status='borrowed'", (m["id"],))[0]["cnt"]
            self.tree.insert("", "end", values=(m["id"], m["name"], m["email"], m["phone"], active))

    def add_member(self):
        name, email, phone = self.m_name_var.get().strip(), self.m_email_var.get().strip(), self.m_phone_var.get().strip()
        if not name or "@" not in email:
            messagebox.showwarning("Lỗi", "Vui lòng nhập họ tên và email hợp lệ!"); return
        self.db.execute("INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        self.m_name_var.set(""); self.m_email_var.set(""); self.m_phone_var.set("")
        self.load_data(); self.app.refresh_stats()

    def delete_member(self):
        sel = self.tree.selection()
        if not sel or not messagebox.askyesno("Xác nhận", "Xóa độc giả này?"): return
        m_id = self.tree.item(sel[0])["values"][0]
        self.db.execute("DELETE FROM members WHERE id=%s", (m_id,))
        self.load_data(); self.app.refresh_stats()


class BorrowsView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.db = app.db
        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self, text="Giao Dịch Mượn & Trả", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", pady=(0, 15))

        top = ctk.CTkFrame(self, fg_color="#242424", corner_radius=12)
        top.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(top, text="Mã Độc Giả:").grid(row=0, column=0, padx=8, pady=12)
        self.borrow_mem_id = ctk.CTkEntry(top, width=90, height=34)
        self.borrow_mem_id.grid(row=0, column=1, padx=6, pady=12)

        ctk.CTkLabel(top, text="Mã Sách:").grid(row=0, column=2, padx=8, pady=12)
        self.borrow_book_id = ctk.CTkEntry(top, width=90, height=34)
        self.borrow_book_id.grid(row=0, column=3, padx=6, pady=12)

        ctk.CTkLabel(top, text="Thời hạn:").grid(row=0, column=4, padx=8, pady=12)
        self.borrow_days = ctk.CTkComboBox(top, values=["7 ngày", "14 ngày", "30 ngày"], width=110, height=34)
        self.borrow_days.set("14 ngày")
        self.borrow_days.grid(row=0, column=5, padx=6, pady=12)

        ctk.CTkButton(top, text="📖 Xác Nhận Mượn", command=self.do_borrow, height=34).grid(row=0, column=6, padx=12)
        ctk.CTkButton(top, text="✅ Trả Sách Đã Chọn", command=self.do_return, height=34, fg_color="#38A169", hover_color="#2F855A").grid(row=0, column=7, padx=6)

        tbl_card = ctk.CTkFrame(self, fg_color="#242424", corner_radius=12)
        tbl_card.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tbl_card, columns=("id", "member", "book", "borrow_date", "due_date", "return_date", "status", "fine"), show="headings")
        cols = [("id", "Mã", 50), ("member", "Độc Giả", 180), ("book", "Tên Sách", 240), ("borrow_date", "Ngày Mượn", 100), ("due_date", "Hạn Trả", 100), ("return_date", "Ngày Trả", 100), ("status", "Trạng Thái", 110), ("fine", "Tiền Phạt", 90)]
        for c, h, w in cols:
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="center" if c in ("id", "borrow_date", "due_date", "return_date", "status", "fine") else "w")
        self.tree.pack(fill="both", expand=True, padx=12, pady=12)

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        rows = self.db.query("""
            SELECT b.id, m.name as member_name, bk.title as book_title, b.borrow_date, b.due_date, b.return_date, b.status, b.fine_amount
            FROM borrows b JOIN members m ON b.member_id = m.id JOIN books bk ON b.book_id = bk.id
            ORDER BY b.id DESC
        """)
        today = date.today().strftime("%Y-%m-%d")
        for r in rows:
            st = "Quá hạn ⚠️" if r["status"] == "borrowed" and r["due_date"] < today else ("Đang mượn" if r["status"] == "borrowed" else "Đã trả")
            self.tree.insert("", "end", values=(r["id"], r["member_name"], r["book_title"], r["borrow_date"], r["due_date"], r["return_date"] or "-", st, f"{r['fine_amount']:,}đ"))

    def do_borrow(self):
        try:
            m_id = int(self.borrow_mem_id.get())
            b_id = int(self.borrow_book_id.get())
            days = int(self.borrow_days.get().split()[0])
        except ValueError:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đúng ID độc giả và ID sách!"); return
        book = self.db.query("SELECT * FROM books WHERE id=%s", (b_id,))
        if not book or book[0]["available"] <= 0:
            messagebox.showerror("Hết sách", "Sách này hiện đã được mượn hết!"); return
        b_date = date.today()
        d_date = b_date + timedelta(days=days)
        self.db.execute("INSERT INTO borrows (book_id, member_id, borrow_date, due_date, status) VALUES (%s, %s, %s, %s, 'borrowed')",
                        (b_id, m_id, b_date.strftime("%Y-%m-%d"), d_date.strftime("%Y-%m-%d")))
        self.db.execute("UPDATE books SET available = available - 1 WHERE id=%s", (b_id,))
        messagebox.showinfo("Thành công", f"Đã ghi nhận mượn sách. Hạn trả: {d_date.strftime('%Y-%m-%d')}")
        self.load_data(); self.app.views["books"].load_data(); self.app.refresh_stats()

    def do_return(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("Chọn mục", "Vui lòng chọn giao dịch cần trả!"); return
        b_id = self.tree.item(sel[0])["values"][0]
        borrow = self.db.query("SELECT * FROM borrows WHERE id=%s", (b_id,))[0]
        if borrow["status"] == "returned":
            messagebox.showinfo("Thông báo", "Sách này đã được trả!"); return
        ret_date = date.today()
        due_date = datetime.strptime(borrow["due_date"], "%Y-%m-%d").date()
        overdue_days = max(0, (ret_date - due_date).days)
        fine = overdue_days * self.app.cfg.get("fine_per_day", 5000)

        self.db.execute("UPDATE borrows SET return_date=%s, fine_amount=%s, status='returned' WHERE id=%s",
                        (ret_date.strftime("%Y-%m-%d"), fine, b_id))
        self.db.execute("UPDATE books SET available = available + 1 WHERE id=%s", (borrow["book_id"],))
        msg = f"Đã trả sách ngày {ret_date.strftime('%Y-%m-%d')}."
        if fine > 0: msg += f"\nQuá hạn {overdue_days} ngày. Phí phạt: {fine:,} VND!"
        messagebox.showinfo("Hoàn tất", msg)
        self.load_data(); self.app.views["books"].load_data(); self.app.views["overdue"].load_data(); self.app.refresh_stats()


class OverdueView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.db = app.db
        self.setup_ui()

    def setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(header, text="Cảnh Báo Quá Hạn & Quản Lý Phạt", font=ctk.CTkFont(size=22, weight="bold")).pack(side="left")

        actions = ctk.CTkFrame(header, fg_color="transparent")
        actions.pack(side="right")
        ctk.CTkButton(actions, text="✉️ Gửi Mail Mục Chọn", height=36, command=self.send_single_reminder).pack(side="left", padx=4)
        ctk.CTkButton(actions, text="⚡ Gửi Toàn Bộ Quá Hạn", height=36, fg_color="#D69E2E", hover_color="#B7791F", command=self.send_bulk_reminders).pack(side="left", padx=4)

        self.overdue_banner = ctk.CTkFrame(self, fg_color="#742A2A", corner_radius=10)
        self.overdue_banner.pack(fill="x", pady=(0, 15))
        self.overdue_summary = ctk.CTkLabel(self.overdue_banner, text="...", font=ctk.CTkFont(size=14, weight="bold"), text_color="#FFF5F5")
        self.overdue_summary.pack(padx=15, pady=12)

        tbl_card = ctk.CTkFrame(self, fg_color="#242424", corner_radius=12)
        tbl_card.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tbl_card, columns=("id", "member", "email", "book", "due_date", "days", "fine"), show="headings")
        cols = [("id", "Mã", 50), ("member", "Tên Độc Giả", 180), ("email", "Email", 240), ("book", "Tên Sách", 240), ("due_date", "Hạn Trả", 100), ("days", "Số Ngày Quá Hạn", 120), ("fine", "Tiền Phạt Tạm Tính", 140)]
        for c, h, w in cols:
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="center" if c in ("id", "due_date", "days", "fine") else "w")
        self.tree.pack(fill="both", expand=True, padx=12, pady=12)

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
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

        color = "#742A2A" if len(rows) > 0 else "#276749"
        self.overdue_banner.configure(fg_color=color)
        self.overdue_summary.configure(text=f"⚠️ Phát hiện {len(rows)} lượt mượn quá hạn  |  Tổng tiền phạt ước tính: {total_fine:,} VND" if len(rows) > 0 else "🎉 Không có lượt mượn nào quá hạn!")

    def send_single_reminder(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("Chọn mục", "Vui lòng chọn 1 dòng để gửi email!"); return
        v = self.tree.item(sel[0])["values"]
        def worker():
            ok = send_reminder_email(self.app.cfg, v[2], v[1], v[3], v[4], v[6])
            if ok: messagebox.showinfo("Thành công", f"Đã gửi email nhắc nhở tới {v[2]}!")
            else: messagebox.showerror("Thất bại", f"Không thể gửi email tới {v[2]}. Kiểm tra .env!")
        threading.Thread(target=worker, daemon=True).start()

    def send_bulk_reminders(self):
        today = date.today().strftime("%Y-%m-%d")
        rows = self.db.query("""
            SELECT m.name, m.email, bk.title, b.due_date
            FROM borrows b JOIN members m ON b.member_id = m.id JOIN books bk ON b.book_id = bk.id
            WHERE b.status = 'borrowed' AND b.due_date <= %s
        """, (today,))
        if not rows: messagebox.showinfo("Thông báo", "Không có bạn đọc nào đến hạn hoặc quá hạn hôm nay!"); return
        def bulk_worker():
            success = 0
            for r in rows:
                if send_reminder_email(self.app.cfg, r["email"], r["name"], r["title"], r["due_date"]):
                    success += 1
            messagebox.showinfo("Hoàn tất", f"Đã gửi nhắc nhở email thành công cho {success}/{len(rows)} bạn đọc.")
        threading.Thread(target=bulk_worker, daemon=True).start()


class ReportsView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.db = app.db
        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self, text="Báo Cáo & Phân Tích Thống Kê", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", pady=(0, 15))

        cards_grid = ctk.CTkFrame(self, fg_color="transparent")
        cards_grid.pack(fill="x", pady=(0, 15))
        cards_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.kpi_widgets = {}
        kpi_defs = [
            ("books", "Tổng Đầu Sách", "📚", "#2B6CB0"),
            ("members", "Tổng Bạn Đọc", "👥", "#319795"),
            ("borrows", "Tổng Lượt Mượn", "🔄", "#805AD5"),
            ("fines", "Tiền Phạt Đã Thu", "💰", "#DD6B20")
        ]
        for idx, (k, title, icon, color) in enumerate(kpi_defs):
            card = ctk.CTkFrame(cards_grid, fg_color="#242424", corner_radius=12)
            card.grid(row=0, column=idx, padx=6, sticky="ew")
            
            top_row = ctk.CTkFrame(card, fg_color="transparent")
            top_row.pack(fill="x", padx=14, pady=(12, 4))
            ctk.CTkLabel(top_row, text=title, font=ctk.CTkFont(size=12), text_color="#A0AEC0").pack(side="left")
            ctk.CTkLabel(top_row, text=icon, font=ctk.CTkFont(size=16)).pack(side="right")

            val_lbl = ctk.CTkLabel(card, text="0", font=ctk.CTkFont(size=22, weight="bold"), text_color=color)
            val_lbl.pack(anchor="w", padx=14, pady=(0, 12))
            self.kpi_widgets[k] = val_lbl

        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        grid_frame.grid_columnconfigure((0, 1), weight=1)
        grid_frame.grid_rowconfigure(0, weight=1)

        c1 = ctk.CTkFrame(grid_frame, fg_color="#242424", corner_radius=12)
        c1.grid(row=0, column=0, padx=6, sticky="nsew")
        ctk.CTkLabel(c1, text="Top Sách Được Mượn Nhiều Nhất", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=12, pady=10)
        self.top_books_tree = ttk.Treeview(c1, columns=("title", "count"), show="headings", height=8)
        self.top_books_tree.heading("title", text="Tên Sách"); self.top_books_tree.heading("count", text="Lượt Mượn")
        self.top_books_tree.column("title", width=280); self.top_books_tree.column("count", width=80, anchor="center")
        self.top_books_tree.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        c2 = ctk.CTkFrame(grid_frame, fg_color="#242424", corner_radius=12)
        c2.grid(row=0, column=1, padx=6, sticky="nsew")
        ctk.CTkLabel(c2, text="Thể Loại Sách Phổ Biến Nhất", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=12, pady=10)
        self.top_cats_tree = ttk.Treeview(c2, columns=("cat", "count"), show="headings", height=8)
        self.top_cats_tree.heading("cat", text="Thể Loại"); self.top_cats_tree.heading("count", text="Tổng Mượn")
        self.top_cats_tree.column("cat", width=220); self.top_cats_tree.column("count", width=80, anchor="center")
        self.top_cats_tree.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def load_data(self):
        b_cnt = self.db.query("SELECT COUNT(*) as c FROM books")[0]["c"]
        m_cnt = self.db.query("SELECT COUNT(*) as c FROM members")[0]["c"]
        br_cnt = self.db.query("SELECT COUNT(*) as c FROM borrows")[0]["c"]
        fine_sum = self.db.query("SELECT SUM(fine_amount) as s FROM borrows")[0]["s"] or 0

        self.kpi_widgets["books"].configure(text=str(b_cnt))
        self.kpi_widgets["members"].configure(text=str(m_cnt))
        self.kpi_widgets["borrows"].configure(text=str(br_cnt))
        self.kpi_widgets["fines"].configure(text=f"{int(fine_sum):,}đ")

        for item in self.top_books_tree.get_children(): self.top_books_tree.delete(item)
        for r in self.db.query("""
            SELECT bk.title, COUNT(b.id) as cnt
            FROM borrows b JOIN books bk ON b.book_id = bk.id
            GROUP BY bk.id, bk.title ORDER BY cnt DESC LIMIT 10
        """):
            self.top_books_tree.insert("", "end", values=(r["title"], r["cnt"]))

        for item in self.top_cats_tree.get_children(): self.top_cats_tree.delete(item)
        for r in self.db.query("""
            SELECT bk.category, COUNT(b.id) as cnt
            FROM borrows b JOIN books bk ON b.book_id = bk.id
            GROUP BY bk.category ORDER BY cnt DESC LIMIT 10
        """):
            self.top_cats_tree.insert("", "end", values=(r["category"], r["cnt"]))
