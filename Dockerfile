FROM python:3.14-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app



COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app

RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

#CMD ["python","manage.py","runserver","0.0.0.0:8000"]

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8000"]