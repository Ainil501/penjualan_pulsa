
import sqlite3
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QMainWindow,
    QTabWidget
)

DB_NAME = "pulsa.db"


# ---------------------------------------------------------------
# DATABASE
# ---------------------------------------------------------------
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

    # Data contoh
    data_contoh = [
        (1, "09/10/2026", "berhasil", "anto", "08123", 12000, "hot promo", 10000),
        (2, "10/10/2026", "berhasil", "budi", "08567", 22000, "super hemat", 20000),
        (3, "11/10/2026", "berhasil", "siti", "08999", 17000, "paket gaul", 15000),
    ]

    for (id_, tgl, status, nama, hp, total, paket, nominal) in data_contoh:

        cur.execute(
            """
            INSERT OR IGNORE INTO transaksi
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (id_, tgl, status, nama, hp, total)
        )

        cur.execute(
            """
            INSERT OR IGNORE INTO detail_transaksi
            (id, transaksi_id, nama_paket, nominal)
            VALUES (?, ?, ?, ?)
            """,
            (id_, id_, paket, nominal)
        )

    conn.commit()
    conn.close()


# ---------------------------------------------------------------
# MENGAMBIL DATA TRANSAKSI
# ---------------------------------------------------------------
def ambil_transaksi(id_transaksi):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT
            t.id,
            t.tanggal,
            t.status,
            t.nama,
            t.nomor_hp,
            t.total_bayar,
            d.nama_paket,
            d.nominal

        FROM transaksi t

        JOIN detail_transaksi d
        ON d.transaksi_id = t.id

        WHERE t.id = ?
    """, (id_transaksi,))

    row = cur.fetchone()

    conn.close()

    return row


# ---------------------------------------------------------------
# MENAMBAHKAN TRANSAKSI
# ---------------------------------------------------------------
def tambah_transaksi(
    tanggal,
    status,
    nama,
    nomor_hp,
    nama_paket,
    nominal,
    total_bayar
):

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


# ---------------------------------------------------------------
# FORMAT RUPIAH
# ---------------------------------------------------------------
def rupiah(angka):
    return f"Rp {angka:,}".replace(",", ".")


# ---------------------------------------------------------------
# HALAMAN DETAIL TRANSAKSI
# ---------------------------------------------------------------
def halaman_detail():

    widget = QWidget()

    layout = QVBoxLayout()

    # -----------------------------------------------------------
    # LABEL
    # -----------------------------------------------------------
    judul = QLabel("Halaman Detail Transaksi")
    judul.setFont(QFont("Arial", 20))
    judul.setAlignment(Qt.AlignmentFlag.AlignCenter)

    label_id = QLabel("ID Transaksi: Belum dipilih")
    label_tanggal = QLabel()
    label_status = QLabel()
    label_nama = QLabel()
    label_hp = QLabel()
    label_paket = QLabel()
    label_nominal = QLabel()
    label_total = QLabel()

    # -----------------------------------------------------------
    # PESAN ERROR
    # -----------------------------------------------------------
    label_error = QLabel(
        "Data tidak valid: transaksi tidak ditemukan"
    )

    label_error.setStyleSheet("color: red;")
    label_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label_error.hide()

    # -----------------------------------------------------------
    # TOMBOL KEMBALI
    # -----------------------------------------------------------
    btn = QPushButton("Kembali")
    btn.setFixedWidth(120)

    def navigasi():

        window = QApplication.activeWindow()

        if window is not None:
            window.buka_riwayat()

    btn.clicked.connect(navigasi)

    # -----------------------------------------------------------
    # MENAMBAHKAN WIDGET KE LAYOUT
    # -----------------------------------------------------------
    layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignLeft)
    layout.addWidget(judul)

    layout.addSpacing(15)

    layout.addWidget(label_id)
    layout.addWidget(label_tanggal)
    layout.addWidget(label_status)

    layout.addSpacing(15)

    layout.addWidget(label_nama)
    layout.addWidget(label_hp)

    layout.addSpacing(15)

    layout.addWidget(label_paket)
    layout.addWidget(label_nominal)

    layout.addSpacing(15)

    layout.addWidget(label_total)
    layout.addWidget(label_error)

    layout.addStretch()

    widget.setLayout(layout)

    # -----------------------------------------------------------
    # FUNGSI MENAMPILKAN DATA TRANSAKSI
    # -----------------------------------------------------------
    def tampilkan(id_transaksi):

        row = ambil_transaksi(id_transaksi)

        if row is None:

            label_error.show()

            label_id.setText("ID Transaksi: -")
            label_tanggal.setText("")
            label_status.setText("")
            label_nama.setText("")
            label_hp.setText("")
            label_paket.setText("")
            label_nominal.setText("")
            label_total.setText("")

            return

        (
            id_,
            tanggal,
            status,
            nama,
            hp,
            total,
            paket,
            nominal
        ) = row

        label_error.hide()

        label_id.setText(f"ID Transaksi: {id_:02d}")
        label_tanggal.setText(f"Tanggal: {tanggal}")
        label_status.setText(f"Status: {status}")
        label_nama.setText(f"Nama: {nama}")
        label_hp.setText(f"Nomor HP: {hp}")
        label_paket.setText(f"Nama Paket: {paket}")
        label_nominal.setText(f"Nominal: {rupiah(nominal)}")
        label_total.setText(f"Total Bayar: {rupiah(total)}")

    # Menghubungkan fungsi tampilkan ke widget
    widget.tampilkan = tampilkan

    # Mengembalikan widget dan label
    return widget, label_id


# ---------------------------------------------------------------
# HALAMAN RIWAYAT TRANSAKSI
# ---------------------------------------------------------------
class Riwayat(QWidget):

    def __init__(self, buka_detail):

        super().__init__()

        self.buka_detail = buka_detail

        # Input ID transaksi
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText(
            "Masukkan ID transaksi (1, 2, 3)"
        )

        # Tombol detail
        btn = QPushButton("Lihat Detail")
        btn.clicked.connect(self.klik_detail)

        # Tombol tambah transaksi
        btn_tambah = QPushButton("Tambah Transaksi Contoh")
        btn_tambah.clicked.connect(self.klik_tambah)

        # Layout
        layout = QVBoxLayout()

        judul = QLabel("Riwayat Transaksi")
        judul.setFont(QFont("Arial", 20))
        judul.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(judul)
        layout.addSpacing(15)
        layout.addWidget(self.input_id)
        layout.addWidget(btn)
        layout.addWidget(btn_tambah)
        layout.addStretch()

        self.setLayout(layout)

    # -----------------------------------------------------------
    # MEMBUKA DETAIL TRANSAKSI
    # -----------------------------------------------------------
    def klik_detail(self):

        teks = self.input_id.text().strip()

        id_transaksi = int(teks) if teks.isdigit() else -1

        self.buka_detail(id_transaksi)

    # -----------------------------------------------------------
    # MENAMBAHKAN TRANSAKSI CONTOH
    # -----------------------------------------------------------
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

        self.buka_detail(id_baru)


# ---------------------------------------------------------------
# MAIN WINDOW
# ---------------------------------------------------------------
class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Aplikasi Transaksi Pulsa")
        self.resize(480, 560)

        # Tab halaman
        self.tabs = QTabWidget()

        # Membuat halaman riwayat
        self.riwayat = Riwayat(self.buka_detail)

        # Membuat halaman detail
        self.detail, self.label_id = halaman_detail()

        # Memasukkan halaman ke tab
        self.tabs.addTab(self.riwayat, "Riwayat")
        self.tabs.addTab(self.detail, "Detail")

        self.setCentralWidget(self.tabs)

    # -----------------------------------------------------------
    # NAVIGASI KE HALAMAN DETAIL
    # -----------------------------------------------------------
    def buka_detail(self, id_transaksi):

        self.detail.tampilkan(id_transaksi)

        self.tabs.setCurrentWidget(self.detail)

    # -----------------------------------------------------------
    # NAVIGASI KEMBALI KE RIWAYAT
    # -----------------------------------------------------------
    def buka_riwayat(self):

        self.tabs.setCurrentWidget(self.riwayat)


# ---------------------------------------------------------------
# PROGRAM UTAMA
# ---------------------------------------------------------------
if __name__ == "__main__":

    init_db()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
