docker compose -f local.yml up --build -d --remove-orphans

# Usuarios
## Superusuarios

python manage.py create_superuser --defaults

python manage.py list_superuser

python manage.py delete_superuser <codigo>

dni: 12345678
correo: root@gmail.com
contraseña: root