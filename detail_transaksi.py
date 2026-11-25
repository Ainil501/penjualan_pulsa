import sqlite3
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

DB_NAME = "pulsa.db"


# ---------------------------------------------------------------
# DATABASE (tabel transaksi + tabel detail_transaksi)
# ---------------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY,
            tanggal TEXT,
            status TEXT,
            nama TEXT,
            nomor_hp TEXT,
            total_bayar INTEGER
        )"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS detail_transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaksi_id INTEGER,
            nama_paket TEXT,
            nominal INTEGER,
            FOREIGN KEY (transaksi_id) REFERENCES transaksi(id)
        )"""
    )
    # data contoh sesuai mockup (hanya dimasukkan jika masih kosong)
    cur.execute("SELECT COUNT(*) FROM transaksi")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO transaksi VALUES (1, '09/10/2026', 'berhasil', 'anto', '08123', 12000)"
        )
        cur.execute(
            "INSERT INTO detail_transaksi (transaksi_id, nama_paket, nominal) "
            "VALUES (1, 'hot promo', 10000)"
        )
    conn.commit()
    conn.close()


def ambil_transaksi(id_transaksi):
    """Ambil data transaksi + detail berdasarkan id. Return None jika tidak ada."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """SELECT t.id, t.tanggal, t.status, t.nama, t.nomor_hp, t.total_bayar,
                  d.nama_paket, d.nominal
           FROM transaksi t
           JOIN detail_transaksi d ON d.transaksi_id = t.id
           WHERE t.id = ?""",
        (id_transaksi,),
    )
    row = cur.fetchone()
    conn.close()
    return row


def rupiah(angka):
    return f"{angka:,}".replace(",", ".")


# ---------------------------------------------------------------
# HALAMAN DETAIL TRANSAKSI
# ---------------------------------------------------------------
class DetailTransaksi(QWidget):
    def __init__(self, tabs, halaman_kembali):
        super().__init__()
        self.tabs = tabs                      # QTabWidget (slide modul 5)
        self.halaman_kembali = halaman_kembali

        # --- tombol kembali ---
        self.btn_kembali = QPushButton("kembali")
        self.btn_kembali.setFixedWidth(120)
        self.btn_kembali.clicked.connect(self.kembali)

        # --- judul ---
        judul = QLabel("Detail transaksi")
        judul.setFont(QFont("Arial", 24))
        judul.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- label data ---
        self.lbl_tanggal = QLabel()
        self.lbl_id = QLabel()
        self.lbl_status = QLabel()
        self.lbl_ringkasan = QLabel()
        self.lbl_nama = QLabel()
        self.lbl_hp = QLabel()
        self.lbl_paket = QLabel()
        self.lbl_nominal = QLabel()
        self.lbl_total = QLabel()

        # --- label pesan error (data tidak valid) ---
        self.lbl_error = QLabel("Data tidak valid: transaksi tidak ditemukan")
        self.lbl_error.setStyleSheet("color: red;")
        self.lbl_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_error.hide()

        # --- baris tanggal (kiri) & id (kanan): QHBoxLayout ---
        baris_atas = QHBoxLayout()
        baris_atas.addWidget(self.lbl_tanggal)
        baris_atas.addStretch()
        baris_atas.addWidget(self.lbl_id)

        # --- kelompok data: QVBoxLayout ---
        self.box_data = QWidget()
        data = QVBoxLayout()
        data.addLayout(baris_atas)
        data.addWidget(self.lbl_status)
        data.addWidget(self.lbl_ringkasan)
        data.addSpacing(20)
        data.addWidget(self.lbl_nama)
        data.addWidget(self.lbl_hp)
        data.addSpacing(20)
        data.addWidget(self.lbl_paket)
        data.addWidget(self.lbl_nominal)
        data.addSpacing(20)
        data.addWidget(self.lbl_total)
        data.addStretch()
        self.box_data.setLayout(data)

        # --- layout utama ---
        layout = QVBoxLayout()
        layout.addWidget(self.btn_kembali, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(judul)
        layout.addWidget(self.lbl_error)
        layout.addWidget(self.box_data)
        self.setLayout(layout)

    def tampilkan(self, id_transaksi):
        """Terima <id> sebagai acuan data, lalu tampilkan datanya."""
        row = ambil_transaksi(id_transaksi)

        if row is None:                       # <id> tidak ada
            self.box_data.hide()
            self.lbl_error.show()
            return

        (id_, tanggal, status, nama, hp, total, paket, nominal) = row
        self.lbl_error.hide()
        self.box_data.show()

        self.lbl_tanggal.setText(f"tanggal: {tanggal}")
        self.lbl_id.setText(f"id:{id_:02d}")
        self.lbl_status.setText(f"transaksi {status}")
        self.lbl_ringkasan.setText(f"kirim pulsa {paket} ke {hp}")
        self.lbl_nama.setText(f"nama: {nama}")
        self.lbl_hp.setText(f"nomor hp: {hp}")
        self.lbl_paket.setText(f"nama paket: {paket}")
        self.lbl_nominal.setText(f"nominal: {nominal}")
        self.lbl_total.setText(f"total bayar: {rupiah(total)}")

    def kembali(self):
        # kembali ke beranda/riwayat memakai setCurrentWidget() di QTabWidget
        self.tabs.setCurrentWidget(self.halaman_kembali)


# ---------------------------------------------------------------
# HALAMAN BERANDA (contoh untuk membuka detail berdasarkan id)
# ---------------------------------------------------------------
class Beranda(QWidget):
    def __init__(self, buka_detail):
        super().__init__()
        self.buka_detail = buka_detail

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("Masukkan id transaksi (contoh: 1)")
        btn = QPushButton("Lihat detail")
        btn.clicked.connect(self.klik_detail)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Riwayat transaksi / Beranda"))
        layout.addWidget(self.input_id)
        layout.addWidget(btn)
        layout.addStretch()
        self.setLayout(layout)

    def klik_detail(self):
        teks = self.input_id.text().strip()
        id_transaksi = int(teks) if teks.isdigit() else -1   # -1 => tidak valid
        self.buka_detail(id_transaksi)


# ---------------------------------------------------------------
# MAIN WINDOW dengan QTabWidget
# ---------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Detail Transaksi")
        self.resize(480, 560)

        self.tabs = QTabWidget()
        self.beranda = Beranda(self.buka_detail)
        self.detail = DetailTransaksi(self.tabs, self.beranda)

        self.tabs.addTab(self.beranda, "Beranda")
        self.tabs.addTab(self.detail, "Detail")
        self.setCentralWidget(self.tabs)

    def buka_detail(self, id_transaksi):
        self.detail.tampilkan(id_transaksi)
        self.tabs.setCurrentWidget(self.detail)


init_db()
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
