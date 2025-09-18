import os
import pandas as pd
from pyspark.sql import SparkSession
from sqlalchemy import create_engine, text
from src.config import SparkConfig, AppConfig
from dataclasses import field, dataclass


def setup_and_upload_to_postgres():
    app_cfg = AppConfig()

    pg_url = (
        f"postgresql://{app_cfg.postgres_user}:{app_cfg.postgres_password}@"
        f"{app_cfg.postgres_hostname}:{app_cfg.postgres_port}/{app_cfg.postgres_db}"
    )

    print(f"Connecting to PostgreSQL at {app_cfg.postgres_hostname}:{app_cfg.postgres_port}/{app_cfg.postgres_db}")
    
    try:
        engine = create_engine(pg_url)
        with engine.connect() as connection:
            # 1. Execute init.sql to create source_data table if not exists
            print("Executing init.sql to create table 'source_data'...")
            with open("src/sql/init.sql", "r") as f:
                init_sql_script = f.read()
            
            connection.execute(text(init_sql_script))
            connection.commit()
            print("Source table creation script executed.")

            # 2. Read local CSV and upload to PostgreSQL
            print(f"Reading local CSV file: {app_cfg.source_file}")
            df_pandas = pd.read_csv(app_cfg.source_file)

            print(f"Uploading data to PostgreSQL table: {app_cfg.input_table}")
            df_pandas.to_sql(app_cfg.input_table, engine, if_exists='replace', index=False)
            print("Initial data successfully uploaded to PostgreSQL.")

    except Exception as e:
        print(f"Error during PostgreSQL setup or upload: {e}")
        raise

if __name__ == "__main__":
    setup_and_upload_to_postgres()