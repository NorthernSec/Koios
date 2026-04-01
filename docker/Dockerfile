# Pull the python image
FROM python:3.11-slim

# Environment variables from Args
ARG APT_PACKAGES

# Static Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        postgresql-common \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Create entrypoint directory
RUN mkdir /usr/src/entrypoint

# Create working directory & use it as the workdir
WORKDIR /usr/src/app

# Install python dependencies
COPY ../app/requirements.txt .
RUN pip install -r requirements.txt
RUN rm -f requirements.txt

# Dynamic package requirements
RUN if [ -n "$APT_PACKAGES" ]; then \
      apt-get update && \
      apt-get install -y --no-install-recommends $APT_PACKAGES && \
      rm -rf /var/lib/apt/lists/*; \
    fi

# Create Entrypoint Hook
ENTRYPOINT ["/usr/src/entrypoint/docker-entrypoint.sh"]
