# Shop-Django
 

Technologies used:

- Django
- django-autofixtures 
- Materialize CSS 

## How to use this project

This project uses Python 3 and also pip to manage dependencies.

- Clone the repository using Git.
- `pip install -r requirements.txt`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`

You can then access the app at http://127.0.0.1:8080

## Generating test data

Run the following command to generate some test data. You can alter the numeric values for more or less data.

```
python manage.py loadtestdata product_manager.Category:3 product_manager.Product:20
```

## Generating a superuser

Run the following command to generate a superuser. You can then log in at /admin/ to alter both Product and User objects.

```
python manage.py createsuperuser
```
