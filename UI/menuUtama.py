from PyQt6.QtWidgets import QMainWindow,QPushButton
from PyQt6.uic import loadUi
from mesjid import FormMesjid
from kamera import FormKamera
from acara import FormAcara
from pengunjung import FormPengunjung


class menuUtama(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('menuUtama.ui',self)
        self.btnMesjid = self.findChild(QPushButton, "btnMesjid")
        self.btnAcara = self.findChild(QPushButton, "btnAcara")
        self.btnKamera = self.findChild(QPushButton, "btnKamera")
        self.btnPengunjung = self.findChild(QPushButton, "btnPengunjung")

        self.btnMesjid.clicked.connect(self.tampil_mesjid)
        self.btnAcara.clicked.connect(self.tampil_acara)
        self.btnKamera.clicked.connect(self.tampil_kamera)
        self.btnPengunjung.clicked.connect(self.tampil_pengunjung)


    def tampil_mesjid(self):
        self.mesjid = FormMesjid()
        self.mesjid.show()
        # self.close()

    def tampil_acara(self):
        self.acara = FormAcara()
        self.acara.show()
        # self.close()

    def tampil_kamera(self):
        self.kamera = FormKamera()
        self.kamera.show()
        # self.close()

    def tampil_pengunjung(self):
        self.pengunjung = FormPengunjung()
        self.pengunjung.show()
        # self.close()
