# Pull the python image
FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y build-essential postgresql-common libpq-dev
RUN rm -rf /var/lib/apt/lists/*

# Create entrypoint directory
RUN mkdir /usr/src/entrypoint

# Create working directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# Install python dependencies
COPY ../app/*requirements.txt .
RUN pip install -r requirements.txt
RUN if [ -f app-requirements.txt ]; then pip install -r app-requirements.txt; fi
RUN rm -f *requirements.txt

# Create Entrypoint Hook
ENTRYPOINT ["/usr/src/entrypoint/docker-entrypoint.sh"]
