FROM python:3.12-rc-slim-buster

EXPOSE 8080

WORKDIR /app

RUN apt update && apt upgrade
RUN apt install -y \
    postgresql \
    postgresql-contrib \
    python-psycopg2 \
    libpq-dev \
    gcc \
    curl \
    libffi-dev

RUN pip install --upgrade pip

COPY setup.py setup.py
RUN pip install -e .[dev,client]

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8080"]
