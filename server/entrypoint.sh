#!/bin/sh
# Sunday, 20 September, 2026 01:32:05 PM UTC
# AUTHOR: mevpd 
# DESC  : capstone ibm 
# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec "$@"
