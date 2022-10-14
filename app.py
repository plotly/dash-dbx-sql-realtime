import dash
import dash_html_components as html
import dash_core_components as dcc
import numpy as np
from pip import main
import plotly.express as px
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
from dash import callback
from dash.dependencies import Input, Output, State
from utils.dbx_utils import get_bme_data
from utils.dbx_utils import get_moving_average
from constants import custom_color
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash_daq as daq






from dash.dependencies import Input, Output

app_start_ts = dt.datetime.now()


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
#fig = px.line(df,x=x,y=y)
templine = px.line(df,x=x,y=y)
humidityline = px.line(df, x=x, y=a)
temp_magraph= px.line(df1, x=t, y=[p,q])
hum_magraph = px.line(df1, x=t, y=[h,g])



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('BME 280 Sensor Data from Simulated Raspberry Pi'),
    html.H5('Temperature'),
    html.Div(
        id='clientside-content', children="Soon data will be here.", title="temperature"   
    ),
    html.Div([
        dcc.Store(id='graph_store', data=dict(x=x,y=y,resolution=resolution)),
        dcc.Interval(id='graph_interval',interval = 1*2000, n_intervals = 0),   
        dcc.Graph(id= 'graph',figure=templine, animate=True),
    ]),
    html.H5('Humidity'),
    html.Div(
        id='clientside-contentb', children="Soon data will be here.",title="time"
    ),
    html.Div([
        dcc.Store(id='hgraph_store', data=dict(x=x,y=a,resolution=resolution)),
        dcc.Interval(id='hgraph_interval',interval = 1*2000, n_intervals = 0),   
        dcc.Graph(id= 'hgraph',figure=humidityline, animate=True),
    ]),
    html.H5('Time'),
    html.Div(
        id='clientside-contentc', children="Soon data will be here.",title="humidity"
    ),
        html.Div([
        dcc.Store(id='temp_magraph_store', data=dict(x=t,y=[p,q],resolution=resolution)),
        dcc.Interval(id='temp_magraph_interval',interval = 1*2000, n_intervals = 0),   
        dcc.Graph(id= 'temp_magraph',figure= temp_magraph, animate=True),
    ]),
        html.Div([
        dcc.Store(id='hum_magraph_store', data=dict(x=t,y=[g,h],resolution=resolution)),
        dcc.Interval(id='hum_magraph_interval',interval = 1*2000, n_intervals = 0),   
        dcc.Graph(id= 'hum_magraph',figure= hum_magraph, animate=True),
    ]),
    html.H5('Date'),
    html.Div(
        id='clientside-contentd', children="Soon data will be here.",title="Id"
    ),
    dcc.Store(
        id='clientside-store-data', data={}
    ),
    dcc.Interval(
        id='serverside-interval',
        interval= 1*2000,
        n_intervals=0
    ),
    dcc.Interval(
        id='clientside-interval',
        n_intervals=0,
        interval= 1*2000
    ),
    dcc.Store(
        id='clientside-store-datab', data={}
    ),
    dcc.Interval(
        id='serverside-intervalb',
        interval= 1*2000,
        n_intervals=0
    ),
    dcc.Interval(
        id='clientside-intervalb',
        n_intervals=0,
        interval= 1*2000
    ),
    dcc.Store(
        id='clientside-store-datac', data={}
    ),
    dcc.Interval(
        id='serverside-intervalc',
        interval= 1*2000,
        n_intervals=0
    ),
    dcc.Interval(
        id='clientside-intervalc',
        n_intervals=0,
        interval=1*2000
    ),
     dcc.Store(
        id='clientside-store-datad', data={}
    ),
    dcc.Interval(
        id='serverside-intervald',
        interval=1*2000,
        n_intervals=0
    ),
    dcc.Interval(
        id='clientside-intervald',
        n_intervals=0,
        interval=1*2000
    )
])

#Clientside callback

@app.callback(Output('graph', 'extendData'),
             [Input('graph_interval', 'n_intervals')])
def update_data(n_intervals):
    index= n_intervals % resolution
    return dict(x=[[x[index]]], y=[[y[index]]]), [0], 10

@app.callback(Output('hgraph', 'extendData'),
             [Input('hgraph_interval', 'n_intervals')])
def update_data(n_intervals):
    index= n_intervals % resolution
    return dict(x=[[x[index]]], y=[[a[index]]]), [0], 10

@app.callback(Output('temp_magraph', 'extendData'),
             [Input('temp_magraph_interval', 'n_intervals')])
def update_data(n_intervals):
    index= n_intervals % resolution
    return dict(x=[[t[index]]], y=[[q[index]],p[index]]), [0], 10

@app.callback(Output('hum_magraph', 'extendData'),
             [Input('hum_magraph_interval', 'n_intervals')])
def update_data(n_intervals):
    index= n_intervals % resolution
    return dict(x=[[t[index]]], y=[[g[index]],h[index]]), [0], 10

@app.callback(
     Output('clientside-store-data', 'data'),
     Input('serverside-interval', 'n_intervals'),
 )
def update_store_data(n_intervals):
     last_row = n_intervals*100
     stored_data = df.iloc[0:last_row]
     return stored_data.to_dict('records')


app.clientside_callback(
     """
     function(n_intervals, data) {
         if(data[n_intervals] === undefined) {
             return '';
         }
         return data[n_intervals]['TempReading'];
     }
     """,
     Output('clientside-content', 'children'),
     Input('clientside-interval','n_intervals'),
     State('clientside-store-data', 'data'),
 )

@app.callback(
     Output('clientside-store-datab', 'data'),
     Input('serverside-intervalb', 'n_intervals'),
 )
def update_store_data(n_intervals):
     last_row = n_intervals*100
     stored_data = df.iloc[0:last_row]
     return stored_data.to_dict('records')


app.clientside_callback(
     """
     function(n_intervals, data) {
         if(data[n_intervals] === undefined) {
             return '';
         }
         return data[n_intervals]['HumidityReading'];
     }
     """,
     Output('clientside-contentb', 'children'),
     Input('clientside-intervalb','n_intervals'),
     State('clientside-store-datab', 'data'),
 )

@app.callback(
     Output('clientside-store-datac', 'data'),
     Input('serverside-intervalc', 'n_intervals'),
 )
def update_store_data(n_intervals):
     last_row = n_intervals*100
     stored_data = df.iloc[0:last_row]
     return stored_data.to_dict('records')


app.clientside_callback(
     """
     function(n_intervals, data) {
         if(data[n_intervals] === undefined) {
             return '';
         }
         return data[n_intervals]['EventTimestamp'];
     }
     """,
     Output('clientside-contentc', 'children'),
     Input('clientside-intervalc','n_intervals'),
     State('clientside-store-datac', 'data'),
 )

@app.callback(
     Output('clientside-store-datad', 'data'),
     Input('serverside-intervald', 'n_intervals'),
 )
def update_store_data(n_intervals):
     last_row = n_intervals*100
     stored_data = df.iloc[0:last_row]
     return stored_data.to_dict('records')


app.clientside_callback(
     """
     function(n_intervals, data) {
         if(data[n_intervals] === undefined) {
             return '';
         }
         return data[n_intervals]['EventDate'];
     }
     """,
     Output('clientside-contentd', 'children'),
     Input('clientside-intervald','n_intervals'),
     State('clientside-store-datad', 'data'),
 )



if __name__ == '__main__':
    app.run_server(debug=True, port=5559)
