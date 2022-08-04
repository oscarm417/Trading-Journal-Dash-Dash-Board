import dash
import pandas as pd 
import numpy as np 
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import settings
from app import app
import tools.data_tools as data_tools

# dash.register_page(__name__, path='/')

layout = html.Div(
    children=[
    html.H1(
        children='Portfolio Page',
        style={
            "text-align":"center",
        }),

    dbc.Container([
        #left side of the screen
        dbc.Col( [ 
            dbc.Row([
                dash_table.DataTable(
                    id = "open_trade_table",
                    style_table = {'overflowX':'auto'},
                    style_cell = {
                        'height': 'auto',
                        'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                        'whiteSpace': 'normal'
                    },
                    data = settings.trade_history_df.to_dict("records"),
                    columns = [
                        {"name":i,"id":i} for i in settings.trade_history_df.columns
                        if i!= "id"  
                        if i != "Exit Price"
                        if i !="Exit Date"
                        if i != "Status"
                        if i != "Side"
                        if i != "Return %"
                    ]
                ),
                html.Div(id = "trade_statistics"),
            ]),
            dbc.Row([
                dbc.Col(id = "win_losses_time"),
                dbc.Col(id = "pnl_over_months"),
            ]),
            dbc.Row([
                dbc.Col(id = "short_long_amount_traded_over_time"),
                dbc.Col(id = "number_of_trades_per_month")
            ])
        ]),
        dbc.Col([ 
            dbc.Row(id = "pnl_chart"),
            # dbc.Row(id = "trade_statistics"),
            dbc.Row(id = "strategy_pnl_comparison"),
            dbc.Row(id = "strategy_win_rage_comparison"),
            dbc.Row(id = "average_win_per_strategy"),
            dbc.Row(id = "strategy_table_comparison")

        ]),
    ]),
    ]
)



@app.callback(
    Output('open_trade_table','data'),
    Input("trade-data","data"))
def clear_table_output(data):
    df = pd.DataFrame(data)
    if len(df) > 0:
        df = df[df['Status']== "Open" ]
        return df.to_dict("records")
    return data



@app.callback(
    Output("win_losses_time","children"),
    Input("trade-data","data")
)
def win_losses_time_chart(data):
    df = pd.DataFrame(data)
    fig = data_tools.plot_win_losses_overtime(df)
    return dcc.Graph(figure = fig)


@app.callback(
Output("pnl_over_months","children"),
Input("trade-data","data")
)
def pnl_over_months_chart(data):
    df = pd.DataFrame(data)
    fig = data_tools.pnl_over_time_chart(df)
    return dcc.Graph(figure = fig)


@app.callback(
Output("short_long_amount_traded_over_time","children"),
Input("trade-data","data")
)
def pnl_over_months_chart(data):
    df = pd.DataFrame(data)
    fig = data_tools.short_long_amounts_over_time(df)
    return dcc.Graph(figure = fig)


@app.callback(
Output("trade_statistics","children"),
Input("trade-data","data")
)
def pnl_over_months_chart(data):
    df = pd.DataFrame(data)
    fig = data_tools.win_rate_pie_chart(df)
    return dcc.Graph(figure = fig)