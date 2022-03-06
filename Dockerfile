FROM tiangolo/uwsgi-nginx-flask:latest

COPY ./app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV STATIC_PATH /app/website/static

COPY ./app /app
