"""
Wrapper tương thích ngược chạy file main.py
"""
from main import ModernLibraryApp, self_test
import sys

if __name__ == "__main__":
    if "--test" in sys.argv:
        self_test()
    else:
        app = ModernLibraryApp()
        app.mainloop()
