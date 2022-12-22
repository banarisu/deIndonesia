Debug = False

import sqlite3
from newsapi.newsapi_client import NewsApiClient

from flask import *
from flask import Flask as f
from flask_mail import Mail, Message

# Start of Trying of Creating DB

'''
print("ketik exit di nama jika ingin keluar")
while x != "exit":
    x = input("Masukan Nama : ")
    if x == "exit":
        print("")
        pass

    else:
        z = input("Masukan id : ")
        try:
            cr.execute('INSERT INTO iden(id,nama) VALUES(?,?)', (z, x))
            z = ""
            x = ""
            pass
        except sqlite3.IntegrityError as zd:
            print("ERROR")
            print(zd)
            x = "exit"
            pass
        pass
'''
# End of Trying of Creating DB

app = f(__name__)
app.secret_key = "kelompok5"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

conn = cursor = None

def openDB():
    global conn, cur
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()

def closeDB():
    global conn, cur
    cur.close()
    conn.close()

@app.route('/')
def index():
    newsapi = NewsApiClient(api_key="867bf71d3e68444593a82e30d90df983")
    topheadlines = newsapi.get_everything(domains="detik.com", sort_by="publishedAt")
    articles = topheadlines['articles']
    judul1 = []
    judul2 = []
    deskripsi1 = []
    deskripsi2 = []
    gambar1 = []
    gambar2 = []
    #watashi maling dari bawah code nya YEHE
    for i in range(0, 5):
        artikel = articles[i]

        if i<2:
            judul1.append(artikel['title'])
            deskripsi1.append(artikel['description'])
            gambar1.append(artikel['urlToImage'])
            pass
        elif i>2:
            judul2.append(artikel['title'])
            deskripsi2.append(artikel['description'])
            gambar2.append(artikel['urlToImage'])
            pass

    con1 = zip(judul1, deskripsi1, gambar1)
    con2 = zip(judul2, deskripsi2, gambar2)
    return render_template("index.html" ,context1 = con1,context2=con2)

@app.route('/berita')
def berita():
    newsapi = NewsApiClient(api_key="867bf71d3e68444593a82e30d90df983")
    topheadlines = newsapi.get_everything(domains="detik.com", sort_by="publishedAt")

    articles = topheadlines['articles']

    judul = []
    deskripsi = []
    gambar = []
    linkBerita = []

    # Bebas pilih mau nampilin berapa berita, tinggal looping
    for i in range(0, 4):
        artikel = articles[i]
        judul.append(artikel['title'])
        deskripsi.append(artikel['description'])
        gambar.append(artikel['urlToImage'])
        linkBerita.append(artikel['url'])
    listberita = zip(judul, deskripsi, gambar, linkBerita)

    return render_template("berita.html", context = listberita)


@app.route('/profil')
def profil():
    return render_template("prof.html")


@app.route('/help', methods=['GET', 'POST'])
def help():
    if request.method == 'POST':
        # Kirim email ke user untuk konfirmasi
        username = "fenardimizu@gmail.com"
        password = "qviacfsgouhlxrzp"

        to = request.form['email']
        nama = request.form['nama']
        judulkeluhan = request.form['judul']
        isikeluhan = request.form['isi']

        subject = "Notifikasi Keluhan/Saran Anda Terhadap deIndonesia"
        message = "Kepada Bapak/Ibu "+nama+\
                  "\nTerima kasih telah menggunakan fitur bantuan pada website kami."+\
                  "\n\nKami ingin memberitahu bahwa keluhan/saran anda yang berjudul '"+request.form['judul']+\
                  "' telah kami terima."+\
                  "\nKami sangat menghargai setiap masukan positif yang membangun dan membantu kami menjadi lebih baik."+\
                  "\n\nSalam hangat dari kami\nDeIndonesia"
        app.config['MAIL_USERNAME'] = username
        app.config['MAIL_PASSWORD'] = password
        pesan = Message(subject, sender=username, recipients=[to])
        pesan.body = message
        try:
            mail = Mail(app)
            mail.connect()
            mail.send(pesan)
            openDB()
            cur.execute('INSERT INTO keluhan(k_nama, k_email, k_judul, k_isi) VALUES (?,?,?,?)', (nama,to,judulkeluhan,isikeluhan) )
            conn.commit()
            closeDB()
            flash('Terima Kasih')
            flash('Keluhan/Saran Anda Berhasil Terkirim! Silahkan cek email anda')
            return redirect(request.url)
        except:
            flash('Mohon Maaf')
            flash('Keluhan/Saran Anda Gagal Terkirim! Silahkan coba lagi')
            return redirect(request.url)
    return render_template("help.html")

if __name__ == "__main__":
    app.run(debug=Debug, host='0.0.0.0', port=5000)
    pass

"""
cara redirect nich : 

cari nama di atas kaya help

return redirect(url_for('help'))

@app.route('/')
def index():
    newsapi = NewsApiClient(api_key="867bf71d3e68444593a82e30d90df983")
    topheadlines = newsapi.get_everything(domains="detik.com", sort_by="publishedAt")
    articles = topheadlines['articles']
    judul1 = []
    judul2 = []
    deskripsi1 = []
    deskripsi2 = []
    gambar1 = []
    gambar2 = []
    #watashi maling dari bawah code nya YEHE
    for i in range(0, 5):
        artikel = articles[i]

        if i<2:
            judul1.append(artikel['title'])
            deskripsi1.append(artikel['description'])
            gambar1.append(artikel['urlToImage'])
            pass
        elif i>2:
            judul2.append(artikel['title'])
            deskripsi2.append(artikel['description'])
            gambar2.append(artikel['urlToImage'])
            pass

    con1 = zip(judul1, deskripsi1, gambar1)
    con2 = zip(judul2, deskripsi2, gambar2)
    return render_template("index.html" ,context1 = con1,context2=con2)


"""