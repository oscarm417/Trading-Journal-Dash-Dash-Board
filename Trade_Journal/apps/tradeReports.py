import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

win_rate = 0 
lose_rate = 0 

# over_all_trade_statistics_table = {
#     'Win %': win_rate,
#     'Loss %': lose_rate,
#     'Average Win': average_win,
#     'Average_loss': average_loss,
#     'Sharpe Ratio': Sharpe_Ratio,
#     'Total Trades': total_trades,
#     'Total Long Trades': long_trades,
#     'Total Short Trades': short_trades,
#     }

layout = html.Div(
    [
    html.H1(
        'Trade Statistics',
        style = {
            "text-align": "center"
        },
    ),
    html.Br(),
    dbc.Container(
        [
            dbc.Row([
                dbc.Tab
            ])
        ]
    )


    ]
)