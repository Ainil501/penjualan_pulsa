from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import QRegularExpression, Qt, pyqtSignal
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QLineEdit, QGridLayout, QHBoxLayout, QMessageBox

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
    buat_tabel_kontak()
    form = FormKontak()
    form.kembali.connect(navigasi)
    layout.addWidget(form)
    widget.setLayout(layout)

    return widget  
    
PREFIX_OPERATOR = {
    "Telkomsel": ["0811", "0812", "0813", "0821", "0822", "0823", "0851", "0852", "0853"],
    "Indosat": ["0814", "0815", "0816", "0855", "0856", "0857", "0858"],
    "XL": ["0817", "0818", "0819", "0859", "0877", "0878"],
    "Tri": ["0895", "0896", "0897", "0898", "0899"],
    "Smartfren": ["0881", "0882", "0883", "0884", "0885", "0886", "0887", "0888", "0889"],
}


def cari_operator(nomor):
    prefix = nomor[:4]
    for operator, daftar in PREFIX_OPERATOR.items():
        if prefix in daftar:
            return operator
    return ""


def format_hp(nomor):
    if nomor is None:
        return ""
    teks = str(nomor)
    return teks if teks.startswith("0") else "0" + teks


def buat_tabel_kontak():
    q = QSqlQuery()
    q.exec("""CREATE TABLE IF NOT EXISTS kontak (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT,
                nomor_hp INTEGER,
                operator TEXT)""")


class FormKontak(QWidget):
    kembali = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.records = []
        self.index = 0
        self.setup_ui()
        self.muat_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        atas = QHBoxLayout()
        self.btn_kembali = QPushButton("kembali")
        self.btn_kembali.clicked.connect(self.kembali.emit)
        atas.addWidget(self.btn_kembali)
        atas.addStretch()
        layout.addLayout(atas)

        form = QGridLayout()
        self.input_id = QLineEdit()
        self.input_nama = QLineEdit()
        self.input_hp = QLineEdit()
        self.input_operator = QLineEdit()
        self.input_id.setEnabled(False)
        self.input_operator.setEnabled(False)
        self.input_hp.setValidator(
            QRegularExpressionValidator(QRegularExpression(r"\d{0,13}"), self)
        )
        self.input_hp.textChanged.connect(self.update_operator)

        form.addWidget(QLabel("id"), 0, 0)
        form.addWidget(self.input_id, 0, 1)
        form.addWidget(QLabel("nama"), 1, 0)
        form.addWidget(self.input_nama, 1, 1)
        form.addWidget(QLabel("nomor hp"), 2, 0)
        form.addWidget(self.input_hp, 2, 1)
        form.addWidget(QLabel("operator"), 3, 0)
        form.addWidget(self.input_operator, 3, 1)
        layout.addLayout(form)

        self.label_posisi = QLabel("")
        self.label_posisi.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_posisi)
        layout.addStretch()

        aksi_atas = QHBoxLayout()
        aksi_atas.addStretch()
        self.btn_tambah = QPushButton("tambah")
        self.btn_tambah.clicked.connect(self.tambah)
        aksi_atas.addWidget(self.btn_tambah)
        layout.addLayout(aksi_atas)

        bawah = QHBoxLayout()
        self.btn_sebelumnya = QPushButton("sebelumnya")
        self.btn_selanjutnya = QPushButton("selanjutnya")
        self.btn_simpan = QPushButton("simpan perubahan")
        self.btn_sebelumnya.clicked.connect(self.dispPrevious)
        self.btn_selanjutnya.clicked.connect(self.dispNext)
        self.btn_simpan.clicked.connect(self.simpan)
        bawah.addWidget(self.btn_sebelumnya)
        bawah.addWidget(self.btn_selanjutnya)
        bawah.addStretch()
        bawah.addWidget(self.btn_simpan)
        layout.addLayout(bawah)

    def muat_data(self, pilih_id=None):
        self.records = []
        q = QSqlQuery()
        q.exec("SELECT id, nama, nomor_hp, operator FROM kontak ORDER BY id")
        while q.next():
            self.records.append((q.value(0), q.value(1), q.value(2), q.value(3)))
        self.index = 0
        if pilih_id is not None:
            for i, rec in enumerate(self.records):
                if rec[0] == pilih_id:
                    self.index = i
        self.tampilkan()

    def tampilkan(self):
        if not self.records:
            self.input_id.clear()
            self.input_nama.clear()
            self.input_hp.clear()
            self.input_operator.clear()
            self.label_posisi.setText("Belum ada data")
            return
        id_, nama, nomor, operator = self.records[self.index]
        self.input_id.setText(str(id_))
        self.input_nama.setText(nama or "")
        self.input_hp.setText(format_hp(nomor))
        self.input_operator.setText(operator or "")
        self.label_posisi.setText(f"Record {self.index + 1} dari {len(self.records)}")

    def update_operator(self, teks):
        self.input_operator.setText(cari_operator(teks))

    def dispPrevious(self):
        self.index -= 1
        if self.index < 0:
            self.index = 0
        self.tampilkan()

    def dispNext(self):
        self.index += 1
        if self.index > len(self.records) - 1:
            self.index = len(self.records) - 1
        self.tampilkan()

    def tambah(self):
        q = QSqlQuery()
        q.exec("INSERT INTO kontak (nama, nomor_hp, operator) VALUES ('', NULL, '')")
        self.muat_data(pilih_id=q.lastInsertId())

    def simpan(self):
        if not self.records:
            return
        nama = self.input_nama.text().strip()
        hp = self.input_hp.text().strip()
        if not nama or not hp:
            QMessageBox.warning(self, "Peringatan", "Nama dan nomor HP harus diisi.")
            return
        id_ = self.records[self.index][0]
        q = QSqlQuery()
        q.prepare("UPDATE kontak SET nama = ?, nomor_hp = ?, operator = ? WHERE id = ?")
        q.addBindValue(nama)
        q.addBindValue(int(hp))
        q.addBindValue(cari_operator(hp))
        q.addBindValue(id_)
        q.exec()
        self.muat_data(pilih_id=id_)
