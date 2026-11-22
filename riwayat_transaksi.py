
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem
)

import sqlite3


def halaman_riwayat():
    widget = QWidget()

    layout = QVBoxLayout()
    layout1 = QHBoxLayout()

    layout.addWidget(QLabel("Halaman Riwayat Transaksi"))


    # Mengambil data database
    conn = sqlite3.connect("penjualan_pulsa.sqlite")
    cursor = conn.cursor()
    table = QTableWidget()
    table.setColumnCount(4)

    table.setHorizontalHeaderLabels([
        "Nomor", "Tanggal", "Nama Paket", "Aksi"
    ])

    table.setEditTriggers(
        QTableWidget.EditTrigger.NoEditTriggers
    )

    try:
        cursor.execute("""
            SELECT t.id_transaksi, t.tanggal, p.nama_paket
            FROM transaksi t
            JOIN detail d ON t.id_transaksi = d.id_transaksi
            JOIN paket p ON d.id_paket = p.id_paket
        """)

        rows = cursor.fetchall()

    except sqlite3.OperationalError:
        rows = []

    if len(rows) > 0:
        table.setRowCount(len(rows))

        # Menyimpan ID transaksi berdasarkan nomor baris
        daftar_id = []

        for i, row in enumerate(rows):
            daftar_id.append(row[0])

            table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            table.setItem(i, 1, QTableWidgetItem(str(row[1])))
            table.setItem(i, 2, QTableWidgetItem(str(row[2])))
            table.setItem(i, 3, QTableWidgetItem("Detail"))

        # Ketika baris diklik
        def buka_detail(baris, kolom):
            id_transaksi = daftar_id[baris]

            window = QApplication.activeWindow()
            window.buka_detail(id_transaksi)

        table.cellClicked.connect(buka_detail)

    else:
        table.setRowCount(1)
        table.setSpan(0, 0, 1, 3)

        table.setItem(
            0, 0,
            QTableWidgetItem("Data tidak ditemukan")
        )

    layout.addWidget(table)

    # Tombol navigasi
    btn_pelanggan = QPushButton("Daftar Pelanggan")
    btn_pembelian = QPushButton("Beli Pulsa")

    btn_pelanggan.clicked.connect(navigasi1)
    btn_pembelian.clicked.connect(navigasi2)

    layout1.addWidget(btn_pembelian)
    layout1.addWidget(btn_pelanggan)

    layout.addLayout(layout1)

    widget.setLayout(layout)

    return widget


# Function navigasi
def navigasi1():
    window = QApplication.activeWindow()
    window.buka_pelanggan()


def navigasi2():
    window = QApplication.activeWindow()
    window.buka_pembelian()


def navigasi3(id_transaksi, checked=False):
    window = QApplication.activeWindow()
    window.buka_detail(id_transaksi)
