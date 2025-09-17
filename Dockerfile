FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Dependências de sistema para compilar psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq-dev \
       build-essential \
       python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip 

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "soilanalysis.wsgi:application"]
