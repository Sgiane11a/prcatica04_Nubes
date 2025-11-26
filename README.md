# Práctica 4 - Sistema de Autenticación 2FA
## Soluciones en la Nube - Tecsup

### 👤 Datos del Estudiante
- **Apellidos:** Cordova Apolinario
- **Nombre:** Steyci Gianella
- **Fecha:** 25/02/2025
- **Sección:** A

---

## 📋 Descripción del Proyecto

Sistema de autenticación web con verificación de dos pasos (2FA) utilizando Google Authenticator. La aplicación está desarrollada con Flask, utiliza PostgreSQL en AWS RDS y está containerizada con Docker.

### ✨ Características Principales

- ✅ Registro de usuarios con generación de QR para 2FA
- ✅ **Doble verificación 2FA: Email + Google Authenticator**
- ✅ Envío automático de código de verificación por correo electrónico
- ✅ Inicio de sesión seguro con contraseña
- ✅ Verificación de segundo factor flexible (email o app)
- ✅ Base de datos PostgreSQL en AWS RDS
- ✅ Interfaz moderna y responsive con Bootstrap 5
- ✅ Despliegue con Docker y Docker Compose
- ✅ Infraestructura desplegada en AWS con CloudFormation

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Flask (Python 3.11)
- **Base de Datos:** PostgreSQL (AWS RDS)
- **Autenticación 2FA:** PyOTP + QRCode
- **Frontend:** HTML5, CSS3, Bootstrap 5, Font Awesome
- **Containerización:** Docker + Docker Compose
- **Infraestructura como Código:** AWS CloudFormation
- **Cloud Provider:** Amazon Web Services (AWS)

---

## 📦 Requisitos Previos

- Python 3.11+
- Docker y Docker Compose
- Cuenta de AWS con RDS configurado
- Google Authenticator (app móvil)

---

## 🚀 Instalación y Ejecución

### Opción 1: Ejecución con Docker (Recomendado)

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Sgiane11a/prcatica04_Nubes.git
   cd practica4
   ```

2. **Configurar variables de entorno:**
   - Copiar el archivo de ejemplo:
   ```bash
   # Windows (PowerShell)
   Copy-Item .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```
   
   - Editar el archivo `.env` y completar con tus credenciales:
   ```env
   MAIL_USERNAME=tu_correo@gmail.com
   MAIL_PASSWORD=xxxx xxxx xxxx xxxx
   DB_USER=postgres
   DB_PASSWORD=tu_contraseña_db
   DB_HOST=tu-endpoint.rds.amazonaws.com
   DB_NAME=postgres
   ```

3. **Configurar Gmail para envío de correos:**
   - Ir a tu [Cuenta de Google](https://myaccount.google.com/)
   - Activar **Verificación en 2 pasos**
   - Generar una **Contraseña de aplicación** en: Seguridad → Verificación en 2 pasos → Contraseñas de aplicaciones
   - Usar esa contraseña en el archivo `.env` (no tu contraseña normal)
   
   Ver **CONFIGURACION_EMAIL.md** para instrucciones detalladas.

4. **Construir y ejecutar con Docker Compose:**
   ```bash
   docker-compose up --build
   ```

5. **Acceder a la aplicación:**
   - Abrir el navegador en: `http://localhost:3000`

### Opción 2: Ejecución Local (Sin Docker)

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Sgiane11a/prcatica04_Nubes.git
   cd practica4
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   - Copiar `.env.example` a `.env`
   - Completar con tus credenciales (ver paso 2 de Opción 1)

5. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```

6. **Acceder a la aplicación:**
   - Abrir el navegador en: `http://localhost:3000`

---

## 📱 Guía de Uso

### 1. Registro de Usuario
1. Acceder a la página principal y hacer clic en **"Registrarse"**
2. Completar el formulario con:
   - Usuario
   - **Correo electrónico** (para recibir códigos de verificación)
   - Contraseña
3. **Escanear el código QR** generado con Google Authenticator (opcional pero recomendado)
4. Guardar el código QR para futuras autenticaciones

### 2. Inicio de Sesión
1. Hacer clic en **"Iniciar Sesión"**
2. Ingresar usuario y contraseña
3. **Revisar tu correo electrónico** - recibirás un código de 6 dígitos
4. En la pantalla de verificación 2FA, ingresar:
   - **El código recibido por email**, O
   - **El código de Google Authenticator** (si lo configuraste)
5. ¡Listo! Acceso concedido

### 3. Cerrar Sesión
- Hacer clic en **"Cerrar Sesión"** en la barra de navegación

---

## 📁 Estructura del Proyecto

```
practica4/
├── app.py                      # Aplicación Flask principal
├── Dockerfile                  # Configuración de Docker
├── docker-compose.yml          # Orquestación de contenedores
├── infraestructura.yaml        # CloudFormation template
├── requirements.txt            # Dependencias de Python
├── README.md                   # Documentación
├── templates/                  # Plantillas HTML
│   ├── base.html              # Template base
│   ├── home.html              # Página principal
│   ├── register.html          # Formulario de registro
│   ├── login.html             # Formulario de login
│   ├── registered.html        # Página con QR code
│   ├── verify_2fa.html        # Verificación 2FA
│   └── success.html           # Página de éxito
└── static/
    └── css/
        └── style.css          # Estilos personalizados
```

---

## 🔧 Configuración de AWS

### Base de Datos RDS (PostgreSQL)
- **Motor:** PostgreSQL
- **Versión:** 13+
- **Instancia:** db.t3.micro (o superior)
- **Puerto:** 5432
- **Acceso público:** Habilitado
- **Security Group:** Permitir puerto 5432 desde tu IP/EC2

### EC2 Instance (CloudFormation)
- **AMI:** Ubuntu 20.04
- **Security Group:** Puerto 3000 abierto
- **Instalación de Docker:** Incluida en UserData

---

## 🐳 Docker

### Dockerfile
El Dockerfile está configurado para:
- Usar imagen base de Python 3.11
- Instalar todas las dependencias
- Exponer el puerto 3000
- Ejecutar la aplicación Flask

### Docker Compose
Configura:
- Servicio web en puerto 3000
- Variables de entorno
- Volúmenes para persistencia

---

## 🔐 Seguridad

- ✅ Autenticación de dos factores obligatoria
- ✅ Secretos TOTP únicos por usuario
- ✅ Sesiones seguras con Flask sessions
- ✅ Base de datos en AWS RDS con acceso controlado

---

## 🎥 Video Demostración

**Link del video:** [[Video en Drive]](https://drive.google.com/file/d/15DG46iqP6_hoUUx5GL9BgPxBzDAw7tiR/view?usp=sharing)
**Link del video en YouTube:** [[Video en YouTube]](https://youtu.be/F-ooty8oy5o)


*(Video de máximo 5 minutos mostrando todo el funcionamiento)*

---

## 👨‍💻 Autor

**Steyci Gianella Cordova Apolinario**  
Tecsup - Soluciones en la Nube  
Sección A - 2025

