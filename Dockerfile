# Dockerfile
FROM python:3.9

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y libpq-dev
RUN pip install -r requirements.txt

RUN pip install psycopg2-binary

RUN pip install alembic

ENV FLASK_APP=app/__init__.py

RUN rm -rf migrations
RUN flask db init
RUN flask db migrate -m "Initial migration"
RUN flask db upgrade

EXPOSE 1010

CMD ["flask", "run", "--host=0.0.0.0", "--port=1010"]
