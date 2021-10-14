release: python manage.py migrate
web: gunicorn -w 1 --access-logfile=- --timeout=120 hello_music.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A hello_music worker -l info
beat: celery -A hello_music beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
