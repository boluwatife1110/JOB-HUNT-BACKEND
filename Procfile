web: python manage.py migrate && gunicorn myproject.wsgi
web: python manage.py collectstatic --noinput && python manage.py migrate && gunicorn myproject.wsgi