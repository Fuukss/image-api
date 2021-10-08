# image-api

## Setup
To run this project:

```
$ python manage.py makemigrations
$ python manage.py migrate 
$ python manage.py createsuperuser 

$ python manage.py loaddata initial_role_data.json

$ docker-compose up --build

$ coverage run manage.py test && coverage report && coverage html
```