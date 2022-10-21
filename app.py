from dash import Dash, Input, Output, State, callback, no_update

import utils.components as components
from utils.dbx_utils import df_live, df_ma

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

    ## if there is no new data, skip the update
    if (storage["df_live_index"] == recent_live_index) or (storage["df_ma_index"] == recent_ma_index):
        return no_update, no_update, no_update

    last_used_live_index = storage["df_live_index"]
    new_date_live = df_live["EventTimestamp"].iloc[last_used_live_index:]
    new_temp = df_live["TempReading"].iloc[last_used_live_index:]
    new_hum = df_live["HumidityReading"].iloc[last_used_live_index:]

    last_used_ma_index = storage["df_ma_index"]
    new_date_ma = df_ma["TimestampSecond"].iloc[last_used_ma_index:]
    new_temp_ma = df_ma["Temperature_Moving_Average"].iloc[last_used_ma_index:]
    new_humid_ma = df_ma["Humidity_Moving_Average"].iloc[last_used_ma_index:]

    ## to save on bandwith and memory, we use 'extendData' feature instead of 'figure'
    ## this way we only send the new data to the client, instead of the entire figure every update
    ## we are adding 4 traces (temp, humid, temp_ma, humid_ma)
    ## and we keep only the last 60 records on the graph
    new_fig_data = [
        dict(
            x=[new_date_ma, new_date_live, new_date_ma, new_date_live],
            y=[new_temp_ma, new_temp, new_humid_ma, new_hum],
        ), [0, 1, 2, 3], 60
    ]
    new_live_data_into = components.style_text(new_temp_ma, new_humid_ma)
    new_stored_indexes = {"df_live_index": recent_live_index, "df_ma_index": recent_ma_index}

    return new_fig_data, new_live_data_into, new_stored_indexes

if __name__ == '__main__':
    app.run_server(debug=False)