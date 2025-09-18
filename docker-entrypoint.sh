#!/bin/bash
set -euo pipefail

echo "Entrypoint: starting Spark data pipeline with PostgreSQL"

# Загружаем переменные из .env
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# 0. Загружаем исходные данные в PostgreSQL (создание таблицы + mock данные)
echo "Step 0: Uploading data to PostgreSQL"
python3 src/utils/uploader.py

SPARK_MASTER="$SPARK_MASTER"
JAR_PATH="$JAR_PATH"
INPUT_TABLE="$POSTGRES_TABLE_SOURCE"
PROCESSED_CSV_PATH="$PROCESSED_CSV_PATH"

echo "Using PostgreSQL table: $INPUT_TABLE"
echo "Using output CSV path: $PROCESSED_CSV_PATH"
echo "Using Spark master: $SPARK_MASTER"

# 1. Запускаем Scala для ETL
echo "Step 1: Running Scala ETL job to export from PostgreSQL to CSV"
spark-submit \
    --master "$SPARK_MASTER" \
    --class DataMart \
    "$JAR_PATH" \
    "$INPUT_TABLE" \
    "$PROCESSED_CSV_PATH" &

SCALA_PID=$!
echo "Scala process started with PID: $SCALA_PID"

# 2. Даем время на выполнение
sleep 15

# 3. Запускаем Python обработку
echo "Step 2: Running Python processing from CSV"
python3 src/main.py

# 4. Завершаем Scala процесс (если он еще жив)
kill $SCALA_PID 2>/dev/null || true

echo "All jobs finished successfully"

# Keep the container running
tail -f /dev/null

