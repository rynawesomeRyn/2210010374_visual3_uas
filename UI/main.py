import sys
from PyQt6.QtWidgets import QApplication
from menuUtama import menuUtama

if __name__ == "__main__":
    aplikasi =QApplication(sys.argv)
    tampilForm = menuUtama()
    tampilForm.show()
    sys.exit(aplikasi.exec())