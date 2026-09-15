"""Configuración centralizada de la Tarea 2: conexión a la base de datos,
carpeta de subida de archivos y límites de validación compartidos entre
`app.py` y `validaciones.py`.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Credenciales de base de datos indicadas en el enunciado de la Tarea 2.
# Se puede sobreescribir con la variable de entorno DATABASE_URL (por ejemplo
# para pruebas locales con SQLite) sin modificar el valor por defecto exigido.
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2",
)

SECRET_KEY = os.environ.get("SECRET_KEY", "oda-tarea2-clave-de-desarrollo")

# Archivos adjuntos de un avistamiento (fotos/videos).
CARPETA_SUBIDAS = os.path.join(BASE_DIR, "static", "uploads")
EXTENSIONES_PERMITIDAS = {"jpg", "jpeg", "png", "mp4"}
TIPOS_MIME_PERMITIDOS = {
    "image/jpeg",
    "image/png",
    "video/mp4",
}
TAMANO_MAXIMO_ARCHIVO = 5 * 1024 * 1024  # 5 MB por archivo, igual que en la Tarea 1

# Flask usa esta cota para rechazar de inmediato una petición demasiado
# pesada (protege contra adjuntar muchos archivos grandes a la vez).
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB por request completa

AVISTAMIENTOS_POR_PAGINA = 5
