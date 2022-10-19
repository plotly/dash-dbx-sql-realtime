import plotly.express as px 

def fig_style(fig):
    name_list=["Temperature", "Humidity"]
    for i,trace in enumerate (fig.data):
        trace.update(name=name_list[i])

    return (
        fig.update_layout(
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
            )
        )
        .update_xaxes(gridcolor="#3F3F3F")
        .update_yaxes(gridcolor="#3F3F3F")
    )

def fig_daily(df):
    fig = px.line(
        df,
        x=df["EventTimestamp"],
        y=[df["TempReading"], df["HumidityReading"]],
        color_discrete_sequence=["#DB4C39", "#7976F7"],
        markers=True,
        labels= {"EventTimestamp": "Time", "HumidityReading": "Humidity", "TempReading": "Temperature"},
        title= f"Daily Temperature & Humidity",
    )
    return fig_style(fig)


def fig_live(df):
    fig = px.line(
        df,
        x=df["TimestampSecond"],
        y=[df["Temp_15s_Moving_Average"], df["Temp_60s_Moving_Average"]],
        color_discrete_sequence=["#DB4C39", "#7976F7"],
        markers=True,
        labels= {"TimestampSecond": "Time"},
        title= f"Live Temperature & Humidity",
    )
    return fig_style(fig)

