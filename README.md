# Image-api

## Setup
To run this project:
```
$ python manage.py makemigrations
$ python manage.py migrate 
$ python manage.py createsuperuser 
```

## Optional 
For creating basic user plans: Basic, Premium, Enterprise
```
$ python manage.py loaddata initial_role_data.json
```

## Run the app 
```
$ docker-compose up --build
```

## Run the tests
```
$ pip install coverage 
$ coverage run manage.py test && coverage report && coverage html
```

## Authorization
All API requests require the use of a generated API token. You can find your token, by navigating to the admin/authtoken/token/ endpoint, or clicking the “Tokens” sidebar item via django-admin.

To authenticate an API request, you should provide your API token in the Authorization header.

## POST image 
    https://<your-domain>/api/image/create

    Headers: 
        -Authorization: Token <token>
    Body: 
        -image: image file in png or jpg format and file size less than 2Mb 
        -slug: slug name or empty string

    Response for accounts:
    - basic: response, slug, username, thumbnail_200
    - premium: response, slug, username, thumbnail_200, thumbnail_400, original_link
    - enterprise: response, slug, username, thumbnail_200, thumbnail_400, original_link
    - others: response, slug, username, defined thumbnail size for the plan, original image if option is True
    
## GET a list of images  
    Url: https://<your-domain>/api/blog/list
    
    Headers: 
        - Authorization: Token <token>
    
    Return a list of of all the images for the currently authenticated user.