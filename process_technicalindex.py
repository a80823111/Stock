from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import calendar
import twstock
import threading

import stock
import technicalindex
import settings

#----計算個股技術指標----
#取得全部個股價格資料
stockprices = stock.get_all_individual_stockprice()
threads = []
for stockprice in stockprices:

    stock_threads = []

    stock_threads.append(threading.Thread(target = technicalindex.MA(stockprice['StockCode'],stockprice['StockPrice'],3)))
    stock_threads.append(threading.Thread(target = technicalindex.MA(stockprice['StockCode'],stockprice['StockPrice'],6)))
    stock_threads.append(threading.Thread(target = technicalindex.MA(stockprice['StockCode'],stockprice['StockPrice'],10)))
    stock_threads.append(threading.Thread(target = technicalindex.MA(stockprice['StockCode'],stockprice['StockPrice'],20)))
    stock_threads.append(threading.Thread(target = technicalindex.MA(stockprice['StockCode'],stockprice['StockPrice'],60)))

    stock_threads.append(threading.Thread(target = technicalindex.KD(stockprice['StockCode'],stockprice['StockPrice'])))
    stock_threads.append(threading.Thread(target = technicalindex.MACD(stockprice['StockCode'],stockprice['StockPrice'])))
    stock_threads.append(threading.Thread(target = technicalindex.RSI(stockprice['StockCode'],stockprice['StockPrice'])))

    for st in stock_threads:
        st.start()

    threads.append(stock_threads)

print('join thread')
for t in threads:
    for st in t:
        st.join()


