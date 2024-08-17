FROM python:3.10
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY server /app
EXPOSE 8000
CMD ["sh", "-c", "sleep 10 && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]