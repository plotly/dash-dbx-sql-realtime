from datetime import datetime
from dash import Dash, html, dcc, Input, Output, callback
import dash_mantine_components as dmc

import utils.components as components
import utils.dbx_utils as utils


app = Dash(
    __name__,
    title="Realtime Dash-DBX", 
    update_title=None,
)
app.layout = components.layout
server = app.server




@callback(
    Output("daily-data-graph", "extendData"),
    Output("daily-data-information", "children"),
    Input("daily-data-interval", "n_intervals"),
)
def update_daily_datah(n):
    new_date, new_temp, new_humidity = utils.get_new_daily_data_offline(n)
    return [
        dict(
            x=[[new_date], [new_date]],
            y=[[new_temp], [new_humidity]],
        ), [0, 1], 48
    ], components.style_text(new_temp, new_humidity)


@callback(
    Output("live-data-graph", "extendData"),
    Output("live-data-information", "children"),
    Input("live-data-interval", "n_intervals"),
)
def update_live_data(n):
    new_date, new_temp, new_humidity = utils.get_new_live_data_offline()
    return [
        dict(
            x=[[new_date], [new_date]],
            y=[[new_temp], [new_humidity]],
        ), [0, 1], 60
    ], datetime.now().strftime("%H:%M:%S")

if __name__ == '__main__':
    app.run_server(debug=True)
