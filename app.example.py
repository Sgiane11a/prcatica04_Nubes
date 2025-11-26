from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import pyotp
import qrcode
import io
import base64
import os
import random
import string

# Intentar cargar .env si existe (para desarrollo local)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # En producción (AWS) puede no estar instalado

app = Flask(__name__)
app.secret_key = 'supersecreto'

# CONFIGURACIÓN DE EMAIL (Gmail SMTP)
# Usa variables de entorno si existen (.env local), sino usa valores por defecto
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'TU_CORREO@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'xxxx xxxx xxxx xxxx')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'TU_CORREO@gmail.com')

mail = Mail(app)

# CONFIGURACIÓN DE BASE DE DATOS (AWS RDS PostgreSQL)
# Usa variables de entorno si existen (.env local), sino usa valores por defecto
db_user = os.getenv('DB_USER', 'postgres')
db_pass = os.getenv('DB_PASSWORD', 'TU_PASSWORD_DB')
db_host = os.getenv('DB_HOST', 'tu-endpoint.rds.amazonaws.com')
db_name = os.getenv('DB_NAME', 'postgres')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    mfa_secret = db.Column(db.String(32), nullable=False)

# Crear tablas al iniciar (si no existen)
# IMPORTANTE: db.drop_all() eliminará TODOS los datos existentes
# Usa esto solo en desarrollo. Para producción, usa migraciones (Flask-Migrate)
with app.app_context():
    db.drop_all()  # Elimina todas las tablas (¡CUIDADO! Borra datos)
    db.create_all()  # Recrea las tablas con la nueva estructura
    print("✅ Base de datos actualizada con el campo 'email'")

# HTML moved to templates/ to improve UI while preserving logic

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    # Generar secreto para Google Authenticator
    secret = pyotp.random_base32()
    new_user = User(username=username, email=email, password=password, mfa_secret=secret)
    try:
        db.session.add(new_user)
        db.session.commit()
        return render_template('registered.html', qr=get_qr(secret, username), username=username)
    except:
        return render_template('register.html', error='Error: El usuario ya existe.')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        # Generar código de 6 dígitos y enviarlo por email
        verification_code = ''.join(random.choices(string.digits, k=6))
        session['pre_2fa_user_id'] = user.id
        session['email_verification_code'] = verification_code
        
        # Enviar código por correo
        send_verification_email(user.email, verification_code, user.username)
        
        return redirect(url_for('verify_2fa'))
    return render_template('login.html', error='Usuario o contraseña incorrectos')

@app.route('/2fa', methods=['GET', 'POST'])
def verify_2fa():
    if request.method == 'POST':
        user_id = session.get('pre_2fa_user_id')
        user = User.query.get(user_id)
        token = request.form['token']
        
        # Verificar código de email o Google Authenticator
        email_code = session.get('email_verification_code')
        totp = pyotp.TOTP(user.mfa_secret)
        
        # Aceptar código de email o de Google Authenticator
        if (email_code and token == email_code) or totp.verify(token):
            session['user_id'] = user.id
            session.pop('pre_2fa_user_id', None)
            session.pop('email_verification_code', None)
            return render_template('success.html')
        else:
            return render_template('verify_2fa.html', error='Código incorrecto. Intente de nuevo.', user_email=user.email)

    # Obtener email del usuario para mostrarlo en la página
    user_id = session.get('pre_2fa_user_id')
    user = User.query.get(user_id) if user_id else None
    user_email = user.email if user else None
    return render_template('verify_2fa.html', user_email=user_email)

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

def send_verification_email(recipient_email, code, username):
    """Envía el código de verificación 2FA por correo electrónico"""
    try:
        msg = Message(
            subject='Código de Verificación 2FA - TecsupLab',
            recipients=[recipient_email]
        )
        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .code {{ font-size: 32px; font-weight: bold; color: #667eea; text-align: center; letter-spacing: 5px; padding: 20px; background: #f0f0f0; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🔐 Código de Verificación 2FA</h2>
                </div>
                <p>Hola <strong>{username}</strong>,</p>
                <p>Tu código de verificación de dos pasos es:</p>
                <div class="code">{code}</div>
                <p>Este código es válido por los próximos <strong>10 minutos</strong>.</p>
                <p>Si no solicitaste este código, ignora este mensaje.</p>
                <div class="footer">
                    <p>TecsupLab - Sistema de Autenticación Segura</p>
                    <p>© 2025 Tecsup. Todos los derechos reservados.</p>
                </div>
            </div>
        </body>
        </html>
        """
        mail.send(msg)
        print(f"✅ Código enviado a {recipient_email}: {code}")
    except Exception as e:
        print(f"❌ Error al enviar email: {str(e)}")
        # En caso de error, el usuario aún puede usar Google Authenticator

if __name__ == '__main__':
    # LEVANTAR EN PUERTO 3000
    app.run(host='0.0.0.0', port=3000)
