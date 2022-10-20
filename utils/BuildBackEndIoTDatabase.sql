# Define the variables used for creating connection strings
adlsAccountName = "ADLSACCOUNTNAME"
adlsContainerName = "ADLSCONTAINERNAME"
adlsFolderName = "ADLSFOLDERNAME"
mountPoint = "MOUNTPOINT"

# Application (Client) ID
applicationId = dbutils.secrets.get(scope="rpscope",key="ApplicationID")

# Application (Client) Secret Key
authenticationKey = dbutils.secrets.get(scope="rpscope",key="ServiceCredentialKey")

# Directory (Tenant) ID
tenandId = dbutils.secrets.get(scope="rpscope",key="DirectoryID")

endpoint = "https://login.microsoftonline.com/" + tenandId + "/oauth2/token"
source = "abfss://" + adlsContainerName + "@" + adlsAccountName + ".dfs.core.windows.net/" + adlsFolderName

# Connecting using Service Principal secrets and OAuth
configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": applicationId,
           "fs.azure.account.oauth2.client.secret": authenticationKey,
           "fs.azure.account.oauth2.client.endpoint": endpoint}

# Mounting ADLS Storage to DBFS
# Mount only if the directory is not already mounted

if not any(mount.mountPoint == mountPoint for mount in dbutils.fs.mounts()):
    
    dbutils.fs.mount(
    source = source,
    mount_point = mountPoint,
    extra_configs = configs
    )
    
service_credential = dbutils.secrets.get(scope="rpscope",key="ServiceCredentialKey")
spark.conf.set("fs.azure.account.auth.type.s2stdastream.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.s2stdastream.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.s2stdastream.dfs.core.windows.net", "applicationId")
spark.conf.set("fs.azure.account.oauth2.client.secret.s2stdastream.dfs.core.windows.net", service_credential)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.s2stdastream.dfs.core.windows.net", "https://login.microsoftonline.com/tenandId/oauth2/token")

bronze_checkpoint_location = "/dbfs/FileStore/tables/checkpoints/bronze/" ## Changed checkpoint_location to bronze_checkpointlocation
silver_checkpoint_location = "/dbfs/FileStore/tables/checkpoints/silver/" ## Changed checkpoint_location to bronze_checkpointlocation

dbutils.fs.rm(bronze_checkpoint_location, recurse=True)
dbutils.fs.rm(silver_checkpoint_location, recurse=True)

%sql
CREATE DATABASE IF NOT EXISTS raspberrypisim_db;
USE raspberrypisim_db;
from pyspark.sql.types import *
from pyspark.sql.functions import *


inputPath = "abfss://" + adlsContainerName + "@" + adlsAccountName + ".dfs.core.windows.net/" + adlsFolderName 


streamingInputDF = (spark
                    .readStream
                    .format("cloudFiles")
                    .option("cloudFiles.format", "text")
                    .option("cloudFiles.maxFilesPerTrigger", 100000)
                    .load(inputPath)
                    .selectExpr(
                    "value:messageId::integer AS Message",
                    "value:deviceId::string AS DeviceName",
                    "value:temperature::float AS TempReading",
                    "value:humidity::float AS HumidityReading",
                    "value:EventProcessedUtcTime::timestamp AS EventTimestamp",
                    "value:EventProcessedUtcTime::timestamp::date AS EventDate", 
                    "current_timestamp() AS ReceivedTimestamp",
                    "input_file_name() AS InputFileName",
                    "value"
                    )
                    )


#dbutils.fs.rm(bronze_checkpoint_location, recurse = True) ## Check 

(
    streamingInputDF
     .writeStream
     .format("delta")
     .outputMode("append")
     .option("checkpointLocation", bronze_checkpoint_location)
     .option("mergeSchema", "true") 
     .trigger(processingTime= '2 seconds') ## processing_time = '2 seconds' for realtime version
     .toTable("raspberrypisim_db.bronze_sensors")  
)



bronze_df = (spark.readStream.format("delta").table("raspberrypisim_db.bronze_sensors").withWatermark("EventTimestamp", "10 minutes"))
    
int_df = (
                    bronze_df
                    .groupBy(col("DeviceName"), window(bronze_df.EventTimestamp, "1 second").alias("EventWindow"))
                    .agg(
                    avg(col("TempReading")).cast("float").alias("TempReading"),
                    avg(col("HumidityReading")).cast("float").alias("HumidityReading"),
                    min(col("EventTimestamp")).cast("timestamp").alias("EventTimestamp"),
                    min(col("EventDate")).cast("date").alias("EventDate"),
                    min(col("ReceivedTimestamp")).cast("timestamp").alias("ReceivedTimestamp"),
                    min(col("InputFileName")).alias("InputFileName")
                    )
          )
    
(
    int_df.writeStream.format("delta").trigger(processingTime="2 seconds").option("checkpointLocation", silver_checkpoint_location).outputMode("append").toTable("raspberrypisim_db.silver_sensors")
)


%sql

CREATE OR REPLACE VIEW raspberrypisim_db.gold_sensors

AS
(
SELECT 
  date_trunc('second', EventTimestamp) AS TimestampSecond,
  AVG(TempReading) OVER(ORDER BY EventTimestamp ROWS BETWEEN 7 PRECEDING AND CURRENT ROW) AS Temperature_Moving_Average,
  AVG(HumidityReading) OVER(ORDER BY EventTimestamp ROWS BETWEEN 7 PRECEDING AND CURRENT ROW) AS Humidity_Moving_Average,
FROM raspberrypisim_db.silver_sensors
)

%sql
SELECt * FROM raspberrypisim_db.gold_sensors -- This will work when streaming real-time, but 2 min window is small
WHERE TimestampSecond::double >= (current_timestamp()::double - 60000) -- Rolling 120 seconds of window

-- This way you can let PLotly Dash app decide dynamically how far back you want it to go
-- This will be the query plotly pushes down to databricks every couple seconds


spark.sql("""OPTIMIZE raspberrypisim_db.silver_sensors ZORDER BY (EventTimestamp)""")