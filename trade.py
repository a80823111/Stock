#交易訊號
import mongo
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from operator import itemgetter #itemgetter用來去dict中的key，省去了使用lambda函式
from itertools import groupby #itertool還包含有其他很多函式，比如將多個list聯合起來。。
#取得可分析之股票 (資料完整 , 技術分析指標資料完整)
def get_valid_static_stock():
    startdate = datetime(2020,10,1)
    enddate = datetime.now()

    #取得個股代碼
    stockcodes = mongo.get_stockcode({ '$or':[ { 'Type':'ETF' },{'Type':'股票'}],'$where': 'this.Code.length == 4'  })
    #取得加權
    fmts_query = {
        "日期" : { '$gte':startdate , '$lt':enddate }
    }
    FMTQIKs = mongo.get_FMTQIK(fmts_query)
    #取得個股技術指標
    tis_query = {
        "Date" : { '$gte':startdate , '$lt':enddate },
        "3MA" : { '$exists':True },
        "6MA" : { '$exists':True },
        "10MA" : { '$exists':True },
        "20MA" : { '$exists':True },
        "60MA" : { '$exists':True },
        "Slow_D" : { '$exists':True },
        "Slow_K" : { '$exists':True },
        "Fast_D" : { '$exists':True },
        "Fast_K" : { '$exists':True },
        #"MACD" : { '$exists':True },
        #"MACD_Macdhist" : { '$exists':True },
        #"MACD_Macdsignal" : { '$exists':True },
        "RSI" : { '$exists':True }
    }
    technicalindexs = mongo.get_technicalindex(tis_query)

    #取得個股價格
    sps_query = {
        "Date" : { '$gte':startdate , '$lt':enddate }
    }
    stockprices = mongo.get_stockprice(sps_query)

    #整理資料
    

    stockprices.sort(key=itemgetter('StockCode'))
    technicalindexs.sort(key=itemgetter('StockCode'))

    stockprices_group = groupby(stockprices,itemgetter('StockCode')) 
    technicalindexs_group = groupby(technicalindexs,itemgetter('StockCode')) 

    result = []
    result_stockprices = []
    result_technicalindexs = []

    for key,group in stockprices_group:
        result_stockprices.append({'key':key,'group':list(group)})
        
    for key,group in technicalindexs_group:
        result_technicalindexs.append({'key':key,'group':list(group)})

    for stockcode in stockcodes:     
        sps = [s['group'] for s in result_stockprices if s['key'] == stockcode['Code']]
        tis = [t['group'] for t in result_technicalindexs if t['key'] == stockcode['Code']]

        
        if len(sps) == 0 or len(tis) == 0:
            continue
        print(len(sps[0]))
        print(len(tis[0]))
        print(len(FMTQIKs))
        #檢查是否有漏資料 (比對個股資料數量 & 加權資料數量 & 指標數量)
        if (len(sps[0]) > (len(FMTQIKs) - 5) ) or (len(sps[0]) != len(tis[0])):
            continue

        result.append({
            'StockCode':stockcode['Code'],
            #日期由新到舊排序
            # 'StockPrice':sps.sort(key=itemgetter('Date'),reverse=True),
            # 'TechnicalIndex':tis.sort(key=itemgetter('Date'),reverse=True)
            # 'StockPrice':sps[0].sort(key=itemgetter('Date'),reverse=True),
            # 'TechnicalIndex':tis[0].sort(key=itemgetter('Date'),reverse=True)
            'StockPrice': sorted(sps[0],key=lambda x:['Date'],reverse=True),
            'TechnicalIndex':sorted(tis[0],key=lambda x:['Date'],reverse=True)

        })
    print('vaild static stock count : ' + str(len(result)))
    return result

    
def MA_signal(stocks):
    #MA_Signal , 0:多頭排列 1:空頭排列
    for stock in stocks:
        print('Process MA Signal Stock Code : ' + stock['StockCode'])
        for technicalindex in stock['TechnicalIndex']:
            if technicalindex['3MA'] > technicalindex['6MA'] and technicalindex['6MA'] > technicalindex['10MA'] and technicalindex['10MA'] > technicalindex['20MA'] and technicalindex['20MA'] > technicalindex['60MA']:
                update = {
                    'StockCode' : stock['StockCode'],
                    'Date' : technicalindex['Date'],
                    'MA_Signal' : 0
                }
                mongo.upsert_trade_signal(update)

            if technicalindex['3MA'] < technicalindex['6MA'] and technicalindex['6MA'] < technicalindex['10MA'] and technicalindex['10MA'] < technicalindex['20MA'] and technicalindex['20MA'] < technicalindex['60MA']:
                update = {
                    'StockCode' : stock['StockCode'],
                    'Date' : technicalindex['Date'],
                    'MA_Signal' : 1
                }
                mongo.upsert_trade_signal(update)

#KD趨勢訊號
def KD_trend_signal(stocks):
    #KD_Trend_Signal , 0:向上 1:向下
    for stock in stocks:
        print('Process KD Trend Signal Stock Code : ' + stock['StockCode'])

        KD_type = ['Slow','Fast']
        for index,technicalindex in enumerate(stock['TechnicalIndex']):
            for kdtype in KD_type:
                #取得最近三天資料
                near_data = []
                if kdtype == 'Slow':
                    near_data = [ { 'Date':s['Date'], 'K':s['Slow_K'],'D':s['Slow_D']} for s in stock['TechnicalIndex'][index: index + 3]]
                else:
                    near_data = [ { 'Date':s['Date'],'K':s['Fast_K'],'D':s['Fast_D']} for s in stock['TechnicalIndex'][index: index + 3]]

                #檢查資料是否足夠
                if len(near_data) != 3:
                    continue   
                print(near_data[0]['K'])
                print(near_data[1]['K'])
                print(near_data[2]['K'])
                #向上趨勢 trend = 0
                if near_data[0]['K'] > near_data[1]['K'] > near_data[2]['K'] and near_data[0]['D'] > near_data[1]['D'] > near_data[2]['D']:
                    update = {
                        'StockCode' : stock['StockCode'],
                        'Date' : technicalindex['Date'],
                        kdtype + 'KD_Trend_Signal' : 0
                    }
                    mongo.upsert_trade_signal(update)

                #向下趨勢 trend = 1
                if near_data[0]['K'] < near_data[1]['K'] < near_data[2]['K'] and near_data[0]['D'] < near_data[1]['D'] < near_data[2]['D']:
                    update = {
                        'StockCode' : stock['StockCode'],
                        'Date' : technicalindex['Date'],
                        kdtype + 'KD_Trend_Signal' : 1
                    }
                    mongo.upsert_trade_signal(update)
                
#KD鈍化訊號
def KD_passivation_signal(stocks):
    #KD_Passivation_Signal , 0:高檔鈍化 1:低檔鈍化
    for stock in stocks:
        print('Process KD Passivation Signal Stock Code : ' + stock['StockCode'])

        KD_type = ['Slow','Fast']
        for index,technicalindex in enumerate(stock['TechnicalIndex']):
            for kdtype in KD_type:
                #取得最近三天資料
                near_data = []
                if kdtype == 'Slow':
                    near_data = [ { 'K':s['Slow_K'],'D':s['Slow_D']} for s in stock['TechnicalIndex'][index: index + 3]]
                else:
                    near_data = [ { 'K':s['Fast_K'],'D':s['Fast_D']} for s in stock['TechnicalIndex'][index: index + 3]]

                #檢查資料是否足夠
                if len(near_data) != 3:
                    continue
                          
                #高檔鈍化
                if near_data[0]['K'] > 80 and near_data[1]['K'] > 80 and near_data[2]['K'] > 80 and near_data[0]['D'] > 80 and  near_data[1]['D'] > 80 and near_data[2]['D'] > 80:
                    update = {
                        'StockCode' : stock['StockCode'],
                        'Date' : technicalindex['Date'],
                        kdtype + 'KD_Passivation_Signal' : 0
                    }
                    mongo.upsert_trade_signal(update)

                #低檔鈍化
                if near_data[0]['K'] < 80 and near_data[1]['K'] < 80 and near_data[2]['K'] < 80 and near_data[0]['D'] < 80 and  near_data[1]['D'] < 80 and near_data[2]['D'] < 80:
                    update = {
                        'StockCode' : stock['StockCode'],
                        'Date' : technicalindex['Date'],
                        kdtype + 'KD_Passivation_Signal' : 1
                    }
                    mongo.upsert_trade_signal(update)