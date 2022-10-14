from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.express as px
from utils.dbx_utils import get_bme_data
from utils.dbx_utils import get_moving_average
from constants import custom_color
import dash_extensions as de



from utils import dbx_utils

url = "https://assets10.lottiefiles.com/packages/lf20_srcvuh0h.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

df1= get_moving_average(Temp_15s_Moving_Average=[],Temp_60s_Moving_Average=[],Humidity_15s_Moving_Average=[],Humidity_60s_Moving_Average=[],TimestampSecond=[])

df = get_bme_data(TempReading=[],HumidityReading=[], EventTimestamp=[],EventDate=[])



x= df.EventTimestamp
y= df.TempReading
a= df.HumidityReading
b= df.EventDate
p= df1.Temp_15s_Moving_Average
q= df1.Temp_60s_Moving_Average
h= df1.Humidity_15s_Moving_Average
g= df1.Humidity_60s_Moving_Average

t= df1.TimestampSecond



resolution = 1000



templine = px.line(df,x=x,y=y,title=f"Temperature vs Time", template='plotly_dark')
humidityline = px.line(df, x=x, y=a, title=f"Humidity vs Time", template='plotly_dark')
temp_magraph= px.line(df1, x=t, y=[p,q], title=f"Temperature Moving Averages", template='plotly_dark')
hum_magraph = px.line(df1, x=t, y=[g,h],title=f"Humidity Moving Averages", template='plotly_dark')
temp_magraph.update_xaxes(rangeslider_visible=True)
hum_magraph.update_xaxes(rangeslider_visible=True)
humtempscatter = px.scatter(df, x=x, y=[y,a], template='plotly_dark')

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


def header(
    app, header_color, header, subheader=None, header_background_color="transparent"
):

    logo = html.Img(src=app.get_asset_url("images/plotly-logo-dark-theme.png"))
    dash_logo = html.A(
        logo,
        href="https://plotly.com/dash/",
        target="_blank",
        className="header-logos-left",
    )

    header = html.Div(
        [
            html.Div(
                [
                    html.Div("Real-Time", style={"color": "#7976F7"}),
                    html.Div(" Dash Apps ", style={"padding": "0px 15px"}),
                    html.Div(" on Databricks", style={"color": "#DB4C39"}),
                ],
                className="header-title",
            ),
            html.Div(subheader, className="subheader-title"),
        ],
        style={"color": header_color},
        className="header-text-middle",
    )

    logo = html.Img(src=app.get_asset_url("images/databricks.png"))
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


LEFT_TAB = html.Div(
    [
        # CROSS FILTER
        dmc.Group(
            direction="column",
            position="center",
            class_name="global-control",
            children=[
                dmc.Title("Temperature and Humidity Related Streams:"),
                 html.Div(
                            id='clientside-contentc',
                            children="Soon data will be here.", 
                            title="Time UTC", 
                            style={'color':'white', 'fontSize':42}  
                            ),
                           html.Div([
                            dcc.Store(
                                id= 'clientside-store-datac', data={}),
                            dcc.Interval(
                                id='serverside-intervalc',
                                interval= 2000, 
                                n_intervals=0),
                            dcc.Interval(
                                id='clientside-intervalc',
                                interval= 2000,
                                n_intervals=0),
                            ]), 
            ],
            
        ),
        # TOP 2 FIGURES
        dmc.Grid(
            gutter="xl",
            children=[
                dmc.Col(
                    span=6,
                    children=html.Div(
                        className="card",
                        children=[
                           html.Div([
                                dcc.Store(
                                    id='graph_store', 
                                    data=dict(x=x,y=y,
                                    resolution=resolution)),
                                dcc.Interval(
                                    id='graph_interval',
                                    interval = 2000, 
                                    n_intervals = 0),
                                dcc.Graph(
                                    id="graph",
                                    figure=templine,
                                    className="glow",
                                    config={"displayModeBar": False},
                                    animate=True,
                                ),
                            ]),
                            html.Div(
                            id='clientside-content',
                            children="Soon data will be here.", 
                            title="Temperature", 
                            style={'color':'white', 'fontSize':42}  
                            ),
                           html.Div([
                            dcc.Store(
                                id= 'clientside-store-data', data={}),
                            dcc.Interval(
                                id='serverside-interval',
                                interval= 1*2000, 
                                n_intervals=0),
                            dcc.Interval(
                                id='clientside-interval',
                                interval= 2000,
                                n_intervals=0),
                            ]),
                        ]),
                    ),
                dmc.Col(
                    span=6,
                    children=html.Div(
                        className="card",
                        children=[
                           html.Div([
                                dcc.Store(
                                    id='temp_magraph_store', 
                                    data=dict(x=x,y=[p,q],
                                    resolution=resolution)),
                                dcc.Interval(
                                    id='temp_magraph_interval',
                                    interval = 1*2000, 
                                    n_intervals = 0),
                                dcc.Graph(
                                    id="temp_magraph",
                                    figure=temp_magraph,
                                    className="glow",
                                    config={"displayModeBar": False},
                                    animate=True,
                                ),
                            ]),
                        ]),
                    ),
            ],
        ),
        dmc.Group(
            direction="column",
            position="center",
            class_name="global-control",
            children=[
                dmc.Title(""),
            ],
        ),
        # TOP 2 FIGURES
        dmc.Grid(
            gutter="xl",
            children=[
                dmc.Col(
                    span=6,
                    children=html.Div(
                        className="card",
                        children=[
                           html.Div([
                                dcc.Store(
                                    id='hgraph_store', 
                                    data=dict(x=x,y=a,
                                    resolution=resolution)),
                                dcc.Interval(
                                    id='hgraph_interval',
                                    interval = 1*2000, 
                                    n_intervals = 0),
                                dcc.Graph(
                                    id="hgraph",
                                    figure=humidityline,
                                    className="glow",
                                    config={"displayModeBar": False},
                                    animate=True,
                                ),
                            ]),
                            html.Div(
                            id='clientside-contentb',
                            children="Soon data will be here.", 
                            title="Humidity", 
                            style={'color':'white', 'fontSize':42}  
                            ),
                           html.Div([
                            dcc.Store(
                                id= 'clientside-store-datab', data={}),
                            dcc.Interval(
                                id='serverside-intervalb',
                                interval= 1*2000, 
                                n_intervals=0),
                            dcc.Interval(
                                id='clientside-intervalb',
                                interval= 2000,
                                n_intervals=0),
                            ]),
                        ]),
                    ),
                  dmc.Col(
                    span=6,
                    children=html.Div(
                        className="card",
                        children=[
                           html.Div([
                                dcc.Store(
                                    id='hum_magraph_store', 
                                    data=dict(x=x,y=[g,h],
                                    resolution=resolution)),
                                dcc.Interval(
                                    id='hum_magraph_interval',
                                    interval = 1*2000, 
                                    n_intervals = 0),
                                dcc.Graph(
                                    id="hum_magraph",
                                    figure=hum_magraph,
                                    className="glow",
                                    config={"displayModeBar": False},
                                    animate=True,
                                ),
                            ]),
                        ]),
                    ),
            ],
        ),
    ],
    className="left-tab",
)

RIGHT_TAB = html.Div(
    [
        # CROSS FILTER
        
    ],
    className="right-tab",
)
    

def notification_line(text):
    return dmc.Notification(
        id="notify-line",
        title="Daily Fitness Data",
        message=[text],
        disallowClose=True,
        radius="xl",
        icon=[DashIconify(icon="simple-icons:databricks", color="#DB4C39", width=128)],
        action="show",
    )

