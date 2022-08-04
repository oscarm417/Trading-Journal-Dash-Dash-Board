
import pandas as pd 


def init():
    global trade_history_df
    trade_history_df = pd.read_pickle("assets/trade_df.pkl")
    trade_history_df['id'] = trade_history_df.index 
    


