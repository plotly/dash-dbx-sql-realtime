import os
from databricks import sql

DB_NAME = "raspberrypisim_db"
DEVICE_TABLE_SILVER = "silver_sensors"
DEVICE_TABLE_GOLD = "gold_sensors"

SERVER_HOSTNAME = os.environ.get("SERVER_HOSTNAME")
HTTP_PATH = os.environ.get("HTTP_PATH")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")

def get_live_data():
    connection0 = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
    )
    cursor0 = connection0.cursor()
    cursor0.execute(
        f"SELECT * FROM {DB_NAME}.{DEVICE_TABLE_SILVER} ORDER BY EventTimestamp ASC;"
    )
    df = cursor0.fetchall_arrow()
    df = df.to_pandas()
    cursor0.close()
    connection0.close()
    return df

def get_moving_average():
    connection1 = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
    )
    cursor1 = connection1.cursor()
    cursor1.execute(
        f"SELECT * FROM {DB_NAME}.{DEVICE_TABLE_GOLD} ORDER BY TimestampSecond ASC;"
    )
    df1 = cursor1.fetchall_arrow()
    df1 = df1.to_pandas()
    cursor1.close()
    connection1.close()
    return df1


df_live = get_live_data()
df_ma = get_moving_average()