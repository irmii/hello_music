release: python manage.py migrate --noinput
web: gunicorn -w 1 --access-logfile=- --timeout=120 hello_music.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A hello_music worker -l info
beat: celery beat -A hello_music -l info
