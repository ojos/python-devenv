# Dockerfile
FROM python:3.8-slim-buster

# Do not stdout/stderr buffer
ENV PYTHONUNBUFFERED 1

# Install dependent packages
RUN apt update
RUN apt -y install gcc \
    git \
    libmariadbclient-dev-compat \
    curl

# Install python packages
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt

COPY ./run.sh /run.sh
RUN chmod +x /run.sh

COPY ./gunicorn.py /gunicorn.py

COPY ./deploy /deploy

COPY ./src /app
WORKDIR /app/

ENV PYTHONPATH=/app

CMD ["/run.sh"]
