import pandas as pd
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import base64
import datetime
import io
from app import app
import dash
import tools.data_tools as data_tools
import settings 
from dash.exceptions import PreventUpdate
import yfinance as yf 

df = 0 
# dash.register_page(__name__)

layout =  html.Div(
        [   html.H1("File Upload\n",style = {
                "text-align":"center"
            }
                ),
            html.H4("Please upload your Excel or CSV file\n",
                style = {
                    "text-align":"center",
                }),
            html.H3("Must have the following columns:\n",
                style = {
                    "text-align":"center",
                }),
            html.Hr(),
            dbc.Row([
                dbc.Col(
                        html.Div(
                    [   html.H5("Columns with a * are mandatory"),
                        html.Li("Entry Date*: MM/DD/YYY"),
                        html.Li("Symbol*: Stock Ticker"),
                        html.Li("Shares*: Number of Shares Bought or (Sold)"),
                        html.Li("Entry Price*"),
                        html.Li("Exit Date: MM/DD/YYY"),
                        html.Li("Exit Price"),
                        html.Li("Strategy: Strategy Name Tag"),                
                    ],),
                ),
                dbc.Col(
                    html.Div([
                        html.H3("Example:",style = {"text-align":"left"}),
                        html.Img(
                            src = app.get_asset_url("example_file_upload.PNG"),
                            id = "plotly-image",
                            style = {
                                "height":"auto",
                                "width":"auto",
                                "margin-right":"250px"
                            }
                        )
                    ]),
                )
            ],
            align="center"
            ),
            html.Hr(),
            html.Div([ # this code section taken from Dash docs https://dash.plotly.com/dash-core-components/upload
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
                html.Div(id="status-of-upload"),
                html.Div(id='output-datatable'),
                
            ])
        ],
    )



def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    global df
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        dbc.Button("Submit", id ="submit-button"),
        html.Hr(),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=15
        ),
        dcc.Store(id='stored-data', data=df.to_dict('records')),
        html.Hr(),  # horizontal line
    ])


@app.callback(Output('output-datatable', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children

@app.callback(
    [Output('status-of-upload','children'),
    Output("trade-data","data")],
    Input('submit-button','n_clicks'))
def clear_table_output(n_clicks):
    global df
    if n_clicks  is None:
        raise PreventUpdate
    if n_clicks == 1:
        df = data_tools.format_before_upload(df)
        print(type(df))
        if type(df) == int:
            return html.Div([
                html.H3("Error Uploading: Mandatory Fields Missing",
                style = {
                'text-align':'center',
                "color":"Red"
                })
            ]), settings.trade_history_df.to_dict("records")
        elif type(df) == pd.DataFrame:
            settings.trade_history_df = settings.trade_history_df.append(df)
            return html.Div(
                html.H3("Succesfully uploaded",
                style = {
                    'text-align':'center',
                    "color":"green"
                })
            ), settings.trade_history_df.to_dict("records")

