# pull official base image
FROM python:3.9.5-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/src/app

# install system dependencies
RUN apt-get update && apt-get install -y \
    netcat \
    dos2unix \
    libpq-dev \
    gcc \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

# convert line endings
RUN dos2unix /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# create media directory
RUN mkdir -p /usr/src/app/media/posts

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# run app
CMD ["python", "manage.py", "run", "-h", "0.0.0.0"]
