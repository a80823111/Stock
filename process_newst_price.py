import pymongo
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import calendar
import twstock

import stock
import technicalindex
import settings

#stock.test()
#----更新股票產品代碼----
#stock.update_stockcode()

#----更新全部加權市場成交資訊----
#stock.update_FMTQIK()

#----更新個股最新價格資料----
stock.update_individual_stockprice()

#----更新全部加權每5秒委託成交統計----
#stock.update_MI_5MINS()

#----計算個股技術指標----
#取得全部個股價格資料
#stockprices = stock.get_all_individual_stockprice()

#取得指定日期內個股價格資料
#stockprices = stock.get_daterange_individual_stockprice()


# for stockprice in stockprices:
#     technicalindex.MA(stockprice['StockCode'],stockprice['StockPrice'],3)
#     technicalindex.MA(stockprice['StockCode'],stockprice['StockPrice'],5)
#     technicalindex.MA(stockprice['StockCode'],stockprice['StockPrice'],6)
#     technicalindex.MA(stockprice['StockCode'],stockprice['StockPrice'],10)
#     technicalindex.MA(stockprice['StockCode'],stockprice['StockPrice'],20)
#     technicalindex.MA(stockprice['StockCode'],stockprice['StockPrice'],60)
#     technicalindex.MA(stockprice['StockCode'],stockprice['StockPrice'],120)
#     technicalindex.MA(stockprice['StockCode'],stockprice['StockPrice'],240)
 
#     technicalindex.KD(stockprice['StockCode'],stockprice['StockPrice'])

#     technicalindex.MACD(stockprice['StockCode'],stockprice['StockPrice'])
#     technicalindex.RSI(stockprice['StockCode'],stockprice['StockPrice'])

#stock.update_MI_5MINS()