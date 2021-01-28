import twstock
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import csv 
from io import StringIO
from operator import itemgetter #itemgetter用來去dict中的key，省去了使用lambda函式
from itertools import groupby #itertool還包含有其他很多函式，比如將多個list聯合起來。。

import mongo
import settings
import compute_tool
import download

#取得資料股票代碼所有資訊
#(type='股票', code='2330', name='台積電', ISIN='TW0002330008', start='1994/09/05', market='上市', group='半導體業', CFI='ESVUFR')
#股票代碼4碼(2330) , 權證代碼6碼(03699P)

#更新股票產品代碼
def update_stockcode():
    #更新更新 TPEX 跟 TWSE 的列表
    twstock.__update_codes()
    sources = twstock.codes
    #移除股票產品代碼
    mongo.delete_stockcode()

    for index in sources:
        #sources[index]
        #(type='股票', code='2330', name='台積電', ISIN='TW0002330008', start='1994/09/05', market='上市', group='半導體業', CFI='ESVUFR')
        print('update code : '+ sources[index].code)
        mongo.upsert_stockcode(sources[index])

#更新個股全部價格資料
def update_all_individual_stockprice():
    #individual_stocks = mongo.get_stockcode({ '$where': 'this.Code.length == 4' })
    individual_stocks = mongo.get_stockcode({ '$or':[ { 'Type':'ETF' },{'Type':'股票'}],'$where': 'this.Code.length == 4'  })
    
    for stock in individual_stocks:     
        startdate = datetime.strptime(stock['ListingDate'], "%Y/%m/%d")
        startdate = startdate.replace(day=1)
        #抓2019以後的資料
        if startdate < settings.history_limit_startdate:
            startdate = settings.history_limit_startdate
            

        while startdate <= settings.today:
            #已有資料的不再更新
            stockprices = mongo.get_stockprice({ 'StockCode': stock['Code'],'Date':{'$gte':startdate,'$lt': (startdate + relativedelta(months=+1))} })
            if len(stockprices) > 0 :
                startdate = startdate + relativedelta(months=+1)
                continue
           
            print('update code with history price : '+ stock['Code'] + ' , date : ' + str(startdate))

            price_source = twstock.stock.Stock(stock['Code'],initial_fetch=False)
            #將資料讀出來
            time.sleep(settings.twse_sleeptime)
            price_datas = price_source.fetch(startdate.year, startdate.month)

            print('update code with history price : '+ stock['Code'] + ' , date : ' + str(startdate))
            for price_data in price_datas: 
                mongo.upsert_individual_stockprice(stock['Code'],price_data)

            startdate = startdate + relativedelta(months=+1)

#更新個股最新價格資料
def update_individual_stockprice():
    individual_stocks = mongo.get_stockcode({ '$or':[ { 'Type':'ETF' },{'Type':'股票'}],'$where': 'this.Code.length == 4'  })
    startdate = settings.today
    print(startdate)
    for stock in individual_stocks:   
        #已有資料的不再更新
        stockprices = mongo.get_stockprice({ 'StockCode': stock['Code'],'Date':settings.today })
        if len(stockprices) > 0 :
            continue

        time.sleep(settings.twse_sleeptime)
        print('update code with new price : '+ stock['Code'])
        #True 抓取最近31天
        price_source = twstock.stock.Stock(stock['Code'],initial_fetch=False)
        #將資料讀出來
        price_datas = price_source.fetch(startdate.year, startdate.month)

        for price_data in price_datas:
            mongo.upsert_individual_stockprice(stock['Code'],price_data)



#取得全部個股價格資料
def get_all_individual_stockprice():
    startdate = settings.history_limit_startdate

    result = []
    stockprice_query = {
        '$where': 'this.StockCode.length == 4',
        'Date':{'$gte':startdate},
        'Open': { '$ne':None },
        'High': { '$ne':None },
        'Low': { '$ne':None },
        'Close': { '$ne':None },
        'Capacity': { '$ne':None }
    }
    stockprice = mongo.get_stockprice(stockprice_query)

    stockprice.sort(key=itemgetter('StockCode'))
    stock_group = groupby(stockprice,itemgetter('StockCode')) 

    for key,group in stock_group:
        g_list = list(group)
        if len(g_list) > 0:
            g_list.sort(key=itemgetter('Date'),reverse=False)
            result.append({ 'StockCode' : key,'StockPrice':g_list })

    
    return result
        

#更新全部加權每5秒委託成交統計
def update_all_MI_5MINS():
    startdate = settings.history_limit_startdate

    while startdate <= settings.today:
        data = download.download_MI_5MINS(startdate)

        for d in data:
            mongo.upsert_MI_5MINS(d)
        startdate = startdate + relativedelta(days=+1)


#更新加權每5秒委託成交統計
def update_MI_5MINS():
    data = download.download_MI_5MINS(settings.today)

    for d in data:
        mongo.upsert_MI_5MINS(d)

#更新全部加權市場成交資訊
def update_all_FMTQIK():
    startdate = settings.history_limit_startdate

    while startdate <= settings.today:
        data = download.download_FMTQIK(startdate)
        for d in data:
            mongo.upsert_FMTQIK(d) 
        startdate = startdate + relativedelta(months=+1)

#更新加權市場成交資訊
def update_FMTQIK():
    data = download.download_FMTQIK(datetime.now())

    for d in data:
        mongo.upsert_FMTQIK(d)


