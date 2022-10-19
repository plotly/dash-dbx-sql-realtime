from databricks import sql
import datetime, random

from constants import (
    SERVER_HOSTNAME,
    HTTP_PATH,
    ACCESS_TOKEN,
    DB_NAME,
    DEVICE_TABLE_SILVER,
    DEVICE_TABLE_GOLD,
    app_start_ts
)

random.seed(42)

def get_immediate_vals():
    connection0 = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
    )
    cursor0 = connection0.cursor()
    cursor0.execute(
        f"SELECT * FROM {DB_NAME}.{DEVICE_TABLE_SILVER} WHERE EventTimestamp >= '{app_start_ts}'::timestamp ORDER BY EventTimestamp ASC;"
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
        f"SELECT * FROM {DB_NAME}.{DEVICE_TABLE_GOLD} WHERE TimestampSecond >= '{app_start_ts}'::timestamp ORDER BY TimestampSecond ASC;"
    )
    df1 = cursor1.fetchall_arrow()
    df1 = df1.to_pandas()
    cursor1.close()
    connection1.close()
    return df1

def get_new_live_data_offline(ma_temp, ma_humid, i=0, generate_past_data=False):
    if generate_past_data:
        timestamp_now = datetime.datetime.now() - datetime.timedelta(seconds=i)
    else:
        timestamp_now = datetime.datetime.now()
    timestamp_now = timestamp_now.strftime("%Y-%m-%d %H:%M:%S")
    

    random_temp = round(random.uniform(20, 30), 1)
    ma_temp.append(random_temp)
    ma_temp = ma_temp[-7:]
    ma_temp_avg = round(sum(ma_temp) / len(ma_temp), 1)

    # add to ma_humid and only keep last 7 values
    random_humidity = round(random.uniform(40, 60), 1)
    ma_humid.append(random_humidity)
    ma_humid = ma_humid[-7:]
    ma_humid_avg = round(sum(ma_humid) / len(ma_humid), 1)

    return timestamp_now, random_temp, ma_temp_avg, ma_temp, random_humidity, ma_humid_avg, ma_humid

