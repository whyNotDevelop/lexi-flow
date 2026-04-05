# users/migrations/0002_create_superuser_from_env.py
import os
from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_superuser(apps, schema_editor):
    User = apps.get_model('users', 'UserModel')
    
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    full_name = os.environ.get('DJANGO_SUPERUSER_FULL_NAME', 'Admin User')
    
    if not email or not password:
        # Skip if environment variables not set – useful for local development
        return
    
    if not User.objects.filter(email=email).exists():
        User.objects.create(
            email=email,
            username=email,  # because your UserModel uses email as USERNAME_FIELD, but username is still required
            password=make_password(password),
            full_name=full_name,
            is_superuser=True,
            is_staff=True,
        )
        print(f"Superuser {email} created successfully.")
    else:
        print(f"Superuser {email} already exists.")

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),  # Replace with the actual previous migration name if different
    ]
    operations = [
        migrations.RunPython(create_superuser),
    ]# users/migrations/XXXX_create_superuser_from_env.py
import os
from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_superuser(apps, schema_editor):
    User = apps.get_model('users', 'UserModel')
    
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    full_name = os.environ.get('DJANGO_SUPERUSER_FULL_NAME', 'Admin User')
    
    if not email or not password:
        # Skip if environment variables not set – useful for local development
        return
    
    if not User.objects.filter(email=email).exists():
        User.objects.create(
            email=email,
            username=email,  # because your UserModel uses email as USERNAME_FIELD, but username is still required
            password=make_password(password),
            full_name=full_name,
            is_superuser=True,
            is_staff=True,
        )
        print(f"Superuser {email} created successfully.")
    else:
        print(f"Superuser {email} already exists.")

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),  # Replace with the actual previous migration name if different
    ]
    operations = [
        migrations.RunPython(create_superuser),
    ]