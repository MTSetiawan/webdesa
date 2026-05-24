import os
import io
import base64
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, send_file, jsonify
)
from werkzeug.utils import secure_filename
from datetime import timedelta
import mysql.connector
from mysql.connector import pooling

# ==========================
# APP & CONFIG
# ==========================
app = Flask(__name__)
app.secret_key = 'rahasia_kecamatan'  # Ganti dengan string random kalau untuk produksi

# Folder Upload
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "static", "uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Koneksi Database MySQL
dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": "200522",
    "database": "db_kecamatan1"
}
    


connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **dbconfig
)

def get_db_connection():
    return connection_pool.get_connection()





# ==========================
# ROUTE UTAMA
# ==========================

@app.route('/')
def index():
    return redirect('/dashboard-public')

@app.route('/home')
def home():
    return render_template('admin/home.html')


# ==========================
# AUTH
# ==========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        akun = cursor.fetchone()
        cursor.close()

        if akun:
            session['admin_id'] = akun['id']
            session['admin_nama'] = akun['nama_lengkap']
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau Password salah!', 'danger')

            cursor.close()
            conn.close()


    return render_template('admin/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nama_lengkap = request.form['nama_lengkap']

        conn = get_db_connection()
        cursor = conn.cursor(
            "INSERT INTO admin (username, password, nama_lengkap) VALUES (%s, %s, %s)",
            (username, password, nama_lengkap)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Pendaftaran berhasil. Silakan login.')
        return redirect(url_for('login'))

    return render_template('admin/register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ==========================
# HALAMAN PROTEKSI LOGIN
# ==========================
@app.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        flash('Silakan login terlebih dahulu.')
        return redirect(url_for('login'))
    return render_template('admin/dashboard.html', nama=session['admin_nama'])


@app.route('/desa')
def desa():
    if 'admin_id' not in session:
        flash('Silakan login terlebih dahulu.')
        return redirect(url_for('login'))
    return render_template('admin/desa.html', nama=session['admin_nama'])


@app.route('/profil')
def profil():
    if 'admin_id' not in session:
        flash('Silakan login terlebih dahulu.')
        return redirect(url_for('login'))
    return render_template('admin/profil.html')


@app.route('/geografis')
def geografis():
    if 'admin_id' not in session:
        flash('Silakan login terlebih dahulu.')
        return redirect(url_for('login'))
    return render_template('admin/geografis.html', nama=session['admin_nama'])


@app.route('/sarpras')
def sarpras():
    if 'admin_id' not in session:
        flash('Silakan login terlebih dahulu.')
        return redirect(url_for('login'))
    return render_template('admin/sarpras.html', nama=session['admin_nama'])


@app.route('/pelayanan')
def pelayanan():
    if 'admin_id' not in session:
        flash('Silakan login terlebih dahulu.')
        return redirect(url_for('login'))
    return render_template('admin/pelayanan.html', nama=session['admin_nama'])


@app.route('/datapegawai')
def data_pegawai():
    if 'admin_id' not in session:
        flash('Silakan login terlebih dahulu.')
        return redirect(url_for('login'))
    return render_template('admin/datapegawai.html', nama=session['admin_nama'])


@app.route('/struktur')
def struktur():
    if 'admin_id' not in session:
        flash('Silakan login terlebih dahulu.')
        return redirect(url_for('login'))
    return render_template('admin/struktur.html', nama=session['admin_nama'])


# ==========================
# HALAMAN DESA DETAIL
# ==========================
@app.route('/desa/<nama>')
def detail_desa(nama):
    return render_template('admin/desa_detail.html', nama=nama.capitalize())

@app.route('/desa/bangsri')
def bangsri():
    return render_template('admin/bangsri.html')

@app.route('/desa/sembung')
def sembung():
    return render_template('admin/sembung.html')

@app.route('/desa/brumbung')
def brumbung():
    return render_template('admin/brumbung.html')

@app.route('/desa/jambe')
def jambe():
    return render_template('admin/jambe.html')


# ==========================
# HALAMAN LAYANAN PUBLIK
# ==========================
@app.route('/pendudukan') 
def pendudukan():
    return render_template('admin/pendudukan.html')

@app.route('/surat') 
def surat():
    return render_template('admin/surat.html')

@app.route('/sosial') 
def sosial():
    return render_template('admin/sosial.html')

@app.route('/pertanahan') 
def pertanahan():
    return render_template('admin/pertanahan.html')

@app.route('/perizinan') 
def perizinan():
    return render_template('admin/perizinan.html')

@app.route('/kesejahteraan') 
def kesejahteraan():
    return render_template('admin/kesejahteraan.html')

@app.route('/pengaduan') 
def pengaduan():
    return render_template('admin/pengaduan.html')

@app.route('/informasi') 
def informasi():
    return render_template('admin/informasi.html')

@app.route('/tempatterkenal') 
def tempatterkenal():
    return render_template('admin/tempatterkenal.html')

@app.route('/visimisi')
def visi_misi():
    return render_template('admin/visimisi.html')



# ==========================
# BERITA
# ==========================
@app.route("/kelola_berita")
def kelola_berita():
    return render_template("admin/kelola_berita.html")


@app.route("/upload_berita", methods=["POST"])
def upload_berita():
    judul = request.form.get("judul")
    isi = request.form.get("isi")
    gambar = request.files.get("gambar")
    img_data = gambar.read() if (gambar and gambar.filename) else None

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO berita (judul, isi, gambar) VALUES (%s, %s, %s)"
    cursor.execute(sql, (judul, isi, img_data))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Berita berhasil diunggah!", "success")
    return redirect(url_for("berita"))


@app.route("/berita")
def berita():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, judul, tanggal, gambar FROM berita ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    data = []
    for id, judul, tanggal, gambar_blob in rows:
        if gambar_blob:
            gambar_base64 = base64.b64encode(gambar_blob).decode("utf-8")
            gambar_src = f"data:image/jpeg;base64,{gambar_base64}"
        else:
            gambar_src = None
        data.append((id, judul, tanggal, gambar_src))

    return render_template("admin/berita.html", data=data)


@app.route("/edit_berita/<int:id>", methods=["GET", "POST"])
def edit_berita(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == "POST":
        judul = request.form["judul"]
        isi = request.form["isi"]
        cursor.execute("UPDATE berita SET judul=%s, isi=%s WHERE id=%s", (judul, isi, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Berita berhasil diperbarui!", "success")
        return redirect(url_for("berita"))

    cursor.execute("SELECT id, judul, isi FROM berita WHERE id=%s", (id,))
    berita = cursor.fetchone()
    cursor.close()
    return render_template("admin/kelola_berita.html", berita=berita)


@app.route("/hapus_berita/<int:id>")
def hapus_berita(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM berita WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Berita berhasil dihapus!", "danger")
    return redirect(url_for("berita"))


# ==========================
# GALERI
# ==========================
@app.route("/upload_foto", methods=["POST"])
def upload_foto():
    from datetime import datetime

    judul = request.form["judul"]
    file = request.files["gambar"]

    if file:
        foto = file.read()
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO galeri (judul, foto, tanggal, status) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (judul, foto, datetime.today().date(), 1))
        conn.commit()
        cursor.close()
        conn.close()

    flash("Foto berhasil diupload!", "success")
    return redirect(url_for("galeri"))



@app.route('/gambar/<int:id>')
def gambar(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT foto FROM galeri WHERE id = %s", (id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result and result[0]:
        from flask import Response
        return Response(result[0], mimetype='image/jpeg')
    else:
        return "", 404
    



@app.route("/galeri")
def galeri():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM galeri ORDER BY id DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("admin/galeri.html", data=data)




@app.route("/edit_foto/<int:id>", methods=["GET", "POST"])
def edit_foto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == "POST":
        judul = request.form.get("judul")
        gambar = request.files.get("gambar")

        if gambar and gambar.filename:
            filename = secure_filename(gambar.filename)
            gambar.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            sql = "UPDATE galeri SET judul=%s, gambar=%s WHERE id=%s"
            val = (judul, filename, id)
        else:
            sql = "UPDATE galeri SET judul=%s WHERE id=%s"
            val = (judul, id)

        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()

        flash("Foto berhasil diperbarui!", "success")
        return redirect(url_for("galeri"))
    
    else:
        cursor.execute("SELECT * FROM galeri WHERE id=%s", (id,))
        foto = cursor.fetchone()
        cursor.close()
        conn.close()

        if not foto:
            flash("Foto tidak ditemukan.", "danger")
            return redirect(url_for("galeri"))

        # Kamu gak punya edit_foto.html, jadi balik ke galeri aja
        return redirect(url_for("galeri"))

    


@app.route("/hapus_foto/<int:id>")
def hapus_foto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM galeri WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Foto berhasil dihapus!", "success")
    return redirect(url_for("galeri"))


# ==========================
# SEARCH
# ==========================



@app.route('/dashboard-public')
def dashboard_public():
    return render_template('publik/dashboard-public.html')


@app.route('/geografis_public')
def geografis_public():
        return render_template('publik/geografis-public.html')

@app.route('/sarpras_public')
def sarpras_public():
        return render_template('publik/sarpras-public.html')

@app.route('/tempatterkenal_public')
def tempatterkenal_public():
        return render_template('publik/tempatterkenal-public.html')

@app.route('/desa-public')
def desa_public():
        return render_template('publik/desa-public.html')

@app.route('/desa-public/bangsri')
def bangsri_public():
    return render_template('publik/bangsri-public.html')

@app.route('/desa-public/jambe')
def jambe_public():
    return render_template('publik/jambe-public.html')

@app.route('/desa-public/brumbung')
def brumbung_public():
    return render_template('publik/brumbung-public.html')

@app.route('/desa-public/sembung')
def sembung_public():
    return render_template('publik/sembung-public.html')


@app.route('/surat-public')
def surat_public():
        return render_template('publik/surat-public.html')

@app.route('/pertanahan-public')
def pertanahan_public():
        return render_template('publik/pertanahan-public.html')

@app.route('/informasi-public')
def informasi_public():
        return render_template('publik/informasi-public.html')

@app.route('/keramaian-public')
def keramaian_public():
        return render_template('publik/keramaian-public.html')

@app.route('/pendudukan-public')
def pendudukan_public():
        return render_template('publik/pendudukan-public.html')

@app.route('/kesejahteraan-public')
def kesejahteraan_public():
        return render_template('publik/kesejahteraan-public.html')

@app.route('/pengaduan-public')
def pengaduan_public():
        return render_template('publik/pengaduan-public.html')

@app.route('/perizinan-public')
def perizinan_public():
        return render_template('publik/perizinan-public.html')

@app.route('/sosial-public')
def sosial_public():
        return render_template('publik/sosial-public.html')

@app.route('/nama-public')
def nama_public():
        return render_template('publik/nama-public.html')

@app.route('/usaha-public')
def usaha_public():
        return render_template('publik/usaha-public.html')

@app.route('/struktur-public')
def struktur_public():
        return render_template('publik/struktur-public.html')

@app.route("/berita-public")
def berita_public():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, judul, isi, gambar FROM berita ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    berita_list = []
    for row in rows:
        id, judul, isi, gambar_blob = row
        gambar_base64 = None
        if gambar_blob:
            gambar_base64 = base64.b64encode(gambar_blob).decode("utf-8")
        berita_list.append({
            "id": id,
            "judul": judul,
            "isi": isi,
            "gambar": gambar_base64
        })

    # render daftar berita publik
    return render_template("publik/berita-public.html", berita_list=berita_list)

@app.route('/berita/<int:id>')
def detail_berita_public(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, judul, isi, tanggal, gambar FROM berita WHERE id = %s", (id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        id, judul, isi, tanggal, gambar_blob = row

        if tanggal:
           tanggal = tanggal + timedelta(hours=7)

        # Konversi gambar blob ke base64 agar bisa ditampilkan di HTML
        gambar_src = None
        if gambar_blob:
            gambar_base64 = base64.b64encode(gambar_blob).decode("utf-8")
            gambar_src = f"data:image/jpeg;base64,{gambar_base64}"

        berita = {
            "id": id,
            "judul": judul,
            "isi": isi,
            "tanggal": tanggal,
            "gambar": gambar_src
        }

        return render_template('publik/detail-berita-public.html', berita=berita)
    else:
        flash("Berita tidak ditemukan!", "danger")
        return redirect(url_for("berita_public"))
    
@app.route('/galeri-public')
def galeri_public():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Ambil semua gambar aktif
    cursor.execute("SELECT id, judul, tanggal FROM galeri WHERE status=1 ORDER BY id DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("publik/galeri-public.html", data=data)

@app.route('/visimisi_public')
def visimisi_public():
    return render_template('publik/visimisi-public.html')

@app.route('/datapegawai-public')
def datapegawai_public():
    return render_template('publik/datapegawai-public.html')

















# ==========================
# MAIN
# ==========================
if __name__ == '__main__':
    app.run(debug=True, port=5002)



