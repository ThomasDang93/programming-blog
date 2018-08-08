import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config


# Automatically creates admin user when deployed
# Admin is created either by environment variables from server or the env file
class Command(BaseCommand):

    def handle(self, *args, **options):
        # Retreiving username environment variables
        if 'AWS_USERNAME' in os.environ:
            USERNAME = os.environ.get('AWS_USERNAME')
        else:
            USERNAME = config('USERNAME')

        # Retreiving email environment variables
        if 'AWS_EMAIL' in os.environ:
            EMAIL = os.environ.get('AWS_EMAIL')
        else:
            EMAIL = config('EMAIL')

        # Retreiving password environment variables
        if 'AWS_PASSWORD' in os.environ:
            PASSWORD = os.environ.get('AWS_PASSWORD')
        else:
            PASSWORD = config('PASSWORD')

        # Create an admin user if server host does not provide a default user
        if not User.objects.filter(username=USERNAME).exists():
            User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
