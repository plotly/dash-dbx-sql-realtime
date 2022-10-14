from constants import (
    SERVER_HOSTNAME,
    HTTP_PATH,
    ACCESS_TOKEN,
    DB_NAME,
    DEVICE_TABLE_SILVER,
    DEVICE_TABLE_GOLD
)


from databricks import sql


import datetime as dt
app_start_ts = dt.datetime.now()

def get_bme_data(TempReading, HumidityReading, EventTimestamp, EventDate):
    connection0 = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
    )
    cursor0 = connection0.cursor()
    cursor0.execute(
        f"SELECT EventTimestamp, TempReading, HumidityReading, EventDate FROM {DB_NAME}.{DEVICE_TABLE_SILVER} ORDER BY EventTimestamp;"
    )
    df = cursor0.fetchall_arrow()
    df = df.to_pandas()
    cursor0.close()
    connection0.close()
    return df

def get_moving_average(Temp_15s_Moving_Average, Humidity_15s_Moving_Average, Temp_60s_Moving_Average, Humidity_60s_Moving_Average, TimestampSecond):
    connection1 = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
    )
    cursor1 = connection1.cursor()
    cursor1.execute(
        f"SELECT Temp_15s_Moving_Average, Humidity_15s_Moving_Average, Temp_60s_Moving_Average, Humidity_60s_Moving_Average, TimestampSecond FROM {DB_NAME}.{DEVICE_TABLE_GOLD} ORDER BY TimestampSecond;"
    )
    df1 = cursor1.fetchall_arrow()
    df1 = df1.to_pandas()
    cursor1.close()
    connection1.close()
    return df1


