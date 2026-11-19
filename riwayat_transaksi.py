from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

def halaman_riwayat(pindah_halaman):
    widget = QWidget()

    layout = QVBoxLayout()
    layout.addWidget(QLabel("Halaman Riwayat Transaksi"))

    btn_pelanggan = QPushButton("Daftar Pelanggan")

    btn_pelanggan.clicked.connect(pindah_halaman)

    layout.addWidget(btn_pelanggan)

    widget.setLayout(layout)

    return widget
