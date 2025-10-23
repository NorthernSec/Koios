#!/bin/sh
# Script Order
#  - Collect static
#  - Ensure database started
#  - Migrate database changes

###
# Install requirements

export PIP_DISABLE_PIP_VERSION_CHECK=1
export PIP_ROOT_USER_ACTION=ignore

echo "📦 Installing requirements"
if [ -f "requirements.txt" ]; then
   pip install --upgrade --quiet --root-user-action=ignore -r requirements.txt
fi

if [ -f "app-requirements.txt" ]; then
   pip install --upgrade --quiet --root-user-action=ignore -r app-requirements.txt
fi

###
# Collect Static
echo "📁 Collecting static files"
python manage.py collectstatic --no-input --clear

###
# Ensure database started
if [ "$DJANGO_DB_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "⏳Waiting for postgres..."
    while ! nc -z $DJANGO_DB_HOST $DJANGO_DB_PORT; do
      sleep 0.1
    done
    echo "🐘 PostgreSQL started"
fi

###
# Migrate potential database changes
echo "🛠️ Making migrations if necessary"
python manage.py makemigrations
python manage.py migrate

###
# Create superuser if note exists
python manage.py shell -c "exec(open('/usr/src/entrypoint/admin-creator.py').read())"


exec "$@"
