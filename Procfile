release: python manage.py migrate --noinput
web: gunicorn -w 1 --access-logfile=- --timeout=120 hello_music.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A hello_music worker -l info
beat: celery -A hello_music beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
