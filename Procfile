web: gunicorn polls_api.wsgi --log-file -
release: python manage.py migrate; python manage.py regenarateurls
