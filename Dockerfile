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
    curl

#RUN useradd -ms /bin/bash bakersoft
#USER bakersoft

RUN pip install --upgrade pip

COPY . .
RUN pip install -e .[dev]

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8080"]
