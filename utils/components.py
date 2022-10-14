from dash import html, dcc
import dash_mantine_components as dmc
from dash iconify import DashIconify

from utils import dbx_utils
from con

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
                    html.Div("Dash", style={"color": "#7976F7"}),
                    html.Div(" with ", style={"padding": "0px 15px"}),
                    html.Div(" Databricks", style={"color": "#DB4C39"}),
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

