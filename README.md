# transportal
Transportal

1. Set Conda environment
```
    conda env create -f environment.yml
```

2. To migrate table in Django, type in these new commands
```
    python manage.py makemigrations
    python manage.py migrate --run-syncdb
```

3. Run the application: python manage.py runserver 0.0.0.0:8123
