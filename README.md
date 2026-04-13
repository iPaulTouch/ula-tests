# ula-tests

Para ejecutar este código , los pasos serían:

Instalar el framework: pip install django

Iniciar el proyecto: django-admin startproject taller_crm

Ejecutar las migraciones para crear la base de datos MySQL/SQLite: python manage.py makemigrations y python manage.py migrate

Crear un usuario administrador (para el RNF1): python manage.py createsuperuser

Levantar el servidor: python manage.py runserver
