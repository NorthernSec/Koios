import os
import sys

from django.contrib.auth import get_user_model

username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "changeme")
email    = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@localhost.local")

if not (username and password and email):
    print("Could not create superuser. Check your environment variables.")
    sys.exit(0)

User = get_user_model()  # get the currently active user model,

print("Checking user")
User.objects.filter(username=username).exists() or \
    User.objects.create_superuser(username, email, password)
print("Ensured user from .env file exists")
