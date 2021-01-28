import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as datetime
from talib import abstract
from operator import itemgetter

import mongo


def MA(stockcode,stockprices,ma_days):
    #matype 0:SMA 1:EMA (反應快) , MA用SMA
    stockprices_df = convert_stockprices_to_talibformat(stockprices)

    ma = abstract.MA(stockprices_df, timeperiod=ma_days, matype=0)

    updates = []
    for index,stockprice in enumerate(stockprices):  
        update = {
                'StockCode' : stockprice['StockCode'],
                'Date' : stockprice['Date'],
                str(ma_days) + 'MA' : ma[index]
        }    

        if not np.isnan(ma[index]):
            updates.append(update)
            #mongo.upsert_technicalindex(update)
    mongo.upsert_many_technicalindex(updates)
    
    print('update ' + stockcode + ' ' + str(ma_days) + 'MA')
        

def KD(stockcode,stockprices):
    #matype 0:SMA 1:EMA (反應快) , KD用EMA
    stockprices_df = convert_stockprices_to_talibformat(stockprices)

    #較慢的KD slowk slowd
    kd = abstract.STOCH(stockprices_df,fastk_period=9,slowk_period=3, slowk_matype=1,slowd_period=3,slowd_matype=1)
    #較快的KD fastk fastd
    kdf = abstract.STOCHF(stockprices_df,fastk_period=9, fastd_period=3,fastd_matype=1)

    updates = []

    for index,stockprice in enumerate(stockprices):      
        update_kd = {
                'StockCode' : stockprice['StockCode'],
                'Date' : stockprice['Date'],
                'Slow_K' : kd['slowk'][index],
                'Slow_D' : kd['slowd'][index]
        }

        #if not np.isnan(kd['slowk'][index]) and not np.isnan(kd['slowd'][index]):
        updates.append(update_kd)

        update_kdf = {
                'StockCode' : stockprice['StockCode'],
                'Date' : stockprice['Date'],
                'Fast_K' : kdf['fastk'][index],
                'Fast_D' : kdf['fastd'][index]
        }

        #if not np.isnan(kdf['fastk'][index]) and not np.isnan(kdf['fastd'][index]):
        updates.append(update_kdf)


    mongo.upsert_many_technicalindex(updates)
    print('update ' + stockcode + ' KD')


def MACD(stockcode,stockprices):
    stockprices_df = convert_stockprices_to_talibformat(stockprices)
    macd = abstract.MACD(stockprices_df)

    updates = []
    for index,stockprice in enumerate(stockprices):  
        update = {
                'StockCode' : stockprice['StockCode'],
                'Date' : stockprice['Date'],
                'MACD' : macd['macd'][index],
                'MACD_Macdsignal' : macd['macdsignal'][index],
                'MACD_Macdhist' : macd['macdhist'][index],
        }

        if not np.isnan(macd['macd'][index]) and not np.isnan(macd['macdsignal'][index]) and not np.isnan(macd['macdhist'][index]):
            updates.append(update)
            #mongo.upsert_technicalindex(update)

    mongo.upsert_many_technicalindex(updates)
    print('update ' + stockcode + ' MACD')

def RSI(stockcode,stockprices):
    stockprices_df = convert_stockprices_to_talibformat(stockprices)
    rsi = abstract.RSI(stockprices_df,timeperiod=12)

    updates = []
    for index,stockprice in enumerate(stockprices):  
        update = {
                'StockCode' : stockprice['StockCode'],
                'Date' : stockprice['Date'],
                'RSI' : rsi[index]
        }

        if not np.isnan(rsi[index]):
            updates.append(update)
            mongo.upsert_technicalindex(update)

    mongo.upsert_many_technicalindex(updates)
    print('update ' + stockcode + ' RSI')


def convert_stockprices_to_talibformat(stockprices):  
    s_dict = {
        'open': [s['Open'] for s in stockprices],
        'high': [s['High'] for s in stockprices],
        'low': [s['Low'] for s in stockprices],
        'close': [s['Close'] for s in stockprices],
        'volume': [s['Capacity'] for s in stockprices]
    }

    return pd.DataFrame(s_dict)

