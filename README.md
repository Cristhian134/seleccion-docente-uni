# Proyecto Selección Docente – UNI

Sistema de gestión para el proceso de selección docente, implementado con Django y desplegado mediante Docker.

## Requisitos Previos

- Docker  
- Docker Compose  
- Python 3.10+ (opcional)

## Puesta en Marcha del Proyecto

### 1. Crear migraciones

```bash
docker compose -f local.yml run --rm app python manage.py makemigrations
```

### 2. Aplicar migraciones

Aplicar las migraciones a la base de datos PostgreSQL del entorno Docker:

```bash
docker compose -f local.yml run --rm app python manage.py migrate
```

### 3. Crear superusuario por defecto

```bash
docker compose -f local.yml run --rm app python manage.py create_superuser --defaults
```

### 4. Levantar el entorno

```bash
docker compose -f local.yml up
```

El sistema estará disponible en:

```
http://localhost:8000/
```

## Gestión de Usuarios

### Crear superusuario (valores por defecto)

```bash
python manage.py create_superuser --defaults
```

### Listar superusuarios

```bash
python manage.py list_superuser
```

### Eliminar superusuario

```bash
python manage.py delete_superuser <codigo>
```

## Credenciales por Defecto

| Campo      | Valor           |
|------------|-----------------|
| DNI        | 12345678        |
| Correo     | root@gmail.com  |
| Contraseña | root            |

## Comandos Útiles

### Apagar contenedores

```bash
docker compose -f local.yml down
```

### Ver logs de la aplicación

```bash
docker compose -f local.yml logs app
```
