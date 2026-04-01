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
tmp_requirements=$(mktemp)

python3 -c "
import tomllib
from pathlib import Path

deps = set()

for file in Path('.').rglob('applet.toml'):
    with open(file, 'rb') as f:
        data = tomllib.load(f)
    deps.update(data.get('python', {}).get('dependencies', []))

print('\n'.join(sorted(deps)))
" > "${tmp_requirements}_sorted"

if [ -s "${tmp_requirements}_sorted" ]; then
    pip install --upgrade --root-user-action=ignore --quiet \
        -r "${tmp_requirements}_sorted"
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
