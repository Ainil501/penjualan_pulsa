from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton

def halaman_pelanggan():
    widget = QWidget()

    layout = QVBoxLayout()

    btn = QPushButton("Kembali")

    def navigasi():
        window = QApplication.activeWindow()
        window.buka_riwayat()

    btn.clicked.connect(navigasi)

    layout.addWidget(btn)
    layout.addWidget(QLabel("Halaman pelanggan"))
    widget.setLayout(layout)

    return widget