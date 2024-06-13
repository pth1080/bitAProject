# Use the official Python base image
FROM python:3.11.6-slim

# Set environment variables to prevent creation of __pycache__ and .DS_Store
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app /app

RUN pip install -r /app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
