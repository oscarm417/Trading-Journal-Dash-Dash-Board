from gc import callbacks
import dash
from dash import html, dcc, dash_table, no_update  
import dash_bootstrap_components as dbc
import settings
from dash.dependencies import Input, Output, State
import pandas as pd 
from app import app
from dash.exceptions import PreventUpdate
import tools.data_tools as data_tools 



initial_active_cell = {"row": 0, "column": 0, "column_id": "Status", "row_id": 0}


layout = html.Div(
    [
    html.H1(
        'Your Trades',
        style= {
            "text-align": "center"
        },
    ),
    html.Br(),
    html.H4("Review your trades"),
    html.H5('Click on a trade below'),
    html.Br(),
    html.Div(
        [   
            html.Div(id = "output-graph-trade"),
            dash_table.DataTable(
                id='datatable',
                data = settings.trade_history_df.to_dict("records"),
                columns = [ 
                    {"name":i,"id":i} for i in settings.trade_history_df.columns
                    if i != 'id'
                ],
                page_size = 10,
                sort_action= "native",
                active_cell=initial_active_cell
            )
        ])
    ]
)

@app.callback(
    Output('datatable','data'),
    Input("trade-data","data"))
def clear_table_output(data):
    df = pd.DataFrame(data)
    if len(df) > 0:
        df = df[df['Status']!= "Open"]
        return df.to_dict("records")
    return data

@app.callback(
    Output("output-graph-trade","children"),
    Input("datatable","active_cell"),
    Input("trade-data","data")
)
def trade_row_clicked(active_cell,data):
    if active_cell is None:
        raise no_update
    print(active_cell)
    df = pd.DataFrame(data)
    df['id'] = df.index
    df = df[df['Status']!= "Open"]
    row_index = active_cell['row']
    trade_series, ticker, entry_date, exit_date, side =  data_tools.get_trade_series(df,row_index,100)
    fig = data_tools.trade_figure(trade_series,ticker, entry_date, exit_date,side)
    print(ticker, entry_date, exit_date, side)
    return dcc.Graph(figure = fig)



