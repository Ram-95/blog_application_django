# Blog_application_django
A simple blog application developed using Django framework

### Steps to be followed for first time use
- #### Set these Environment variables along with AWS Credentials

```
DEBUG_VALUE = True
DJANGO_ENV = DEV
SECRET_KEY_BLOG = <Generate some secret key>
```

- #### Run these commands - This will create your Tables (by the Model definition) in the Database
```
python manage.py makemigrations

python manage.py migrate
```
- ##### Create an ```admin``` user by running these following commands
```
python manage.py createsuperuser
```
- #### Run Tests to ensure everything is set up and working correctly.
```
python manage.py test
```

### API Endpoints
- To get a users data:
  > ```/api/users/?username=<username>```
- To get all posts of a user:
  > ```/api/posts/?username=<username>```
- To get a post by it's **id**:
  >```/api/view_post/?post_id=<id>```

### Screenshots

###### Homepage

![Homepage](https://raw.githubusercontent.com/Ram-95/blog_application_django/DRF_slug_branch/screenshots/Screenshot_2021-07-30-22-09-44-19.jpg)

###### Post
![View Post](https://raw.githubusercontent.com/Ram-95/blog_application_django/DRF_slug_branch/screenshots/Screenshot_2021-07-30-22-10-53-97.jpg)
##### See live at: https://blog-app-pydj.herokuapp.com/


#### This will be updated regularly....
