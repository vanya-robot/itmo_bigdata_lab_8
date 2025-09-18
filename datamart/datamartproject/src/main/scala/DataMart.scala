import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.ml.feature.Imputer
import java.util.Properties

object DataMart {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("DataMart ETL")
      .master("local[*]")
      .config("spark.sql.adaptive.enabled", "true")
      .getOrCreate()

    // Database connection properties from environment variables
    val pgHostname = sys.env.getOrElse("POSTGRES_HOSTNAME", "postgres-service")
    val pgPort = sys.env.getOrElse("POSTGRES_PORT", "5432")
    val pgDatabase = sys.env.getOrElse("POSTGRES_DB", "mydatabase")
    val pgUser = sys.env.getOrElse("POSTGRES_USER", "user")
    val pgPassword = sys.env.getOrElse("POSTGRES_PASSWORD", "password")
    val url = s"jdbc:postgresql://$pgHostname:$pgPort/$pgDatabase"

    val connectionProperties = new Properties()
    connectionProperties.put("user", pgUser)
    connectionProperties.put("password", pgPassword)
    connectionProperties.put("driver", "org.postgresql.Driver")

    try {
      val inputTable = args(0) // Table name to read from PostgreSQL
      val outputCsvPath = if (args.length > 1) args(1) else "processed_data.csv" // Local CSV path to write to

      // Read from PostgreSQL
      println(s"Reading data from PostgreSQL table: $inputTable")
      val df = spark.read
        .jdbc(url, inputTable, connectionProperties)

      val featureCols = Array("energy_100g", "fat_100g", "carbohydrates_100g", "proteins_100g", "sugars_100g")

      // Replace negative values with null
      var processed = df
      for (c <- featureCols) {
        processed = processed.withColumn(c, when(col(c) < 0, null).otherwise(col(c)))
      }

      // Impute missing values with mean
      val imputer = new Imputer()
        .setInputCols(featureCols)
        .setOutputCols(featureCols)
        .setStrategy("mean")
      processed = imputer.fit(processed).transform(processed)

      // Select columns to save
      val toSaveCols = Array("id") ++ featureCols
      
      // Save processed data to a local CSV file
      println(s"Saving processed data to local CSV: $outputCsvPath")
      processed.select(toSaveCols.head, toSaveCols.tail: _*)
        .write.mode("overwrite")
        .option("header", "true")
        .csv(outputCsvPath)

      println(s"DATA_SAVED: true")
      println(s"OUTPUT_CSV_PATH: $outputCsvPath")
    } finally {
      spark.stop()
    }
  }
}