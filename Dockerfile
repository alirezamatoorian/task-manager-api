FROM python:3.14-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

#CMD ["python","manage.py","runserver","0.0.0.0:8000"]
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "core.wsgi:application" ,"--bind", "0.0.0.0:8000"]