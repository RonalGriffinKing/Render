from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()

app=Flask(__name__)

@app.route('/')
def index():
    username=os.getenv('USERNAME')
    email=os.getenv('EMAIL')
    paddword=os.getenv('PASSWORD')
    print(username,email,paddword)
    return '<h1>Mi primera app deployada con render </h1>'

@app.route('/inicio')
def inicio():
   return render_template('inicio.html')


def status_404(error):
    return '<h1> Pagina no encontrada</h1>'



if __name__== '__main__':
    app.register_error_handler(404,status_404)
    app.run(debug=True)
