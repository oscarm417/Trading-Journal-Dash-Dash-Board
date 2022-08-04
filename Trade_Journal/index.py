# import dash_core_components as dcc
# import dash_html_components as html
from dash import Dash,html, dcc
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
# must add this line in order for the app to be deployed successfully on Heroku
from app import server
from app import app
# import all pages in the app
from apps import Upload, home, tradeHistory, tradeReports, Upload 
# from structures import side_nav_bar 
import settings 
import dash
#
settings.init()

trades_df = settings.trade_history_df.to_dict("records")
print(trades_df)

###################### Navigation Bars ###############################
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    }

side_nav_bar = html.Div(
    [   
        dcc.Store(id = "trade-data",data = trades_df),
        html.Img(
            src = app.get_asset_url("logo.png"),
            id = "plotly-image",
            style = {
                "height": "140px",
                "width": "auto",
                "margin-bottom": "25px",
            },),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Portfolio", href="/", active="exact"),
                dbc.NavLink("Trade History", href="/Trade_History", active="exact"),
                dbc.NavLink("Import Trades", href="/Import_Trades",active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style= SIDEBAR_STYLE,
)

top_nav_bar = dbc.Navbar(
        dbc.Container(
            [
                dbc.Col(dbc.NavbarBrand("", href="#"), sm=3, md=2),
            ],
        ),
        color="dark",
        dark=True,
        )

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
content = html.Div(id="page-content",children = [], style = CONTENT_STYLE)

##################### App Page Layout ################################
app.layout = html.Div(
    [
        #top headerRow
        top_nav_bar,
        side_nav_bar,
        #change output screens
        dcc.Location(id="url"),
        content,
    ]
)

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == "/Trade_History":
        return tradeHistory.layout 
    elif pathname == "/Import_Trades":
        return Upload.layout     
    return dbc.Container(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
                html.Hr(),
                html.H3("Page not found. Heres some guidance",style ={"text-align":"center"}),
                html.Img(
                src = app.get_asset_url("saint_powell.jpg"),
                id = "plotly-image",
                style = {
                    "display":"block",
                    "margin-left":"auto",
                    "margin-right":"auto",
                    "height": "auto",
                    "width": "auto",
                    "margin-bottom": "25px",
                },),
            ]
        )

if __name__ == '__main__':
    app.run_server(debug = True)