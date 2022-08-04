
from dash import Dash, html, dcc
import dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px




app = Dash(__name__,
        external_stylesheets=[
        dbc.themes.BOOTSTRAP,
         {
        'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
        'crossorigin': 'anonymous'
        },
        ],
        suppress_callback_exceptions=True
)

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
content = html.Div(id="page-content",children = [], style = CONTENT_STYLE)

server = app.server
app.config.suppress_callback_exceptions = True