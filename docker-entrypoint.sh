# docker-entrypoint.sh
#!/bin/sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ "$DJANGO_ENV" = "production" ]; then
  gunicorn matrimony.wsgi:application --bind 0.0.0.0:8000
else
  python manage.py runserver 0.0.0.0:8000
fi
