# Image-api

## Run the app 
```
$ docker-compose up --build
```

## Setup
To run this project:
```
$ docker exec -it imageapi_app_1 python manage.py createsuperuser
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
        - image: image file in png or jpg format and file size less than 2Mb 
        - expire_time: integer. If user account have option for links expiring in time, can choice expiring time in request in seconds.

    Response for accounts:
    - basic: 
        * a link to a thumbnail that's 200px in height
    - premium: 
        * a link to a thumbnail that's 200px in height
        * a link to a thumbnail that's 400px in height
        * a link to the originally uploaded image
    - enterprise: 
        * a link to a thumbnail that's 200px in height
        * a link to a thumbnail that's 400px in height
        * a link to the originally uploaded image
        * ability to fetch a link that expires after a number of seconds (user can specify any number between 300 and 30000)
    - plans created by admin:
        * links to a selected thumbnails  
        * optional: a link to the originally uploaded image 
        * optional: a link expires in time
    
## GET a list of images  
    Url: https://<your-domain>/api/blog/list
    
    Headers: 
        - Authorization: Token <token>
    
    Return a list of of all the images for the currently authenticated user.