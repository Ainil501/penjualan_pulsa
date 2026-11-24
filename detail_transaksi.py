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
# DATABASE
# ---------------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    # Data contoh (aman dijalankan berkali-kali)
    data_contoh = [
        (1, "09/10/2026", "berhasil", "anto", "08123", 12000, "hot promo", 10000),
        (2, "10/10/2026", "berhasil", "budi", "08567", 22000, "super hemat", 20000),
        (3, "11/10/2026", "berhasil", "siti", "08999", 17000, "paket gaul", 15000),
    ]
    for (id_, tgl, status, nama, hp, total, paket, nominal) in data_contoh:
        cur.execute(
            "INSERT OR IGNORE INTO transaksi VALUES (?, ?, ?, ?, ?, ?)",
            (id_, tgl, status, nama, hp, total),
        )
        cur.execute(
            "INSERT OR IGNORE INTO detail_transaksi (id, transaksi_id, nama_paket, nominal) "
            "VALUES (?, ?, ?, ?)",
            (id_, id_, paket, nominal),
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


def tambah_transaksi(tanggal, status, nama, nomor_hp, nama_paket, nominal, total_bayar):
    """Simpan transaksi baru ke dua tabel, lalu kembalikan id barunya."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transaksi (tanggal, status, nama, nomor_hp, total_bayar) "
        "VALUES (?, ?, ?, ?, ?)",
        (tanggal, status, nama, nomor_hp, total_bayar),
    )
    id_baru = cur.lastrowid          # id otomatis dari tabel transaksi
    cur.execute(
        "INSERT INTO detail_transaksi (transaksi_id, nama_paket, nominal) "
        "VALUES (?, ?, ?)",
        (id_baru, nama_paket, nominal),
    )
    conn.commit()
    conn.close()
    return id_baru


def rupiah(angka):
    return f"{angka:,}".replace(",", ".")


# ---------------------------------------------------------------
# HALAMAN DETAIL (gaya fungsi, sama seperti kode milikmu)
# ---------------------------------------------------------------
def halaman_detail():
    widget = QWidget()

    # --- tombol kembali ---
    btn = QPushButton("kembali")
    btn.setFixedWidth(120)

    def navigasi():
        window = QApplication.activeWindow()
        if window is not None:
            window.buka_riwayat()

    btn.clicked.connect(navigasi)

    # --- judul ---
    judul = QLabel("Detail transaksi")
    judul.setFont(QFont("Arial", 24))
    judul.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # --- label data ---
    label_tanggal = QLabel()
    label_id = QLabel("id: -")            # label id (ikut dikembalikan)
    label_status = QLabel()
    label_ringkasan = QLabel()
    label_nama = QLabel()
    label_hp = QLabel()
    label_paket = QLabel()
    label_nominal = QLabel()
    label_total = QLabel()

    # --- pesan error jika id tidak ada ---
    label_error = QLabel("Data tidak valid: transaksi tidak ditemukan")
    label_error.setStyleSheet("color: red;")
    label_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label_error.hide()

    # --- baris atas: tanggal (kiri) & id (kanan) ---
    baris_atas = QHBoxLayout()
    baris_atas.addWidget(label_tanggal)
    baris_atas.addStretch()
    baris_atas.addWidget(label_id)

    # --- kelompok data ---
    box_data = QWidget()
    data = QVBoxLayout()
    data.addLayout(baris_atas)
    data.addWidget(label_status)
    data.addWidget(label_ringkasan)
    data.addSpacing(20)
    data.addWidget(label_nama)
    data.addWidget(label_hp)
    data.addSpacing(20)
    data.addWidget(label_paket)
    data.addWidget(label_nominal)
    data.addSpacing(20)
    data.addWidget(label_total)
    data.addStretch()
    box_data.setLayout(data)

    # --- layout utama ---
    layout = QVBoxLayout()
    layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignLeft)
    layout.addWidget(judul)
    layout.addWidget(label_error)
    layout.addWidget(box_data)
    widget.setLayout(layout)

    # --- isi halaman berdasarkan <id> ---
    def tampilkan(id_transaksi):
        row = ambil_transaksi(id_transaksi)

        if row is None:                   # <id> tidak ada
            box_data.hide()
            label_error.show()
            return

        (id_, tanggal, status, nama, hp, total, paket, nominal) = row
        label_error.hide()
        box_data.show()

        label_tanggal.setText(f"tanggal: {tanggal}")
        label_id.setText(f"id:{id_:02d}")
        label_status.setText(f"transaksi {status}")
        label_ringkasan.setText(f"kirim pulsa {paket} ke {hp}")
        label_nama.setText(f"nama: {nama}")
        label_hp.setText(f"nomor hp: {hp}")
        label_paket.setText(f"nama paket: {paket}")
        label_nominal.setText(f"nominal: {nominal}")
        label_total.setText(f"total bayar: {rupiah(total)}")

    # tempelkan fungsi ke widget supaya bisa dipanggil: widget.tampilkan(id)
    widget.tampilkan = tampilkan

    # Mengembalikan widget dan label (sama seperti kodemu)
    return widget, label_id


# ---------------------------------------------------------------
# CONTOH PEMAKAIAN (MainWindow dengan buka_riwayat & buka_detail)
# ---------------------------------------------------------------
class Riwayat(QWidget):
    def __init__(self, buka_detail):
        super().__init__()
        self.buka_detail = buka_detail

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("Masukkan id transaksi (contoh: 1, 2, 3)")
        btn = QPushButton("Lihat detail")
        btn.clicked.connect(self.klik_detail)

        btn_tambah = QPushButton("Tambah transaksi contoh")
        btn_tambah.clicked.connect(self.klik_tambah)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Riwayat transaksi / Beranda"))
        layout.addWidget(self.input_id)
        layout.addWidget(btn)
        layout.addWidget(btn_tambah)
        layout.addStretch()
        self.setLayout(layout)

    def klik_detail(self):
        teks = self.input_id.text().strip()
        id_transaksi = int(teks) if teks.isdigit() else -1
        self.buka_detail(id_transaksi)

    def klik_tambah(self):
        id_baru = tambah_transaksi(
            "12/10/2026", "berhasil", "dewi", "08777", "paket hemat", 25000, 27000
        )
        self.buka_detail(id_baru)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Detail Transaksi")
        self.resize(480, 560)

        self.tabs = QTabWidget()
        self.riwayat = Riwayat(self.buka_detail)
        self.detail, self.label_id = halaman_detail()

        self.tabs.addTab(self.riwayat, "Riwayat")
        self.tabs.addTab(self.detail, "Detail")
        self.setCentralWidget(self.tabs)

    def buka_detail(self, id_transaksi):
        self.detail.tampilkan(id_transaksi)
        self.tabs.setCurrentWidget(self.detail)

    def buka_riwayat(self):
        # dipanggil tombol "kembali" di halaman_detail()
        self.tabs.setCurrentWidget(self.riwayat)


if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
