# Configuración de Gmail para Envío de Correos

## Pasos para configurar Gmail SMTP

### 1. Activar Verificación en 2 Pasos en Google

1. Ve a [Cuenta de Google](https://myaccount.google.com/)
2. En el menú izquierdo, selecciona **"Seguridad"**
3. Busca la sección **"Cómo inicias sesión en Google"**
4. Haz clic en **"Verificación en 2 pasos"**
5. Sigue los pasos para activarla (si no está activada)

### 2. Generar Contraseña de Aplicación

1. Una vez activada la verificación en 2 pasos, regresa a **"Seguridad"**
2. Busca **"Contraseñas de aplicaciones"** (al final de la sección "Verificación en 2 pasos")
3. Haz clic en **"Contraseñas de aplicaciones"**
4. Selecciona:
   - **Aplicación:** Correo
   - **Dispositivo:** Otro (nombre personalizado) → escribe "Flask 2FA App"
5. Haz clic en **"Generar"**
6. **Copia la contraseña de 16 caracteres** (ejemplo: `abcd efgh ijkl mnop`)

### 3. Configurar en app.py

Edita el archivo `app.py` y actualiza:

```python
app.config['MAIL_USERNAME'] = 'tu_correo@gmail.com'        # Tu Gmail
app.config['MAIL_PASSWORD'] = 'abcd efgh ijkl mnop'        # Contraseña de aplicación (16 caracteres)
app.config['MAIL_DEFAULT_SENDER'] = 'tu_correo@gmail.com'  # El mismo correo
```

### 4. Notas Importantes

- ⚠️ **NO uses tu contraseña normal de Gmail** - usa la contraseña de aplicación
- ✅ La contraseña de aplicación tiene 16 caracteres con espacios
- ✅ Puedes revocar la contraseña en cualquier momento desde tu cuenta Google
- ✅ Cada aplicación debe tener su propia contraseña de aplicación

### 5. Alternativas a Gmail

Si prefieres usar otro servicio de correo:

#### Outlook/Hotmail
```python
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'tu_correo@outlook.com'
app.config['MAIL_PASSWORD'] = 'tu_contraseña'
```

#### Yahoo Mail
```python
app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'tu_correo@yahoo.com'
app.config['MAIL_PASSWORD'] = 'tu_contraseña_app'  # También requiere contraseña de app
```

### 6. Verificar Configuración

Para verificar que funciona correctamente:

1. Ejecuta la aplicación: `python app.py`
2. Registra un usuario con tu correo real
3. Inicia sesión
4. Revisa tu bandeja de entrada - deberías recibir el código

Si hay errores, revisa la consola donde ejecutaste `python app.py` - mostrará mensajes de error del envío de email.

### Troubleshooting

**Error: "Username and Password not accepted"**
- Verifica que estés usando la contraseña de aplicación, no tu contraseña normal
- Asegúrate de que la verificación en 2 pasos esté activada

**Error: "SMTPAuthenticationError"**
- Revisa que el correo y la contraseña sean correctos
- Prueba generar una nueva contraseña de aplicación

**No llega el correo**
- Revisa la carpeta de SPAM
- Verifica que el correo del destinatario sea correcto
- Revisa los logs en la consola de Python
