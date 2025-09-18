import os
from dataclasses import dataclass
from pyspark.sql import SparkSession
from dataclasses import field, dataclass


@dataclass
class SparkConfig:
    master: str = os.getenv("SPARK_MASTER", "local[*]")
    driver_memory: str = os.getenv("SPARK_DRIVER_MEMORY", "1g")
    executor_memory: str = os.getenv("SPARK_EXECUTOR_MEMORY", "1g")
    driver_cores: str = os.getenv("SPARK_DRIVER_CORES", "1")
    executor_cores: str = os.getenv("SPARK_EXECUTOR_CORES", "1")
    num_executors: str = os.getenv("SPARK_NUM_EXECUTORS", "1")
    java_opts: str = os.getenv("SPARK_JAVA_OPTS", "-Dfile.encoding=UTF-8")
    default_fs: str = os.getenv("SPARK_DEFAULT_FS", "hdfs://namenode:9000")

    def get_spark_session(self) -> SparkSession:
        builder = SparkSession.builder.master(self.master).appName("lab7_datamart_model")
        builder = builder.config("spark.driver.memory", self.driver_memory)
        builder = builder.config("spark.executor.memory", self.executor_memory)
        builder = builder.config("spark.driver.cores", self.driver_cores)
        builder = builder.config("spark.executor.cores", self.executor_cores)
        builder = builder.config("spark.executor.instances", self.num_executors)
        builder = builder.config("spark.driver.extraJavaOptions", self.java_opts)
        builder = builder.config("spark.executor.extraJavaOptions", self.java_opts)
        #builder = builder.config("spark.hadoop.fs.defaultFS", self.default_fs)
        return builder.getOrCreate()


@dataclass
class AppConfig:
    model_path: str = os.getenv("MODEL_PATH", "src/models/kmeans_model")
    source_file: str = os.getenv("SOURCE_FILE", "src/sql/source_data.csv")

    spark: SparkConfig = field(default_factory=SparkConfig)
    
    # Postgres configuration
    postgres_hostname: str = os.getenv("POSTGRES_HOSTNAME", "postgres-service")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")
    postgres_db: str = os.getenv("POSTGRES_DB", "mydatabase")
    postgres_user: str = os.getenv("POSTGRES_USER", "user")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "password")
    
    # Table names
    input_table: str = os.getenv("POSTGRES_INPUT_TABLE", "source_data")

    processed_csv_path: str = os.getenv("PROCESSED_CSV_PATH", "processed_data.csv")