import pandas as pd
import numpy as np 
import datetime
import yfinance as yf 
import plotly.graph_objects as go 
from dateutil import parser


#check if all the uploaded fields are there, if they are calculate 
#return and profit
def format_before_upload(df):
    counter = 0
    calculations = []
    for index,row in df.iterrows():
        target_row = row[['Status','Entry Date','Symbol','Shares','Entry Price','Exit Date','Exit Price']]
        nan_row = target_row.isna().tolist()
        temp = []
        if target_row['Status'] == "Open" and nan_row == [False, False, False, False, False, True, True]:
            counter +=1
            temp = [np.nan]*2
        elif (target_row['Status'] == "Loss" or target_row["Status"] == "Win") and nan_row == [False, False, False, False, False, False, False]:
            counter+=1
            shares = row['Shares']
            entry_total = row['Entry Price'] * shares 
            exit_total = row['Exit Price'] * shares 
            pnl = exit_total - entry_total
            pnl_percent = (pnl/abs(entry_total))*100
            temp = [round(pnl,2),round(pnl_percent,2)]
        else:
            counter +=1
            temp = [np.nan]*2

        calculations.append(temp)


    if type(df) == pd.DataFrame:
        df[['Return $','Return %']] = np.array(calculations,dtype=object)
        return df
    else:
        print('failed i guess')
        return -1
        
def get_trade_series(data,row_index, lookback):
    row = data.iloc[row_index]
    side = "Long" if row['Shares'] >= 0 else "Short"
    start_date = str(row['Entry Date'])[:10]
    end_date = str(row['Exit Date'])[:10]
    data_start_date = parser.parse(start_date) - datetime.timedelta(days = lookback)
    data_end_date = parser.parse(end_date) + datetime.timedelta(days = lookback)
    ticker = row['Symbol']
    trade_series = yf.download(ticker, start = data_start_date,end = data_end_date)
    return trade_series,ticker,start_date, end_date, side


def trade_figure(trade_series,ticker,entry_date, exit_date,side):
    if side == "Long":
        entry = "Buy" 
        exit = "Sell" 
    else:
        entry = "Short" 
        exit = "Cover Short" 

    fig = go.Figure(data = go.Ohlc(
            x = trade_series.index,
            open =trade_series['Open'],
            high = trade_series['Close'],
            low = trade_series['Low'],
            close = trade_series['Close']
        ))

    fig.update_layout(
        title = f'{ticker} {side} Trade',
        title_x = 0.5,
        yaxis_title = "Price",
        xaxis_title = "Date",
        shapes = [
            dict(
                x0= entry_date, x1=entry_date, y0=0, y1=1, xref='x', yref='paper',
                line_width=2),
                dict(
                x0=exit_date, x1=exit_date, y0=0, y1=1, xref='x', yref='paper',
                line_width=2
            )
        ],
        annotations=[
            dict(
                x=entry_date, y=0.05, xref='x', yref='paper',
                showarrow=False, xanchor='left', text=entry
            ),
            dict(
            x=exit_date, y=0.05, xref='x', yref='paper',
            showarrow=False, xanchor='left', text=exit
            )
        ]
        )

    fig.update(layout_xaxis_rangeslider_visible=False)
    return fig 



def plot_win_losses_overtime(df: pd.DataFrame) -> go.Figure:
    df = df[df['Status'] != "Open"]
    df['Return $'] = df['Shares'] *(df['Exit Price'] - df['Entry Price'])
    df['Exit Date'] = df['Exit Date'].apply(lambda x: parser.parse(x[:10]).replace(day = 1))
    wins = df[df['Return $'] >= 0 ].copy()
    losses = df[df['Return $'] <0].copy()
    wins = wins.groupby(by = "Exit Date").sum()
    losses = losses.groupby(by = "Exit Date").sum()
    fig = go.Figure(data=[
    go.Bar(name='Wins',
        x=wins.index.tolist(),
        y=wins['Return $'].tolist(),
        marker_color = "#4CBB17"),
    go.Bar(name='Losses', 
        x=losses.index.tolist(), 
        y=losses['Return $'].tolist(),
        marker_color = "#FF5733 "),
    ])
    # Change the bar mode
    fig.update_layout(
        title = {
            "text": "Wins vs Losses Over Time",
            "x": .5,
            "y": .9,
            "xanchor" : "center",
            "yanchor": "top"
        },
        xaxis_title = "Date",
        yaxis_title = "PnL",
        barmode = "relative",
        )
    return fig



def pnl_over_time_chart(df):
    df = df[df['Status'] != "Open"]
    df['Return $'] = df['Shares'] *(df['Exit Price'] - df['Entry Price'])
    df['Exit Date'] = df['Exit Date'].apply(lambda x: parser.parse(x[:10]).replace(day = 1))
    df = df.groupby(by = 'Exit Date').sum()
    wins = df[df['Return $'] >= 0 ].copy()
    losses = df[df['Return $'] <0].copy()
    wins = wins.groupby(by = "Exit Date").sum()
    losses = losses.groupby(by = "Exit Date").sum()
                
    fig = go.Figure()

    fig.add_trace(go.Bar(x=wins.index.tolist(), y=wins['Return $'].tolist(),
                    base=0,
                    marker_color='chartreuse',
                    name='Wins'
                    ))
    fig.add_trace(go.Bar(x=losses.index.tolist(), y=losses['Return $'].tolist(),
                    marker_color='crimson',
                    name='Losses'))

    fig.update_layout(
        title = {
            "text": "PnL Over Time",
            "x": .5,
            "y": .9,
            "xanchor" : "center",
            "yanchor": "top"
        },
        xaxis_title = "Date",
        yaxis_title = "PnL"
        )
    return fig 
    
def short_long_amounts_over_time(df):
    df = df[df['Status'] != "Open"]
    df['Return $'] = df['Shares'] *(df['Exit Price'] - df['Entry Price'])
    df['Exit Date'] = df['Exit Date'].apply(lambda x: parser.parse(x[:10]).replace(day = 1))
    long = df[df['Shares'] >= 0 ].copy()
    short = df[df['Shares'] <0].copy()
    long['Entry Amount'] = long['Shares'] * long['Entry Price']
    short['Entry Amount'] = short['Shares'] * short['Entry Price']
    long = long.groupby(by = 'Exit Date').sum()
    short = short.groupby(by = 'Exit Date').sum()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=short.index.tolist(), y=short['Entry Amount'].tolist(),
                    base=0,
                    marker_color='crimson',
                    name='Short Dollar Amount'))
    fig.add_trace(go.Bar(x=long.index.tolist(), y=long['Entry Amount'].tolist(),
                    base=0,
                    marker_color='chartreuse',
                    name='Long Dollar Amount'
                    ))
    fig.update_layout(
        title = {
            "text": "Short vs Long Dollar Amounts Over Time",
            "x": .5,
            "y": .9,
            "xanchor" : "center",
            "yanchor": "top",
            
        },
        xaxis_title = "Date",
        yaxis_title = "Dollar Amount",
        barmode = "relative"
            )
    return fig
 

def trades_chart_type_over_time(df):
    df = df[df['Status'] != "Open"]
    df['Return $'] = df['Shares'] *(df['Exit Price'] - df['Entry Price'])
    df['Entry Date'] = df['Exit Date'].apply(lambda x: parser.parse(x[:10]).replace(day = 1))
    longs = df[df['Shares'] >= 0 ].copy()
    shorts = df[df['Shares'] <0].copy()
    longs = longs.groupby(by = 'Entry Date').count()
    shorts = shorts.groupby(by = 'Entry Date').count()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=shorts.index.tolist(), y=shorts['Return $'].tolist(),
                    base=0,
                    marker_color='crimson',
                    name='Shorts'))

    fig.add_trace(go.Bar(x=longs.index.tolist(), y=longs['Return $'].tolist(),
                    base=0,
                    marker_color='chartreuse',
                    name='Longs'
                    ))
    fig.update_layout(
        title = {
            "text": "Number of Trades Over Time",
            "x": .5,
            "y": .9,
            "xanchor" : "center",
            "yanchor": "top"
        },
        xaxis_title = "Date",
        yaxis_title = "Trades",
        )    
    return fig 



def win_rate_pie_chart(df):
    df = df[df['Status'] != "Open"]
    wins = len(df[df['Return $']>=0])
    losses = len(df[df['Return $']<0])
    percentage = round(wins/(wins+losses)*100,2)
    color = "blue" if percentage >=50 else "red"

    fig = go.Figure()
    fig.add_trace(go.Pie(labels=['Win','Loss'], values=[wins, losses], name="Win Rate"))
    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.7, hoverinfo="label+percent+name")

    fig.update_layout(
        title_text="Win Rate",
        # Add annotations in the center of the donut pies.
        annotations=[
            dict(text=f'{percentage}%',
            x=0.5, y=0.5,
            font_size=15, 
            showarrow=False,
            font = dict(color = "blue")
            )])
    fig.update_layout(
        title = {
            "text" : "Win Rate",
            "x": .5,
            "y": .9,
            "xanchor": "center",
            "yanchor" : "top",
        },
        width = 450,
        height = 400,
        )
    return fig 