FROM bitnami/spark:3.5.0

USER root

RUN apt-get update && \
    apt-get install -y curl gnupg unzip default-jre && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ src/
COPY datamart-pg-csv-fat.jar .
COPY .env .

# Example CSV
COPY src/sql/source_data.csv /app/source_data.csv
# init.sql
COPY src/sql/init.sql /app/src/sql/init.sql

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]