import sqlite3

def buat_database():
    conn = sqlite3.connect("penjualan_pulsa.sqlite")
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    # Tabel pelanggan
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pelanggan (
            id_pelanggan INTEGER PRIMARY KEY AUTOINCREMENT,
            nama         TEXT NOT NULL,
            nomor_hp     TEXT NOT NULL,
            operator     TEXT NOT NULL
        )
    """)

    # Tabel paket
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paket (
            id_paket    INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_paket  TEXT NOT NULL,
            nominal     INTEGER NOT NULL,
            harga       INTEGER NOT NULL
        )
    """)

    # Tabel transaksi
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id_transaksi INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal      TEXT NOT NULL,
            id_pelanggan INTEGER NOT NULL,
            metode_bayar TEXT NOT NULL,
            status       TEXT NOT NULL,
            FOREIGN KEY (id_pelanggan) REFERENCES pelanggan(id_pelanggan)
        )
    """)

    # Tabel detail
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detail (
            id_detail    INTEGER PRIMARY KEY AUTOINCREMENT,
            id_transaksi INTEGER NOT NULL,
            id_paket     INTEGER NOT NULL,
            harga        INTEGER NOT NULL,
            FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi),
            FOREIGN KEY (id_paket)     REFERENCES paket(id_paket)
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    buat_database()
    print("Database berhasil dibuat.")
