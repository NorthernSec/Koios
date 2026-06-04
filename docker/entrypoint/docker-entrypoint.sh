#!/bin/sh
# Script Order
#  - Collect static
#  - Ensure database started
#  - Migrate database changes

GREEN='\033[1;32m'
ORANGE='\033[0;33m'
NC='\033[0m' # No Color

###
# Install requirements

export PIP_DISABLE_PIP_VERSION_CHECK=1
export PIP_ROOT_USER_ACTION=ignore

###
# Install Python Dependencies
echo "${GREEN}📦 Installing requirements${NC}"
tmp_requirements=$(mktemp)

python3 /usr/src/entrypoint/dependency_collector.py > "${tmp_requirements}"

if [ -s "${tmp_requirements}" ]; then
    pip install --upgrade --root-user-action=ignore --quiet \
        -r "${tmp_requirements}"
fi

###
# Ensure applet names are correct
python3 /usr/src/entrypoint/applet_renamer.py

###
# Collect Static
echo "${GREEN}📁 Collecting static files${NC}"
python manage.py collectstatic --no-input --clear --verbosity 0

###
# Ensure database started
if [ "$DJANGO_DB_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "${ORANGE}⏳Waiting for postgres...${NC}"
    while ! nc -z $DJANGO_DB_HOST $DJANGO_DB_PORT; do
      sleep 0.1
    done
    echo "🐘 PostgreSQL started"
fi

###
# Migrate potential database changes
echo "${GREEN}🛠️ Making migrations if necessary${NC}"
python manage.py makemigrations
python manage.py migrate

###
# Create superuser if note exists
echo "${GREEN}👑Ensuring admin account exists${NC}"
python manage.py shell -c "exec(open('/usr/src/entrypoint/admin-creator.py').read())"

exec "$@"
