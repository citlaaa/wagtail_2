# Proyecto Wagtail – UNAM

## Descripción
Sistema web desarrollado con **Wagtail** para el desarrollo de nuestro servicio social en favor de la **Universidad Nacional Autónoma de México (UNAM)**.
El proyecto centraliza módulos necesarios para la gestión institucional, permitiendo mantener ordenados y accesibles los procesos y documentos internos.

## Objetivo
Facilitar la administración de documentos y procesos internos mediante una plataforma web modular, segura y mantenible.

---

## Autores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/citlaaa">
        <img src="https://github.com/citlaaa.png" width="100px;" alt=""/><br />
        <sub><b>Citlally Fernanda Suárez Juárez</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Tony0619-29">
        <img src="https://github.com/Tony0619-29.png" width="100px;" alt=""/><br />
        <sub><b>Antonio Medina Montoya</b></sub>
      </a>
    </td>
  </tr>
</table>

---

## Tecnologías Utilizadas

- **Python 3.11 o superior**
- **Django 5.2.8**
- **Wagtail 7.2**
- **HTML / CSS / Bootstrap**
- **MariaDB**
- Entorno virtual con `venv`
- Sistema operativo recomendado: Linux / Windows

---

## Módulos del Proyecto

El sistema está organizado en varias aplicaciones internas:

- **app_consejo** – Gestión de funciones y contenidos del consejo.
- **app_dictaminadora** – Administración de procesos de dictaminación y revisión.
- **app_estimulos** – Gestión de estímulos y documentos asociados.
- **home** – Página principal, vistas generales y elementos base del sitio.

---

## Instalación y Puesta en Marcha

Sigue estos pasos para levantar el proyecto en tu entorno local.

### 1. Clonar el repositorio
```bash
git clone [https://github.com/citlaaa/wagtail_2.git](https://github.com/citlaaa/wagtail_2.git)
cd wagtail_2
```
### 2. Crear y activar un entorno virtual
```bash
# Para macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Para Windows
python -m venv venv
venv\Scripts\activate
```
### 3. Configurar la base de datos MariaDB
Asegúrate de tener MariaDB instalado y ejecutándose.

 Accede a tu gestor de base de datos y ejecuta:
```SQL
CREATE DATABASE wagtail_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
Configurar credenciales: Verifica que tu archivo settings.py (o tus variables de entorno) coincidan con tu configuración local. 
Ejemplo básico:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "wagtail_db",
        "USER": "root",     # Cambiar por tu usuario
        "PASSWORD": "",     # Cambiar por tu contraseña
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {"charset": "utf8mb4"},
    }
}
```
### 4. Ejecutar Migraciones Iniciales
```bash
python manage.py migrate
```
### 5. Crear un superusuario
Para acceder al panel de administración de Wagtail
```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```
---
### Recomendaciones
Si necesitas modificar la estructura de la base de datos (modelos), sigue este flujo:
1. Crear migraciones (makemigrations): Si modificas algún archivo models.py, ejecuta este comando para generar los archivos de instrucciones (planos) de los cambios.
```bash
python manage.py makemigrations
```
Aplicar migraciones (migrate): Una vez creados los archivos de migración, impacta esos cambios en la base de datos real.
```bash
python manage.py migrate
```

