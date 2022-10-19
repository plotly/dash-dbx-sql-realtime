import plotly.graph_objects as go

def fig_live(df):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["TimestampSecond"], 
            y=df["MovingAverageTemperature"], 
            name="MA", 
            mode='lines',
            line=dict(color="#DB4C39", width=6),
            hovertemplate="<b>%{y:.1f}°C</b>"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["TimestampSecond"], 
            y=df["Temperature"], 
            name="Temperature", 
            mode='lines',
            line=dict(color="#E26F60", width=2, dash="dash"),
            hovertemplate="<b>%{y:.1f}°C</b>"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["TimestampSecond"], 
            y=df["MovingAverageHumidity"], 
            name="MA", 
            mode='lines',
            line=dict(color="#5452AC", width=6),
            hovertemplate="<b>%{y:.1f}%</b>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["TimestampSecond"], 
            y=df["Humidity"], 
            name="Humidity", 
            mode='lines',
            line=dict(color="#7976F7", width=2, dash="dash"),
            hovertemplate="<b>%{y:.1f}%</b>",
        )
    )

    fig.update_layout(
        title={ "text": f"Live Temperature & Humidity", "x": 0.5, "xanchor": "center", "yanchor": "top"},
        paper_bgcolor="#1c2022", 
        plot_bgcolor="#1c2022", 
        font_color="#A3AAB7", 
        legend_traceorder="reversed", 
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified',
    )
    fig.update_xaxes(gridcolor="#3F3F3F", title="", hoverformat="%H:%M:%S<br>")
    fig.update_yaxes(gridcolor="#3F3F3F", title="")
    
    return fig

