import sqlite3
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QMainWindow,
    QTabWidget,
    QListWidget,
    QListWidgetItem
)

DB_NAME = "pulsa.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            status TEXT,
            nama TEXT,
            nomor_hp TEXT,
            total_bayar INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS detail_transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaksi_id INTEGER,
            nama_paket TEXT,
            nominal INTEGER,
            FOREIGN KEY (transaksi_id) REFERENCES transaksi(id)
        )
    """)

    data_contoh = [
        (1, "09/10/2026", "berhasil", "anto", "08123", 12000, "hot promo", 10000),
        (2, "10/10/2026", "berhasil", "budi", "08567", 22000, "super hemat", 20000),
        (3, "11/10/2026", "berhasil", "siti", "08999", 17000, "paket gaul", 15000),
    ]

    for (id_, tgl, status, nama, hp, total, paket, nominal) in data_contoh:

        cur.execute(
            "INSERT OR IGNORE INTO transaksi VALUES (?, ?, ?, ?, ?, ?)",
            (id_, tgl, status, nama, hp, total)
        )

        cur.execute(
            """INSERT OR IGNORE INTO detail_transaksi
            (id, transaksi_id, nama_paket, nominal)
            VALUES (?, ?, ?, ?)""",
            (id_, id_, paket, nominal)
        )

    conn.commit()
    conn.close()


def ambil_semua_transaksi():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, tanggal, nama, total_bayar
        FROM transaksi
        ORDER BY id DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


def ambil_transaksi(id_transaksi):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT t.id, t.tanggal, t.status, t.nama,
               t.nomor_hp, t.total_bayar,
               d.nama_paket, d.nominal
        FROM transaksi t
        JOIN detail_transaksi d
        ON d.transaksi_id = t.id
        WHERE t.id = ?
    """, (id_transaksi,))

    row = cur.fetchone()

    conn.close()

    return row


def tambah_transaksi(tanggal, status, nama, nomor_hp,
                     nama_paket, nominal, total_bayar):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO transaksi
        (tanggal, status, nama, nomor_hp, total_bayar)
        VALUES (?, ?, ?, ?, ?)
    """, (tanggal, status, nama, nomor_hp, total_bayar))

    id_baru = cur.lastrowid

    cur.execute("""
        INSERT INTO detail_transaksi
        (transaksi_id, nama_paket, nominal)
        VALUES (?, ?, ?)
    """, (id_baru, nama_paket, nominal))

    conn.commit()
    conn.close()

    return id_baru


def rupiah(angka):
    return f"{angka:,}".replace(",", ".")


def halaman_detail(kembali):

    widget = QWidget()

    layout = QVBoxLayout()

    judul = QLabel("Halaman Detail")
    judul.setFont(QFont("Arial", 24))
    judul.setAlignment(Qt.AlignmentFlag.AlignCenter)

    label_id = QLabel("ID Transaksi: Belum dipilih")

    label_tanggal = QLabel("Tanggal: -")
    label_status = QLabel("Status: -")
    label_nama = QLabel("Nama: -")
    label_hp = QLabel("Nomor HP: -")
    label_paket = QLabel("Nama Paket: -")
    label_nominal = QLabel("Nominal: -")
    label_total = QLabel("Total Bayar: -")

    btn = QPushButton("Kembali")
    btn.clicked.connect(kembali)

    def tampilkan(id_transaksi):

        row = ambil_transaksi(id_transaksi)

        if row is None:

            label_id.setText("ID Transaksi: Tidak ditemukan")
            label_tanggal.setText("Tanggal: -")
            label_status.setText("Status: -")
            label_nama.setText("Nama: -")
            label_hp.setText("Nomor HP: -")
            label_paket.setText("Nama Paket: -")
            label_nominal.setText("Nominal: -")
            label_total.setText("Total Bayar: -")

            return

        (id_, tanggal, status, nama, hp,
         total, paket, nominal) = row

        label_id.setText(f"ID Transaksi: {id_}")
        label_tanggal.setText(f"Tanggal: {tanggal}")
        label_status.setText(f"Status: {status}")
        label_nama.setText(f"Nama: {nama}")
        label_hp.setText(f"Nomor HP: {hp}")
        label_paket.setText(f"Nama Paket: {paket}")
        label_nominal.setText(f"Nominal: Rp {rupiah(nominal)}")
        label_total.setText(f"Total Bayar: Rp {rupiah(total)}")

    layout.addWidget(btn)
    layout.addWidget(judul)
    layout.addWidget(label_id)
    layout.addWidget(label_tanggal)
    layout.addWidget(label_status)
    layout.addWidget(label_nama)
    layout.addWidget(label_hp)
    layout.addWidget(label_paket)
    layout.addWidget(label_nominal)
    layout.addWidget(label_total)
    layout.addStretch()

    widget.setLayout(layout)

    widget.tampilkan = tampilkan

    return widget


class Riwayat(QWidget):

    def __init__(self, buka_detail):
        super().__init__()

        self.buka_detail = buka_detail

        self.daftar = QListWidget()
        self.daftar.itemClicked.connect(self.klik_item)

        btn_tambah = QPushButton("Tambah Transaksi Contoh")
        btn_tambah.clicked.connect(self.klik_tambah)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Riwayat Transaksi / Beranda"))
        layout.addWidget(self.daftar)
        layout.addWidget(btn_tambah)

        self.setLayout(layout)

        self.muat_daftar()

    def muat_daftar(self):

        self.daftar.clear()

        for (id_, tanggal, nama, total) in ambil_semua_transaksi():

            item = QListWidgetItem(
                f"#{id_}  |  {tanggal}  |  {nama}  |  Rp {rupiah(total)}"
            )
            item.setData(Qt.ItemDataRole.UserRole, id_)

            self.daftar.addItem(item)

    def klik_item(self, item):

        id_transaksi = item.data(Qt.ItemDataRole.UserRole)

        self.buka_detail(id_transaksi)

    def klik_tambah(self):

        id_baru = tambah_transaksi(
            "12/10/2026",
            "berhasil",
            "dewi",
            "08777",
            "paket hemat",
            25000,
            27000
        )

        self.muat_daftar()

        self.buka_detail(id_baru)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Detail Transaksi")
        self.resize(480, 560)

        self.tabs = QTabWidget()

        self.riwayat = Riwayat(self.buka_detail)

        self.detail = halaman_detail(self.buka_riwayat)

        self.tabs.addTab(self.riwayat, "Riwayat")
        self.tabs.addTab(self.detail, "Detail")

        self.setCentralWidget(self.tabs)

    def buka_detail(self, id_transaksi):

        self.detail.tampilkan(id_transaksi)

        self.tabs.setCurrentWidget(self.detail)

    def buka_riwayat(self):

        self.tabs.setCurrentWidget(self.riwayat)


if __name__ == "__main__":

    init_db()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
