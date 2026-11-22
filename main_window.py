import sys
import os

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget,
    QPushButton, QVBoxLayout, QWidget
)

from riwayat_transaksi import halaman_riwayat
from daftar_pelanggan import halaman_pelanggan
from pembelian_pulsa import halaman_pembelian
from detail_transaksi import halaman_detail
from database import buat_database


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Penjualan Pulsa")
        self.setGeometry(300,300,500,600)

        # if not os.path.exists("penjualan_pulsa.sqlite"):
        #     buat_database()

            
        # Membuat halaman
        self.riwayat = halaman_riwayat()
        self.pelanggan = halaman_pelanggan()
        self.pembelian = halaman_pembelian()
        self.detail, self.label_id = halaman_detail()

        # Membuat tab
        self.tabs = QTabWidget()
        self.tabs.tabBar().hide()

        self.tabs.addTab(self.riwayat, "Riwayat")
        self.tabs.addTab(self.pelanggan, "Pelanggan")
        self.tabs.addTab(self.pembelian, "Pembelian")
        self.tabs.addTab(self.detail, "Detail")

        self.setCentralWidget(self.tabs)

    # Function navigasi
    def buka_riwayat(self):
        self.tabs.setCurrentWidget(self.riwayat)

    def buka_pelanggan(self):
        self.tabs.setCurrentWidget(self.pelanggan)

    def buka_pembelian(self):
        self.tabs.setCurrentWidget(self.pembelian)

    def buka_detail(self, id_transaksi):
        self.label_id.setText(f"ID Transaksi: {id_transaksi}")
        self.tabs.setCurrentWidget(self.detail)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()