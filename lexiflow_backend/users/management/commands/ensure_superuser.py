import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser from environment variables if it does not exist'

    def handle(self, *args, **options):
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        full_name = os.environ.get('DJANGO_SUPERUSER_FULL_NAME', 'Admin User')

        if not email or not password:
            self.stdout.write(self.style.WARNING(
                'Superuser environment variables (DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD) not set. Skipping.'
            ))
            return

        # Use the custom user model's manager
        if not User.objects.filter(email=email).exists():
            try:
                User.objects.create_superuser(
                    email=email,
                    password=password,
                    full_name=full_name,
                    username=email  # required by Django's AbstractUser
                )
                self.stdout.write(self.style.SUCCESS(f'Superuser {email} created successfully.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create superuser: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser {email} already exists.'))