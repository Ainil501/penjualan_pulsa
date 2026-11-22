import sqlite3

def buat_database():
    conn = sqlite3.connect("penjualan_pulsa.sqlite")
    cursor = conn.cursor()

    pass

    conn.commit()
    conn.close()
