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


class FormAcara(QMainWindow):
    def __init__(self):
        super().__init__()

        # Memuat file .ui
        uic.loadUi("acara.ui", self)

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
        self.tableAcara.clicked.connect(self.on_table_click)
        self.btnCetak.clicked.connect(self.print_pdf)

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM acara_keagamaan")
        data = self.cursor.fetchall()
        headers = [desc[0] for desc in self.cursor.description]
        return data, headers

    def fetch_allPDF(self):
        try:
            self.cursor.execute("SELECT *FROM acara_keagamaan")
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
            self.tableAcara.setModel(self.model)
        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan saat memuat data: {e}")

    def add_data(self):
        id_acara = self.editIDAcara.text()
        nama_acara = self.editnmAcara.text()
        tanggal_acara = self.dateEditAcara.date().toString("yyyy-MM-dd")
        lokasi = self.editLokasi.text()
        deskripsi = self.editDeskrip.text()
        dibuat_oleh = self.editOleh.text()
        if id_acara and nama_acara and tanggal_acara and lokasi and deskripsi and dibuat_oleh:
            try:
                self.cursor.execute("INSERT INTO acara_keagamaan (id_acara, nama_acara, tanggal_acara, lokasi, deskripsi, dibuat_oleh) VALUES (%s, %s, %s, %s, %s, %s)",(id_acara, nama_acara, tanggal_acara, lokasi, deskripsi, dibuat_oleh),)
                self.connection.commit()
                self.clear_inputs()
                self.load_data()
                QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan.")
            except Exception as e:
                QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi.")

    def update_data(self):
        id_acara = self.editIDAcara.text()
        nama_acara = self.editnmAcara.text()
        tanggal_acara = self.dateEditAcara.date().toString("yyyy-MM-dd")
        lokasi = self.editLokasi.text()
        deskripsi = self.editDeskrip.text()
        dibuat_oleh = self.editOleh.text()
        if id_acara and nama_acara and tanggal_acara and lokasi and deskripsi and dibuat_oleh:
            try:
                self.cursor.execute("UPDATE acara_keagamaan SET nama_acara = %s, tanggal_acara = %s, lokasi = %s, deskripsi = %s, dibuat_oleh = %s "
                                    "WHERE id_acara = %s",(nama_acara, tanggal_acara, lokasi, deskripsi, dibuat_oleh, id_acara ),)
                self.connection.commit()
                self.load_data()
                self.clear_inputs()
                QMessageBox.information(self, "Sukses", "Data berhasil diubah.")
            except Exception as e:
                QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi.")

    def delete_data(self):
        id_acara = self.editIDAcara.text()
        if id_acara:
            try:
                self.cursor.execute("DELETE FROM acara_keagamaan WHERE id_acara = %s", (id_acara,))
                self.connection.commit()
                self.load_data()
                self.clear_inputs()
                QMessageBox.information(self, "Sukses", "Data berhasil dihapus.")
            except Exception as e:
                QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Kode kategori harus diisi untuk menghapus data.")

    def clear_inputs(self):
        self.editIDAcara.clear()
        self.editnmAcara.clear()
        self.dateEditAcara.setDate(QDate.currentDate())
        self.editLokasi.clear()
        self.editDeskrip.clear()
        self.editOleh.clear()

    def on_table_click(self, index):
        try:
            row = index.row()
            record = self.model._data[row]
            self.editIDAcara.setText(str(record[0]))
            self.editnmAcara.setText(str(record[1]))
            self.dateEditAcara.setDate(QDate.fromString(record[2], "yyyy-MM-dd") if isinstance(record[2], str) else QDate(record[2].year,record[2].month,record[2].day))
            self.editLokasi.setText(str(record[3]))
            self.editDeskrip.setText(str(record[4]))
            self.editOleh.setText(str(record[5]))

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Terjadi kesalahan: {e}")

    def print_pdf(self):
        try:
            data = self.fetch_allPDF()
            if not data:
                QMessageBox.warning(self, "Data Kosong", "Tidak ada data untuk dicetak.")
                return

            pdf_file = "acara_report.pdf"
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter

            # Header laporan
            c.drawString(100, height - 50, "Laporan Data Acara")
            c.drawString(100, height - 100, "ID Acara")
            c.drawString(160, height - 100, "Nama Acara")
            c.drawString(250, height - 100, "Tanggal Acara")
            c.drawString(350, height - 100, "Lokasi")
            c.drawString(420, height - 100, "Deskripsi")
            c.drawString(530, height - 100, "Dibuat Oleh")

            # Isi laporan
            y_position = height - 120
            for row in data:
                tanggal_acara = row[2]
                if isinstance(tanggal_acara, date):
                    tanggal_acara = tanggal_acara.strftime("%d-%m-%Y")

                c.drawString(100, y_position, str(row[0]))
                c.drawString(160, y_position, row[1])
                c.drawString(250, y_position, tanggal_acara)
                c.drawString(350, y_position, row[3])
                c.drawString(420, y_position, row[4])
                c.drawString(530, y_position, row[5])

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
    window = FormAcara()
    window.show()
    sys.exit(app.exec())
