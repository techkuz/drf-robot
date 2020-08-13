FROM python:3.7.6

ENV PYTHONUNBUFFERED 1

COPY . /students_api

WORKDIR /students_api

RUN pip install -r requirements.txt

EXPOSE 8080

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8080
