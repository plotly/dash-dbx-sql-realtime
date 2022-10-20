import dash
from dash import html, dcc
import dash_mantine_components as dmc
import pandas as pd

import utils.figures as figs
from utils.dbx_utils import df_live, df_ma

app_description = {
    "headers": [
        "Databricks as a Data Warehouse",
        "Fast Query, Computation, & Retrieval of Databricks Data",
        "Gateway to Sophisticated Data Science",
    ],
    "texts": [
        "for simple to advanced python analytical workflows",
        "at scale and in REAL TIME via Plotly Dash analytical web applications",
        "for simple to advanced python analytical workflows",
    ],
}

def layout():
    return dmc.MantineProvider(
    withGlobalStyles=True,
    theme={"colorScheme":"dark"},
    children=dmc.NotificationsProvider(
        html.Div([
            header(header_color="#FFFFFF", header_background_color="#111014",),
            create_text_columns(app_description, "description"),
            graph_view(),
            
            dcc.Interval(id='live-data-interval', interval = 5100, n_intervals=0 ),
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
    fig_live = figs.fig_live(df_live, df_ma)
    recent_live_index = df_live.tail(1).index[0]
    recent_ma_index = df_ma.tail(1).index[0]

    print("================== app start:", recent_live_index, recent_ma_index)

    return html.Div(
        className="graph-view",
        children=html.Div(
            className="card",
            children=[
                ## figure
                dcc.Graph(
                    id="live-data-graph",
                    figure=fig_live,
                    className="glow",
                    config={"displayModeBar": False},
                    animate=True,
                ),
                
                ## current-time information
                html.Div( id='live-data-information'),
                dcc.Store(id='store-data', data={"df_live_index": recent_live_index, "df_ma_index": recent_ma_index}),
            ]
        )
    )

def style_text(temperature, humidity, time):
    return html.Div([
        html.Div(f"Temperature: {temperature}°C", style={"color": "#DB4C39", 'fontSize':32}),
        html.Div(f"{time} GMT", style={'color':'grey', 'fontSize':26}),
        html.Div(f"Humidity: {humidity}%", style={"color": "#7976F7", 'fontSize':32}),
    ], style={"display": "flex", "justify-content": "space-between"}),