from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from connectdb import Database
app = Flask(__name__)

#koneksi ke database
app.secret_key = "customer_672019154"

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


users = []
users.append(User(id=1, username='teguh@gmail.com', password='1'))

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('customertampildata'))

        return redirect(url_for('login'))
        flash('password/userbane abda salah')

    return render_template('login.html')

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/admin')
def customertampildata():
    conn = Database('ksb-2022')
    datatampil = conn.select("SELECT * FROM hotelteguhr_672019154 ORDER BY ktp DESC")
    return render_template('admin.html', datapemesan=datatampil)

@app.route('/', methods=['POST'])
def customerinsert():
    conn = Database('ksb-2022')
    if request.method == 'POST':
        ktp = request.form['ktp']
        nama = request.form['nama']
        email = request.form['email']
        nomorhp = request.form['nomorhp']
        pesan = request.form['pesan']
        conn.execute("INSERT INTO hotelteguhr_672019154 (ktp,nama, email, nomorhp, pesan) VALUES ('{0}','{1}','{2}','{3}','{4}');".format(ktp,nama, email, nomorhp, pesan))
        flash('Insert Data sukses')
        return redirect(url_for('index'))

@app.route('/customerupdate', methods=['POST'])
def customerupdate():
    conn = Database('ksb-2022')
    if request.method == 'POST':
        ktp = request.form['ktp']
        nama = request.form['nama']
        email = request.form['email']
        nomorhp = request.form['nomorhp']
        pesan = request.form['pesan']
        conn.execute("UPDATE  hotelteguhr_672019154  SET  nama='{0}', email='{1}', nomorhp='{2}', pesan='{3}' WHERE ktp='{4}';".format(nama, email, nomorhp, pesan, ktp))

        flash("Data Berhasil di Update")
        return redirect(url_for('customertampildata'))

# delete data
@app.route('/customerhapus/<int:ktp>', methods=['POST', 'GET'])
def customerhapus(ktp):
    conn = Database('ksb-2022')
    conn.execute("DELETE FROM  hotelteguhr_672019154  WHERE ktp={0}".format(ktp))

    flash("data Berhasil di Hapus")
    return redirect(url_for('customertampildata'))

@app.route("/about")
def tentang():
    return render_template('about.html')

@app.route("/fasilitas")
def fasilitas():
    return render_template('fasilitas.html')

if __name__ == '__main__':
    app.run(debug=True)