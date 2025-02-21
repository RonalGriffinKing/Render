

from flask import Flask,render_template,jsonify,request,session
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash,check_password_hash
from flask_mail import Mail,Message

app=Flask(__name__)

#configuracion mail
app.config['MAIL_SERVER'] = 'smpt.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'PRUEBASDAW2021@gmail.com'
app.config['MAIL_PASSWORD'] = 'teht zjip gyfz jvvf'
app.config["MONGO_URI"] = "mongodb://localhost:27017/Examen"


mongo = PyMongo(app)
mail =Mail(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrarte')
def registrarte():
    return render_template('registrarte.html')

@app.route('/registrarteBD', methods=['POST'])
def registrarteBD():
            correo=request.form.get('correo')
            contra=request.form.get('contra')
            if correo and contra:
                hashed_password=generate_password_hash(contra)
                user={
                    'correo':correo,
                    'contra':hashed_password
                }
                mongo.db.usuario.insert_one(user)

                msg=Message(
                      subject=correo,
                      sender='PRUEBASDAW2021@gmail.com',
                      body='Registrado Con Exito'
                )
                
                return render_template('registrarte.html',mensaje='REGISTRO CON EXITO')
            else:
                return render_template('registrarte.html',mensaje='NO PUEDE ESTAR VACIO')

@app.route('/iniciar')
def iniciar():
    return render_template('iniciarsesion.html')

@app.route('/iniciarBD', methods=['POST'])
def iniciarBD():
            correo=request.form.get('correo')
            contra=request.form.get('contra')
            hashed_password=generate_password_hash(contra)
            comprobado=check_password_hash(hashed_password,contra)
            usuario=mongo.db.usuario.find_one({'correo':correo,'contra':comprobado})
            if usuario and correo and contra:
                session['user']=correo
                return render_template('enviarcorreo.html')
            else:
                return render_template('iniciarsesion.html',mensaje='LOGGIN SIN EXITO')

@app.route('/enviarcorreo')
def enviarcorreo():
      if 'user' not in session:
            return jsonify({'mensaje':'no puedes ingresar'})

if __name__=='__main__':
    app.run(debug=True)