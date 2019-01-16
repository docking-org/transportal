# transportal
Transportal

Dependencies:

Python2.7
Django 1.11.18
Django==1.11.18
mod-wsgi==4.6.5
numpy==1.16.0

1. Set Virtualenv: virtualenv venv

2. Install modules: pip install -r requirements.txt

3. To migrate table in Django 1.11, type in these new commands
python manage.py makemigrations
python manage.py migrate --run-syncdb

4. Run the application: python manage.py runserver