import sys
import pymysql
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QStringListModel

from koneksiDB import KoneksiDB
from tableModel import TableModel

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class FormKamera(QMainWindow):
    def __init__(self):
        super().__init__()

        # Memuat file .ui
        uic.loadUi("kamera.ui", self)

        # Koneksi ke database
        self.db = KoneksiDB()
        self.connection = self.db.get_connection()
        self.cursor = self.db.get_cursor()

        # Memuat data awal ke tabel
        self.load_data()

        # Menyambungkan fungsi ke tombol
        self.btnSimpan.clicked.connect(self.add_data)
        self.btnUbah.clicked.connect(self.update_data)
        self.btnHapus.clicked.connect(self.delete_data)
        self.tableKamera.clicked.connect(self.on_table_click)
        self.btnCetak.clicked.connect(self.print_pdf)

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM kamera")
        data = self.cursor.fetchall()
        headers = [desc[0] for desc in self.cursor.description]
        return data, headers

    def fetch_allPDF(self):
        self.cursor.execute("SELECT * FROM kamera")
        return self.cursor.fetchall()

    def load_data(self):
        try:
            data, headers = self.fetch_all()
            self.model = TableModel(data, headers)
            self.tableKamera.setModel(self.model)
        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan saat memuat data: {e}")

    def add_data(self):
        id_kamera = self.editIDKamera.text()
        nama_kamera = self.editnmKamera.text()
        lokasi = self.editLokasi.text()
        if id_kamera and nama_kamera and lokasi:
            try:
                self.cursor.execute(
                    "INSERT INTO kamera (id_kamera, nama_kamera, lokasi) VALUES (%s, %s, %s)",(id_kamera, nama_kamera, lokasi),
                )
                self.connection.commit()
                self.clear_inputs()
                self.load_data()
                QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan.")
            except Exception as e:
                QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi.")

    def update_data(self):
        id_kamera = self.editIDKamera.text()
        nama_kamera = self.editnmKamera.text()
        lokasi = self.editLokasi.text()
        if id_kamera and nama_kamera and lokasi:
            try:
                self.cursor.execute(
                    "UPDATE kamera SET nama_kamera = %s, lokasi = %s WHERE id_kamera = %s",(nama_kamera, lokasi, id_kamera),)
                self.connection.commit()
                self.load_data()
                self.clear_inputs()
                QMessageBox.information(self, "Sukses", "Data berhasil diubah.")
            except Exception as e:
                QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi.")

    def delete_data(self):
        id_kamera = self.editIDKamera.text()
        if id_kamera:
            try:
                self.cursor.execute("DELETE FROM kamera WHERE id_kamera = %s", (id_kamera,))
                self.connection.commit()
                self.load_data()
                self.clear_inputs()
                QMessageBox.information(self, "Sukses", "Data berhasil dihapus.")
            except Exception as e:
                QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Kode kategori harus diisi untuk menghapus data.")

    def clear_inputs(self):
        self.editIDKamera.clear()
        self.editnmKamera.clear()
        self.editLokasi.clear()

    def on_table_click(self, index):
        try:
            row = index.row()
            record = self.model._data[row]
            self.editIDKamera.setText(str(record[0]))
            self.editnmKamera.setText(str(record[1]))
            self.editLokasi.setText(str(record[2]))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Terjadi kesalahan: {e}")

    def print_pdf(self):
        try:
            data = self.fetch_allPDF()
            if not data:
                QMessageBox.warning(self, "Data Kosong", "Tidak ada data untuk dicetak.")
                return

            pdf_file = "kamera_report.pdf"
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter

            # Header laporan
            c.drawString(100, height - 50, "Laporan Data Kamera")
            c.drawString(100, height - 100, "ID Kamera")
            c.drawString(200, height - 100, "Nama Kamera")
            c.drawString(300, height - 100, "Lokasi")

            # Isi laporan
            y_position = height - 120
            for row in data:
                c.drawString(100, y_position, str(row[0]))
                c.drawString(200, y_position, row[1])
                c.drawString(300, y_position, row[2])
                y_position -= 20

            c.save()
            QMessageBox.information(self, "Sukses", f"Laporan berhasil dicetak ke {pdf_file}.")
        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan saat mencetak PDF: {e}")

    def closeEvent(self, event):
        self.connection.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormKamera()
    window.show()
    sys.exit(app.exec())
