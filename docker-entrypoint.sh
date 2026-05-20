#!/bin/bash
set -e

echo "Waiting for MySQL to be ready..."
until python -c "
import MySQLdb
import os
try:
    MySQLdb.connect(
        host=os.environ.get('MYSQL_HOST','db'),
        port=int(os.environ.get('MYSQL_PORT','3306')),
        user=os.environ.get('MYSQL_USER','isim_user'),
        passwd=os.environ.get('MYSQL_PASSWORD','isim_password'),
        db=os.environ.get('MYSQL_DATABASE','isim_website')
    )
    print('MySQL ready!')
except Exception as e:
    print(f'Waiting... {e}')
    exit(1)
"; do
    sleep 2
done

echo "Running database migrations..."
flask db upgrade 2>/dev/null || flask create-tables

echo "Seeding initial admin user..."
flask seed 2>/dev/null || true

echo "Starting Flask application..."
exec gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 run:app
