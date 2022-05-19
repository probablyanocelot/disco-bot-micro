FROM library/postgres
ENV POSTGRES_USER test
ENV POSTGRES_PASSWORD test
ENV POSTGRES_DB player

FROM python:3.10.2
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

# use docker-compose to run the app