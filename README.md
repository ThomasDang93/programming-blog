# programming-blog

**programming-blog** is my personal Django project that serves 
as a template for a blog websitemade with programmers in mind. 
Here are the major features: 
* Markdown editor
* Disqus comment integration
* Taxonomy with Categories and Tags 
* Blog post pagination
* Online Resume Template

This projecet was initially made to deploy in AWS, but you can easily 
tweak the code to utilize whatever hosting provider you like.

The code in this repository runs my personal website, which you can check out right here:

https://www.thomasbyte.com/


Quick start
-----------
These instructions assume that you have initiated a brand new Django project with `django-admin startproject ebdjango`. You should also create your own virtual environment with `virtualenv` to avoid package conflicts.

## Step 1
In your new Django project, save your SECRET_ACCESS_KEY into a text editor. You will need it later.

Now capture the **programming-blog** repository using `git clone https://github.com/ThomasDang93/programming-blog.git`.
Once captured, move all the files into your Django root directory so that it overirides your original Django files. 
Your root directory should look something like this.
```
	.
	├── blog
	│   ├── admin.py
	│   ├── apps.py
	│   ├── __init__.py
	│   ├── management
	│   ├── migrations
	│   ├── models.py
	│   ├── static
	│   ├── templates
	│   ├── templatetags
	│   ├── tests.py
	│   ├── urls.py
	│   └── views.py
	├── manage.py
	├── mysite
	├── README.rst
	└── requirements.txt
  ```

You can also include .ebextensions and .ebignore in the root directory, but 
those will only be used for deploying this project to AWS. Refer to these docs
if you would like to learn how to deploy on AWS:

https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html

https://realpython.com/deploying-a-django-app-and-postgresql-to-aws-elastic-beanstalk/

## Step 2

Make sure you download all the python packages listed in `requirements.txt` using:

`pip install -r /path/to/requirements.txt`

## Step 3

Add this to your INSTALLED_APPS in settings.py
```
INSTALLED_APPS = [
    ...
  'blog',
  'martor',
  'taggit',
  'taggit_templatetags2',
  'disqus',
]
```

## Step 4

Your project `urls.py` should look like this:

```
import os
from django.contrib import admin
from django.urls import include, path
from decouple import config

if 'AWS_ADMIN' in os.environ:
    ADMIN = os.environ.get('AWS_ADMIN')
else:
    ADMIN = config('ADMIN')
urlpatterns = [
    path('', include('blog.urls')),
    path(ADMIN, admin.site.urls),
    path('martor/', include('martor.urls')),
]
```

## Step 5

The `.env` file contains environment variables needed to run the project. 
This helps decouple the deployment process for production environment while still
allowing you to run this project locally. When you decide to deploy to a hosting environment, it
is recommended that you establish environment variables for that host instead of hardcoding 
sensitive information like secret keys. Open `.env` and proceed to set up those variables, including
the SECRET_ACCESS_KEY that you saved earlier. Some variables may be optional depending on whether or 
not you need them for local testing.

## Step 6

Run `python manage.py makemigrations` and then `python manage.py migrate` to create the blog models.

## Step 7

Create username and password with this command:
`python manage.py createsuperuser`

To make a blog, start the development server with
`python manage.py runserver`
and visit http://127.0.0.1:8000/admin/ to access the admin.
You must login with the username and password you created.
   
## Step 8

Visit http://localhost:8000 to view your website.

## That's it!
Just note that when you decide to deploy your website in a production environment, you need to do a few things to add security.
1. Set `DEBUG = FALSE` in `settings.py`
2. Uncomment this code block from `settings.py`
```
# Requests over HTTP are redirected to HTTPS.
SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Set this to True to avoid transmitting the session cookie over HTTP accidentally.
SESSION_COOKIE_SECURE = True

# Set this to True to avoid transmitting the CSRF cookie over HTTP accidentally.
CSRF_COOKIE_SECURE = True

# HSTS is an HTTP header that informs a browser that all future connections to a particular
# site should always use HTTPS. Combined with redirecting requests over HTTP to HTTPS,
# this will ensure that connections always enjoy the added security of SSL provided one
# successful connection has occurred.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True

# Prevents the browser from guessing the content type
SECURE_CONTENT_TYPE_NOSNIFF = True

# Enables the XSS filter in the browser, and force it to always block XSS attacks
SECURE_BROWSER_XSS_FILTER = True

# Prevents click jacking
X_FRAME_OPTIONS = 'DENY'
```
For a deeper explanation on the code you just uncommented, visit this link:
https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

3. Enter your website domain name in `ALLOWED_HOSTS`.
```
ALLOWED_HOSTS = [
    'www.domainname.com',
]
```
