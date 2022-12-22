# dipisah dari file utama biar tidak pusying

import sqlite3

conn = sqlite3.connect('db.db')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS berita (
    b_id INTEGER PRIMARY KEY AUTOINCREMENT,
    b_judul TEXT,
    b_gambar BLOB,
    b_deskripsi TEXT
    );
    ''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS keluhan(
    k_id INTEGER PRIMARY KEY AUTOINCREMENT,
    k_nama TEXT,
    k_email TEXT,
    k_judul TEXT,
    k_isi TEXT
    );
    ''')

conn.commit()
cur.close()
conn.close()