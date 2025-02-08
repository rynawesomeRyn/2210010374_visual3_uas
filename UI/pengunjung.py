import sys
from datetime import date

import pymysql
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QStringListModel, QDate

from koneksiDB import KoneksiDB
from tableModel import TableModel

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class FormPengunjung(QMainWindow):
    def __init__(self):
        super().__init__()

        # Memuat file .ui
        uic.loadUi("pengunjung.ui", self)

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
        self.tablePengunjung.clicked.connect(self.on_table_click)
        self.btnCetak.clicked.connect(self.print_pdf)

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM pengunjung_masjid")
        data = self.cursor.fetchall()
        headers = [desc[0] for desc in self.cursor.description]
        return data, headers

    def fetch_allPDF(self):
        try:
            self.cursor.execute("SELECT *FROM pengunjung_masjid")
            results = self.cursor.fetchall()
            print("Results fetched:", results)  # Tambahkan ini untuk debugging
            return results
        except pymysql.connector.Error as err:
            print(f"Kesalahan saat mengambil data: {err}")
            return []

    def load_data(self):
        try:
            data, headers = self.fetch_all()
            self.model = TableModel(data, headers)
            self.tablePengunjung.setModel(self.model)
        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan saat memuat data: {e}")

    def add_data(self):
        id_pengunjung = self.editIDPengunjung.text()
        nama_pengunjung = self.editnmPengunjung.text()
        jenis_kelamin = self.cbJK.currentText()
        tanggal_kunjungan = self.dateTglKunjungan.date().toString("yyyy-MM-dd")
        if id_pengunjung and nama_pengunjung and jenis_kelamin and tanggal_kunjungan:
            try:
                self.cursor.execute("INSERT INTO pengunjung_masjid (id_pengunjung, nama_pengunjung, jenis_kelamin, tanggal_kunjungan) VALUES (%s, %s, %s, %s)",(id_pengunjung, nama_pengunjung, jenis_kelamin, tanggal_kunjungan),)
                self.connection.commit()
                self.clear_inputs()
                self.load_data()
                QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan.")
            except Exception as e:
                QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi.")

    def update_data(self):
        id_pengunjung = self.editIDPengunjung.text()
        nama_pengunjung = self.editnmPengunjung.text()
        jenis_kelamin = self.cbJK.currentText()
        tanggal_kunjungan = self.dateTglKunjungan.date().toString("yyyy-MM-dd")
        if id_pengunjung and nama_pengunjung and jenis_kelamin and tanggal_kunjungan:
            try:
                self.cursor.execute("UPDATE pengunjung_masjid SET nama_pengunjung = %s, jenis_kelamin = %s, tanggal_kunjungan = %s "
                                    "WHERE id_pengunjung = %s",(nama_pengunjung, jenis_kelamin, tanggal_kunjungan, id_pengunjung),)
                self.connection.commit()
                self.load_data()
                self.clear_inputs()
                QMessageBox.information(self, "Sukses", "Data berhasil diubah.")
            except Exception as e:
                QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi.")

    def delete_data(self):
        id_pengunjung = self.editIDPengunjung.text()
        if id_pengunjung:
            try:
                self.cursor.execute("DELETE FROM pengunjung_masjid WHERE id_pengunjung = %s", (id_pengunjung,))
                self.connection.commit()
                self.load_data()
                self.clear_inputs()
                QMessageBox.information(self, "Sukses", "Data berhasil dihapus.")
            except Exception as e:
                QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Kode kategori harus diisi untuk menghapus data.")

    def clear_inputs(self):
        self.editIDPengunjung.clear()
        self.editnmPengunjung.clear()
        self.cbJK.setCurrentIndex(0)
        self.dateTglKunjungan.setDate(QDate.currentDate())

    def on_table_click(self, index):
        try:
            row = index.row()
            record = self.model._data[row]
            self.editIDPengunjung.setText(str(record[0]))
            self.editnmPengunjung.setText(str(record[1]))
            self.cbJK.setCurrentText(str(record[2]))
            self.dateTglKunjungan.setDate(QDate.fromString(record[3], "yyyy-MM-dd") if isinstance(record[3], str) else QDate(record[3].year,record[3].month,record[3].day))

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Terjadi kesalahan: {e}")

    def print_pdf(self):
        try:
            data = self.fetch_allPDF()
            if not data:
                QMessageBox.warning(self, "Data Kosong", "Tidak ada data untuk dicetak.")
                return

            pdf_file = "pengunjung_report.pdf"
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter

            # Header laporan
            c.drawString(100, height - 50, "Laporan Data Pengunjung")
            c.drawString(100, height - 100, "ID Pengunjung")
            c.drawString(200, height - 100, "Nama Pengunjung")
            c.drawString(320, height - 100, "Jenis Kelamin")
            c.drawString(420, height - 100, "Tanggal Kunjungan")

            # Isi laporan
            y_position = height - 120
            for row in data:
                tanggal_kunjungan = row[3]
                if isinstance(tanggal_kunjungan, date):
                    tanggal_kunjungan = tanggal_kunjungan.strftime("%d-%m-%Y")

                c.drawString(100, y_position, str(row[0]))
                c.drawString(200, y_position, row[1])
                c.drawString(320, y_position, row[2])
                c.drawString(420, y_position, tanggal_kunjungan)

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
    window = FormPengunjung()
    window.show()
    sys.exit(app.exec())
