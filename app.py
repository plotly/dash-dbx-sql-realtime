from datetime import datetime
from dash import Dash, html, dcc, Input, Output, callback
import dash_mantine_components as dmc

import utils.components as comp
import utils.dbx_utils as utils
from constants import app_description


app = Dash(
    __name__,
    title="Realtime Dash-DBX", 
    update_title=None,
)
server = app.server

app.layout = dmc.MantineProvider(
    withGlobalStyles=True,
    theme={"colorScheme":"dark"},
    children=dmc.NotificationsProvider(
        html.Div([
            comp.header(header_color="#FFFFFF", header_background_color="#111014",),
            comp.create_text_columns(app_description, "description"),
            comp.graph_view(),
            
            dcc.Interval(id='daily-data-interval', interval = 10_000, n_intervals=0 ),
            dcc.Interval(id='live-data-interval', interval = 1000, n_intervals=0 ),
        ])
    )
)

def style_text(temperature, humidity):
    return html.Div([
        html.Div([
            html.Div(f"Temperature: {temperature}°C", style={"color": "#7976F7"}),
            html.Div(f"Humidity: {humidity}%", style={"color": "#DB4C39"}),
        ], style={"display": "flex", "justify-content": "space-between"}),
    ])


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
    ], style_text(new_temp, new_humidity)


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
