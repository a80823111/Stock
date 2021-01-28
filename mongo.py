
import pymongo
from pymongo import UpdateOne

client = pymongo.MongoClient(host='localhost', port=27017)
db = client['Stock']
stockcode = db['StockCode']

def upsert_stockcode(value):  
    query = { 
        'Code':value.code
        }

    update = {
        'Code' : value.code,
        'Type' : value.type,
        'Name' : value.name,
        'ISIN' : value.ISIN,
        'ListingDate' : value.start,
        'Market' : value.market,
        'IndustryGroup' : value.group,
        'CFI' : value.CFI
    }

    db.StockCode.update_one(query,{'$set':update} ,upsert=True) 

def delete_stockcode():  
    db.StockCode.delete_many({}) 

def upsert_individual_stockprice(stockcode,value):
    #Data(date=datetime.datetime(2020, 12, 1, 0, 0), capacity=38341265, turnover=18719729411, open=489.5, high=490.0, low=483.5, close=490.0, change=9.5, transaction=24827)
    #capacity 總成交股數 (單位: 股)。
    #turnover 總成交金額 (單位: 新台幣/元)。
    #open 開盤價。
    #high 盤中最高價
    #low 盤中最低價。
    #close 收盤價。
    #change 漲跌價差。
    #transaction 成交筆數。

    query = { 
        'StockCode':stockcode,
        'Date':value.date
        }
    
    update = {
        'StockCode' : stockcode,
        'Date' : value.date,
        'Capacity' : value.capacity,
        'Turnover' : value.turnover,
        'Open' : value.open,
        'High' : value.high,
        'Low' : value.low,
        'Close' : value.close,
        'Change' : value.change,
        'Transaction' : value.transaction
    }

    db.StockPrice.update_one(query,{'$set':update} ,upsert=True) 

def upsert_individual_stockprice_yahoo(value):
    query = { 
        'StockCode':value['StockCode'],
        'Date':value['Date']
        }

    db.StockPrice.update_one(query,{'$set':value} ,upsert=True) 

def get_stockcode(query):
    return list(db.StockCode.find(query))

def get_stockprice(query):
    return list(db.StockPrice.find(query))

def upsert_technicalindex(value):  
    query = { 
        'StockCode':value['StockCode'],
        'Date':value['Date']
        }
    db.TechnicalIndex.update_one(query,{'$set':value} ,upsert=True) 

def upsert_many_technicalindex(values):  
    updates = []

    for value in values:
        query = { 
            'StockCode':value['StockCode'],
            'Date':value['Date']
        }
        updates.append(UpdateOne(query,{'$set':value},upsert=True))

    if len(values) > 0:
        db.TechnicalIndex.bulk_write(updates)
    else:
        print('array is empty')

def get_technicalindex(query):
    return list(db.TechnicalIndex.find(query))

def upsert_MI_5MINS(value):
    query = { 
        '時間':value['時間']
        }

    db.MI_5MINS.update_one(query,{'$set':value} ,upsert=True) 

def upsert_FMTQIK(value):
    query = { 
        '日期':value['日期']
        }

    db.FMTQIK.update_one(query,{'$set':value} ,upsert=True) 

def get_FMTQIK(query):
    return list(db.FMTQIK.find(query))

def get_last_date_FMTQIK():
    return list(db.FMTQIK.find().sort("日期",pymongo.DESCENDING))[0]['日期']   

def upsert_trade_signal(value):  
    query = { 
        'StockCode':value['StockCode'],
        'Date':value['Date']
        }
    db.TradeSignal.update_one(query,{'$set':value} ,upsert=True) 

