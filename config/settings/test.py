from .base import *
import sys


SECRET_KEY = "test-secret-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]


# Base de datos en memoria para acelerar la ejecución de pruebas
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_db",
        "USER": "test_user",
        "PASSWORD": "test_pass",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

# Hashing rápido para tests
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


# Backend de correo en memoria
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


# Simplificar la configuración de logging durante pruebas
LOGURU_LOGGING = {
    "handlers": [
        {"sink": sys.stderr, "level": "INFO"},
    ],
}
logger.configure(**LOGURU_LOGGING)
