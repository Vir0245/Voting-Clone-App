FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 80

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80", "--workers", "4", "--keep-alive", "0"]
