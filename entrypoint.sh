#!/bin/sh

set -e

#chown -R appuser:appuser /app/staticfiles /app/media


python manage.py migrate --noinput
python manage.py collectstatic --noinput

#exec gosu appuser "$@"

exec "$@"
