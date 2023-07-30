FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install django
RUN pip install django-restframework
RUN pip install Pillow

WORKDIR /app

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
