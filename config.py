"""
Cấu hình hệ thống đọc từ .env hoặc biến môi trường
"""
import os

DEFAULT_CONFIG = {
    "db_host": "localhost",
    "db_port": 3306,
    "db_user": "root",
    "db_password": "",
    "db_name": "library_db",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_email": "example@gmail.com",
    "smtp_password": "",
    "fine_per_day": 5000
}

def load_config(env_file=".env"):
    cfg = DEFAULT_CONFIG.copy()
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip().lower(), v.strip().strip("'\"")
                    if k in cfg:
                        if isinstance(cfg[k], int):
                            try: v = int(v)
                            except ValueError: pass
                        cfg[k] = v
    for k in cfg:
        val = os.environ.get(k.upper())
        if val is not None:
            if isinstance(cfg[k], int):
                try: val = int(val)
                except ValueError: pass
            cfg[k] = val
    return cfg
