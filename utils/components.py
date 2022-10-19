from hashlib import new
import dash
from dash import html, dcc
import dash_mantine_components as dmc
import pandas as pd

from utils.dbx_utils import get_new_daily_data_offline, get_new_live_data_offline
import utils.figures as figs
from constants import app_description

# from utils.dbx_utils import get_immediate_vals, get_moving_average
# df_live= get_moving_average()
# df_daily = get_immediate_vals()

def layout():
    return dmc.MantineProvider(
    withGlobalStyles=True,
    theme={"colorScheme":"dark"},
    children=dmc.NotificationsProvider(
        html.Div([
            header(header_color="#FFFFFF", header_background_color="#111014",),
            create_text_columns(app_description, "description"),
            graph_view(),
            
            dcc.Interval(id='daily-data-interval', interval = 10_000, n_intervals=0 ),
            dcc.Interval(id='live-data-interval', interval = 1000, n_intervals=0 ),
        ])
    )
)

def create_text_columns(data_dict, class_name=None):
    """Create element that creates header + text column for every header and text in the list"""
    width = {"width": str(100 / len(data_dict["headers"])) + "%"}
    return html.Div(
        [
            html.Div([html.H3(header), html.P(text)], style=width)
            for header, text in zip(data_dict["headers"], data_dict["texts"])
        ],
        className="text-columns" + (f" {class_name}" if class_name else ""),
    )

def header(header_color, header_background_color="transparent"):

    logo = html.Img(src=dash.get_asset_url("images/plotly-logo-dark-theme.png"))
    dash_logo = html.A(
        logo,
        href="https://plotly.com/dash/",
        target="_blank",
        className="header-logos-left",
    )

    header = html.Div([
        html.Div(
            [
                html.Div("Real-Time", style={"color": "#7976F7"}),
                html.Div(" Dash Apps on ", style={"padding": "0px 15px"}),
                html.Div("Databricks", style={"color": "#DB4C39"}),
            ],
            className="header-title",
        )],
        style={"color": header_color},
        className="header-text-middle",
    )

    logo = html.Img(src=dash.get_asset_url("images/databricks.png"))
    databricks_logo = html.A(
        logo,
        href="https://databricks.com/",
        target="_blank",
        className="header-logos-right",
    )

    return html.Div(
        [dash_logo, header, databricks_logo],
        className="header",
        style={"background-color": header_background_color},
    )


def graph_view():

    new_daily_data = []
    for i in range(48):
        new_daily_data.insert(0, get_new_daily_data_offline(i, generate_past_data=True))
    df_daily = pd.DataFrame(new_daily_data, columns=["EventTimestamp", "TempReading", "HumidityReading"])
    fig_daily = figs.fig_daily(df_daily)

    new_live_data = []
    for i in range(60):
        new_live_data.insert(0, get_new_live_data_offline(i, generate_past_data=True))
    df_live = pd.DataFrame(new_live_data, columns=["TimestampSecond", "Temp_15s_Moving_Average", "Temp_60s_Moving_Average"])
    fig_live = figs.fig_live(df_live)

    return html.Div(
    className="graph-view",
    children=[
        # 2 FIGURES
        dmc.Grid(
            gutter="xl",
            children=[

                ## left figure
                dmc.Col(
                    span=6,
                    children=html.Div(
                        className="card",
                        children=[

                            ## figure
                            html.Div([
                                dcc.Graph(
                                    id="daily-data-graph",
                                    figure=fig_daily,
                                    className="glow",
                                    config={"displayModeBar": False},
                                    animate=True,
                                ),
                            ]),
                            ## temperature-humidity information
                            html.Div(
                                id='daily-data-information',
                                style={'color':'white', 'fontSize':42}  
                            ),
                        ]
                    ),
                ),

                ## right figure
                dmc.Col(
                    span=6,
                    children=html.Div(
                        className="card",
                        children=[
                            ## figure
                            html.Div([
                                dcc.Graph(
                                    id="live-data-graph",
                                    figure=fig_live,
                                    className="glow",
                                    config={"displayModeBar": False},
                                    animate=True,
                                ),
                            ]),
                            
                            ## current-time information
                            html.Div(
                                id='live-data-information',
                                style={'color':'#7976F7', 'fontSize':42, 'textAlign':'center'}  
                            ),
                        ]
                    ),
                ),
            ],
        ),
    ],
)

def style_text(temperature, humidity):
    return html.Div([
        html.Div([
            html.Div(f"Temperature: {temperature}°C", style={"color": "#7976F7"}),
            html.Div(f"Humidity: {humidity}%", style={"color": "#DB4C39"}),
        ], style={"display": "flex", "justify-content": "space-between"}),
    ])