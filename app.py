from flask import Flask, url_for, request, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import SubmitField, TextField, StringField, TextAreaField
from wtforms.validators import DataRequired


from cryptography.fernet import Fernet



app = Flask(__name__)
app.config['SECRET_KEY'] = 'bismillah'
Bootstrap(app)



class MasukanPesan(FlaskForm):
    pesan = TextAreaField('Masukan Pesan', validators=[DataRequired()])
    submit = SubmitField('Enkripsi')

class DekripsiPesan(FlaskForm):
    cipher = TextAreaField('Masukan Cipher', validators=[DataRequired()])
    kunci = StringField('Masukan Kunci', validators = [DataRequired()])
    submit = SubmitField('Dekripsi')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/enkripsi', methods = ['POST', 'GET'])
def enkripsi():
    form = MasukanPesan()
    enkripsi = False
    hasil = {}
    if form.validate_on_submit():
        plain = bytes(form.pesan.data, 'utf-8')
        key = Fernet.generate_key()
        algoritma = Fernet(key)
        hasil = algoritma.encrypt(plain)
        hasil = {
            'plain_text' : form.pesan.data,
            'key' : str(key).split("'")[1],
            'hasil' : str(hasil).split("'")[1]
        }
        enkripsi = True

    return render_template('enkripsi.html', form = form, enkripsi = enkripsi, hasil = hasil)


@app.route('/dekripsi', methods = ['POST', 'GET'])
def dekripsi():
    form = DekripsiPesan()
    dekripsi = None
    hasil = {}
    if form.validate_on_submit():
        try:
            cipher = bytes(form.cipher.data, 'utf-8')
            kunci = bytes(form.kunci.data, 'utf-8')
            algoritma = Fernet(kunci)
            hasil = str(algoritma.decrypt(cipher)).split("'")[1]
            print(hasil)
            hasil = {
                'cipher' : cipher,
                'kunci' : kunci,
                'hasil' : hasil
            }
            dekripsi = True

        except:
            print('Token tidak sesuai!')
            dekripsi = False


    return render_template('dekripsi.html', form = form, dekripsi = dekripsi, hasil = hasil)



if __name__ == "__main__":
    app.run(debug= True)
