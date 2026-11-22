from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

def halaman_pembelian():
    widget = QWidget()

    layout = QVBoxLayout()

    btn = QPushButton("Kembali")

    def navigasi():
        window = QApplication.activeWindow()
        window.buka_riwayat()

    btn.clicked.connect(navigasi)

    layout.addWidget(btn)
    layout.addWidget(QLabel("Halaman pembelian pulsa"))
    widget.setLayout(layout)

    return widget