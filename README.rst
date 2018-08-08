=====
programming-blog
=====

programming-blog is my personal Django project that serves 
as a template for a blog website made for programmers. It 
features a Markdown editor, Disqus comment integration, 
categories, tags, and blog post pagination. This project
was made to deploy in AWS.


Quick start
-----------
These instructions assume that you have initiated a brand new Django project
and have copied the needed files from the "programming-blog" repository onto your root 
directory. You should also create your own virtual environment to avoid package conflicts.

1. Your root directory should look like this with all the source files in each folder.
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

You can also include .ebextensions and .elasticbeanstalk in the root directory, but 
those folders will only be used for deploying this project to AWS. Refer to AWS docs
on how to deploy this project to a production environment.

1. Make sure you download all the python packages listed in "requirements.txt" using:

	pip install -r /path/to/requirements.txt

2. Add this to your INSTALLED_APPS in settings.py

    INSTALLED_APPS = [
        ...
        'blog',
	    'martor',
	    'taggit',
	    'taggit_templatetags2',
	    'disqus',
    ]

3. Your project urls.py should look like this:

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

4. The .env file contains environment variables needed to run the project. 
   This helps decouple the deployment process for production environment while still
   allowing you to run this project locally. Open .env and proceed to set up those variables. Some may be optional depending if you need them for local testing.

3. Run `python manage.py migrate` to create the blog models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a blog (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/polls/ to participate in the blog.