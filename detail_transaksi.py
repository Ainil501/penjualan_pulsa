from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QVBoxLayout, QPushButton
)

def halaman_detail():
    widget = QWidget()

    layout = QVBoxLayout()

    label_id = QLabel("ID Transaksi: Belum dipilih")

    btn = QPushButton("Kembali")

    def navigasi():
        window = QApplication.activeWindow()
        window.buka_riwayat()

    btn.clicked.connect(navigasi)

    layout.addWidget(QLabel("Halaman Detail"))
    layout.addWidget(label_id)
    layout.addWidget(btn)

    widget.setLayout(layout)

    # Mengembalikan widget dan label
    return widget, label_id