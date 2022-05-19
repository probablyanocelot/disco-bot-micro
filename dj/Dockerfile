FROM library/postgres
ENV POSTGRES_USER test
ENV POSTGRES_PASSWORD test
ENV POSTGRES_DB dj
ENV FLASK_APP=app.py


FROM python:3.10.2
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Create, init venv:
# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

#  Add dependency files:
ADD backend_youtube_dl.py /usr/local/lib/python3.10/site-packages/pafy
# ADD ffmpeg.exe /usr/local/lib ?

COPY . /app

# use docker-compose to run the app