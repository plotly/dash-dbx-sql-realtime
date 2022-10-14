import plotly.express as px 
from constants import custom_color

def fig_style(fig):
    return (
        fig.update_layout(
            paper_bgcolor="#1c2022", plot_bgcolor="#1c2022", font_color="#A3AAB7"
        )
        .update_xaxes(gridcolor="#3F3F3F")
        .update_yaxes(gridcolor="#3F3F3F")
    )

def create_empty(text):
    layout = dict(
        autosize=True,
        annotations=[dict(text=text, showarrow=False)],
        paper_bgcolor="#1c2022",
        plot_bgcolor="#1c2022",
        font_color="#A3AAB7",
        font=dict(color="FFFF", size=20),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
    )
    return {"data": [], "layout": layout}

def generate_line(df, temperature, comp):
    axis_labels = {
        "temperature": "Temperature",
        "enqueuedTimeUtc": "Time"
    }
    fig = px.line(
        df,
        x="time",
        y="temperature",
        color=comp,
        color_discrete_sequence=custom_color[comp],
        markers=True,
        labels={"temperature": axis_labels[temperature]},
        title= "Temperature vs Time",
    )
    return fig_style(fig)

