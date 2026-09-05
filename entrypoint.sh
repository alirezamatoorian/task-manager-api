#!/bin/sh

set -e

# for nginx unroot user with celery
[ -d /app/staticfiles ] && chown -R appuser:appuser /app/staticfiles
[ -d /app/media ] && chown -R appuser:appuser /app/media


# for nginx unroot user
#chown -R appuser:appuser /app/staticfiles /app/media

#for nginx unroot user with celery
#gosu appuser python manage.py migrate --noinput
#gosu appuser python manage.py collectstatic --noinput

if [ "$RUN_MIGRATIONS" = "true" ]; then
    gosu appuser python manage.py migrate --noinput
    gosu appuser python manage.py collectstatic --noinput
fi

#python manage.py migrate --noinput
#python manage.py collectstatic --noinput


#for unroot user with nginx
exec gosu appuser "$@"

#exec "$@"
