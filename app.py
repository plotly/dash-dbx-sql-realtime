from dash import Dash, Input, Output, State, callback, no_update
from datetime import datetime

import utils.components as components

from utils.dbx_utils import df_live, df_ma

outside_index = df_ma.tail(1).index[0]

app = Dash(
    __name__,
    title="Realtime Dash-DBX", 
    update_title=None,
    suppress_callback_exceptions=True
)
app.layout = components.layout
server = app.server


@callback(
    Output("live-data-graph", "extendData"),
    Output("live-data-information", "children"),
    Output("store-data", "data"),
    Input("live-data-interval", "n_intervals"),
    State("store-data", "data"),
)
def update_live_data(n, storage):
    recent_live_index = df_live.tail(1).index[0]
    recent_ma_index = df_ma.tail(1).index[0]
    print("outside index is:", outside_index)
    print(df_ma.tail(5))
    print(f"recent_live_index: {recent_live_index}, old: {storage['df_live_index']}")
    print(f"recent_ma_index: {recent_ma_index}, old: {storage['df_ma_index']} ")

    if (storage["df_live_index"] == recent_live_index) or (storage["df_ma_index"] == recent_ma_index):
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx No new data")
        return no_update, no_update, no_update

    print("NEEEEEEEEEEEEEEW DATAAAAAAAAAAAAAA works")

    last_used_live_index = storage["df_live_index"]
    new_date_live = df_live["EventTimestamp"].iloc[last_used_live_index:]
    new_temp = df_live["TempReading"].iloc[last_used_live_index:]
    new_hum = df_live["HumidityReading"].iloc[last_used_live_index:]

    last_used_ma_index = storage["df_ma_index"]
    new_date_ma = df_ma["TimestampSecond"].iloc[last_used_ma_index:]
    ma_temp_avg = df_ma["Temperature_Moving_Average"].iloc[last_used_ma_index:]
    ma_humid_avg = df_ma["Humidity_Moving_Average"].iloc[last_used_ma_index:]

    # get rows in pandas 2 to 20

    

    time = datetime.now().strftime("%H:%M:%S")
    return [
        dict(
            x=[new_date_ma, new_date_live, new_date_ma, new_date_live],
            y=[ma_temp_avg, new_temp, ma_humid_avg, new_hum],
        ), [0, 1, 2, 3], 60
    ], components.style_text(ma_temp_avg, ma_humid_avg, time), {"df_live_index": recent_live_index, "df_ma_index": recent_ma_index}

if __name__ == '__main__':
    app.run_server(debug=False)