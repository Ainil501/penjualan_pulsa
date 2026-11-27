from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLineEdit
)

import sqlite3

# Variabel global
table = None
search_tanggal = None
search_paket = None
daftar_id = []

def halaman_riwayat():
    global table, search_tanggal, search_paket

    widget = QWidget()

    layout = QVBoxLayout()
    layout1 = QHBoxLayout()

    layout.addWidget(QLabel("Halaman Riwayat Transaksi"))


    search_tanggal = QLineEdit()
    search_tanggal.setPlaceholderText("Cari tanggal...")
    search_tanggal.textChanged.connect(update_filter)
    layout.addWidget(search_tanggal)

    search_paket = QLineEdit()
    search_paket.setPlaceholderText("Cari nama paket...")
    search_paket.textChanged.connect(update_filter)
    layout.addWidget(search_paket)


    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels([
        "Nomor", "Tanggal", "Nama Paket", "Aksi"
    ])
    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    table.cellClicked.connect(klik_tabel)
    layout.addWidget(table)


    btn_pelanggan = QPushButton("Daftar Pelanggan")
    btn_pembelian = QPushButton("Beli Pulsa")

    btn_pelanggan.clicked.connect(navigasi1)
    btn_pembelian.clicked.connect(navigasi2)

    layout1.addWidget(btn_pembelian)
    layout1.addWidget(btn_pelanggan)

    layout.addLayout(layout1)

    widget.setLayout(layout)

    load_data()

    return widget


def load_data(keyword1="", keyword2=""):
    global daftar_id
    rows = []

    conn = sqlite3.connect("penjualan_pulsa.sqlite")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id_transaksi, t.tanggal, p.nama_paket
            FROM transaksi t
            JOIN detail d ON t.id_transaksi = d.id_transaksi
            JOIN paket p ON d.id_paket = p.id_paket
            WHERE t.tanggal LIKE ? AND p.nama_paket LIKE ?
        """, (f"%{keyword1}%", f"%{keyword2}%"))
        rows = cursor.fetchall()
    except sqlite3.OperationalError:
        rows = []
    finally:
        conn.close()

    table.clearSpans()
    table.setRowCount(0)
    daftar_id = []

    if len(rows) == 0:
        table.setRowCount(1)
        table.setSpan(0, 0, 1, 4)
        table.setItem(0, 0, QTableWidgetItem("Data tidak ditemukan"))
        return

    table.setRowCount(len(rows))

    for i, row in enumerate(rows):
        daftar_id.append(row[0])

        table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
        table.setItem(i, 1, QTableWidgetItem(str(row[1])))
        table.setItem(i, 2, QTableWidgetItem(str(row[2])))
        table.setItem(i, 3, QTableWidgetItem("Detail"))


def klik_tabel(baris, kolom):
    if kolom == 3 and baris < len(daftar_id):
        navigasi3(daftar_id[baris])


def update_filter():
    keyword1 = search_tanggal.text().strip()
    keyword2 = search_paket.text().strip()
    load_data(keyword1, keyword2)


# Function navigasi
def navigasi1():
    window = QApplication.activeWindow()
    window.buka_pelanggan()


def navigasi2():
    window = QApplication.activeWindow()
    window.buka_pembelian()


def navigasi3(id_transaksi):
    window = QApplication.activeWindow()
    window.buka_detail(id_transaksi)