# Blog_application_django
A Blog application developed using Django framework 3.1. See live at: https://blog-app-pydj.herokuapp.com/

### Features:
- User Authentication - Users can register, login and logout
- Create, Edit and Delete Posts
- Users can Like and Comment on posts.
- Connections - Follow/Unfollow other users.

### Steps to be followed for first time use
- #### Set these Environment variables along with AWS Credentials

```
DEBUG_VALUE = True
DJANGO_ENV = DEV
SECRET_KEY_BLOG = <Your Secret Key>
```
- #### Run these commands - This will create your application tables (by the Model definition) in the Database.
```
python manage.py makemigrations

python manage.py migrate
```
- #### Create an ```admin``` user by running these following commands
```
python manage.py createsuperuser
```
- #### Run Tests to ensure everything is set up and working correctly.
```
python manage.py test
```

### Blog Application API Endpoints

- GET ```https://blog-app-pydj.herokuapp.com/api/v1/viewset/users``` - Returns the list of all users registered.

#### Blogposts API Endpoints
- GET ```https://blog-app-pydj.herokuapp.com/api/v1/viewset/posts``` - Returns the list of all posts by all users.
- POST ```https://blog-app-pydj.herokuapp.com/api/v1/viewset/posts``` - Creates a new post. 
    > Data required = ```{"title": "Title", "description": "Description", "author": "Author ID"}```
- GET ```https://blog-app-pydj.herokuapp.com/api/v1/viewset/posts/<id>``` - Returns a post by it's post ID.
- PUT ```https://blog-app-pydj.herokuapp.com/api/v1/viewset/posts/<id>``` - Updates a post by it's post ID.
- DELETE ```https://blog-app-pydj.herokuapp.com/api/v1/viewset/posts/<id>``` - Deletes a post by it's post ID.
- GET ```https://blog-app-pydj.herokuapp.com/api/v1/posts/?username=<username>``` - Returns a list of all posts by a specific user by his username.


#### API Documentation - https://documenter.getpostman.com/view/18647792/UVJhDuVC

#### This will be updated regularly....
