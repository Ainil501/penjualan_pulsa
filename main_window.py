import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Penjualan Pulsa")

        self.tabs = QTabWidget()
        self.tabs.tabBar().hide()

        #tambah disini
        self.tabs.addTab(, "riwayat")

        self.setCentralWidget(self.tabs)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
