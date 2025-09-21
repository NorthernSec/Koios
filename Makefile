# Service name from docker-compose.yml
SERVICE=app
DATABASE=db

# Run Django management commands
manage:
	docker compose up -d $(DATABASE)
	docker compose run --rm $(SERVICE) python manage.py $(cmd)
	docker compose down

# Start a new app: make startapp name=myapp
startapp:
	docker compose up -d $(DATABASE)
	docker compose run --rm $(SERVICE) python manage.py startapp $(name)
	docker compose down
	sudo chown -R $(shell id -u):$(shell id -g) app/$(name)

# Apply migrations
migrate:
	docker compose up -d $(DATABASE)
	docker compose run --rm $(SERVICE) python manage.py migrate
	docker compose down

# Create migrations
makemigrations:
	docker compose up -d $(DATABASE)
	docker compose run --rm $(SERVICE) python manage.py makemigrations
	docker compose down

# Open a Django shell
shell:
	docker compose up -d $(DATABASE)
	docker compose run --rm $(SERVICE) python manage.py shell
	docker compose down

# Bring up the full stack
up:
	docker compose up

# Stop containers
down:
	docker compose down
