from dash import Dash, Input, Output, State, callback
from datetime import datetime

import utils.components as components
import utils.dbx_utils as utils

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
    new_date, new_temp, ma_temp_avg, ma_temp, new_humidity, ma_humid_avg, ma_humid  = utils.get_new_live_data_offline(storage["ma_temp"], storage["ma_humid"])
    time = datetime.now().strftime("%H:%M:%S")
    return [
        dict(
            x=[[new_date], [new_date], [new_date], [new_date]],
            y=[[new_temp], [ma_temp_avg], [new_humidity], [ma_humid_avg]],
        ), [0, 1, 2, 3], 60
    ], components.style_text(new_temp, new_humidity, time), {"ma_temp": ma_temp, "ma_humid": ma_humid}

if __name__ == '__main__':
    app.run_server(debug=True)
