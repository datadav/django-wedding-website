#!/bin/bash

export DJANGO_SUPERUSER_PASSWORD=changeme
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@example.com
python manage.py collectstatic --noinput

# i commit my migration files to git so i dont need to run it on server
# ./manage.py makemigrations app_name
python manage.py migrate

# Create the superuser

python manage.py createsuperuser --noinput

/usr/sbin/nginx -g 'daemon off;' &

gunicorn bigday.wsgi --bind 0.0.0.0:8000