import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

class Command(BaseCommand):
    help = 'Create a superuser if it does not already exist'

    def handle(self, *args, **options):

        User = get_user_model()
        admin_username = config('DJANGO_SUPERUSER_USERNAME')
        admin_email = config('DJANGO_SUPERUSER_EMAIL')
        admin_password = config('DJANGO_SUPERUSER_PASSWORD')
        if admin_email and admin_password and admin_username:
            if not User.objects.filter(username=admin_username).exists():
                User.objects.create_superuser(username=admin_username, email=admin_email, password=admin_password)
                self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
            else:
                self.stdout.write(self.style.SUCCESS('Superuser already exists.'))
        else:
            self.stdout.write(self.style.ERROR('Superuser details are not set in environment variables.'))
