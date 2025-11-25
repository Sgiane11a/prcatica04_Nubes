from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import pyotp
import qrcode
import io
import base64
import os

app = Flask(__name__)
app.secret_key = 'supersecreto'

# CONFIGURACIÓN DE BASE DE DATOS (Recuerda cambiar el ENDPOINT)
# Formato: postgresql://usuario:contraseña@ENDPOINT:5432/postgres
# EJEMPLO:
db_user = "postgres"
db_pass = "aL388TEC2955"
db_host = "lab-bd.c9kyyo2w0xe5.us-east-2.rds.amazonaws.com" # <--- CAMBIA ESTO POR TU ENDPOINT DEL PASO 1
db_name = "postgres"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    mfa_secret = db.Column(db.String(32), nullable=False)

# Crear tablas al iniciar (si no existen)
with app.app_context():
    db.create_all()

# HTML Básico embebido para no crear más archivos
html_template = """
<!DOCTYPE html>
<html>
<head><title>Lab Cloud 2FA</title></head>
<body>
    <h2>Sistema Seguro Lab 4</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}<ul style="color:red">{% for message in messages %}<li>{{ message }}</li>{% endfor %}</ul>{% endif %}
    {% endwith %}
    
    {% if session.get('user_id') %}
        <p>Bienvenido! Estás autenticado.</p>
        <a href="/logout">Cerrar Sesión</a>
    {% else %}
        <h3>Registro</h3>
        <form action="/register" method="post">
            User: <input type="text" name="username"> Pass: <input type="password" name="password">
            <input type="submit" value="Registrar">
        </form>
        <h3>Login</h3>
        <form action="/login" method="post">
            User: <input type="text" name="username"> Pass: <input type="password" name="password">
            <input type="submit" value="Entrar">
        </form>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    # Generar secreto para Google Authenticator
    secret = pyotp.random_base32()
    new_user = User(username=username, password=password, mfa_secret=secret)
    try:
        db.session.add(new_user)
        db.session.commit()
        return f"Usuario creado. <br> ESCANEA ESTO EN GOOGLE AUTHENTICATOR: <br> <img src='{get_qr(secret, username)}'> <br> <a href='/'>Volver</a>"
    except:
        return "Error: El usuario ya existe."

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['pre_2fa_user_id'] = user.id
        return redirect(url_for('verify_2fa'))
    return "Usuario o contraseña incorrectos"

@app.route('/2fa', methods=['GET', 'POST'])
def verify_2fa():
    if request.method == 'POST':
        user_id = session.get('pre_2fa_user_id')
        user = User.query.get(user_id)
        token = request.form['token']
        totp = pyotp.TOTP(user.mfa_secret)
        if totp.verify(token):
            session['user_id'] = user.id
            session.pop('pre_2fa_user_id', None)
            return "<h1>ÉXITO: Autenticación de 2 Pasos Correcta.</h1> <a href='/'>Ir al inicio</a>"
        else:
            return "Código incorrecto. Intente de nuevo."
    
    return """
    <form method="post">
        Ingrese código de Google Authenticator: <input type="text" name="token">
        <input type="submit" value="Verificar">
    </form>
    """

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def get_qr(secret, username):
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="TecsupLab")
    img = qrcode.make(uri)
    buffered = io.BytesIO()
    img.save(buffered)
    return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()

if __name__ == '__main__':
    # LEVANTAR EN PUERTO 3000
    app.run(host='0.0.0.0', port=3000)