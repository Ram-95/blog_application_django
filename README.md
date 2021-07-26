# Blog_application_django
A simple blog application developed using Django framework

### Steps to be followed for first time use
- Run these commands - This will create your Tables (by the Model definition) in the Database
```
python manage.py makemigrations

python manage.py migrate
```
- Create an ```admin``` user by running these following commands
```
$ python manage.py createsuperuser
```

### API Endpoints
- To get a users data - ```/api/users/?username=<username>```
- To get all posts of a user - ```/api/posts/?username=<username>```
- To get a post by it's **id** = ```/api/view_post/?post_id=<id>```
