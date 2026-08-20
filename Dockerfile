FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 10000

CMD ["gunicorn", "djackets_django.wsgi:application", "--bind", "0.0.0.0:10000"]