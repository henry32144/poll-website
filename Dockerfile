FROM python:3.7
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "wsgi:app", "-c", "./gunicorn.conf.py"]