
import requests
import csv 
from datetime import datetime, timedelta
import time

import settings
import compute_tool
#下載個股股價資料
def download_individual_stock(stockcode,startdate,enddate):
    #https://query1.finance.yahoo.com/v7/finance/download/2330.TW?period1=0&period2=1549258857&interval=1d&events=history&crumb=hP2rOschxO0
    #日期轉成 timestamp
    startdate_timestamp = datetime.timestamp(startdate)
    enddate_timestamp = datetime.timestamp(enddate)
    url = 'https://query1.finance.yahoo.com/v7/finance/download/{stockcode}.TW?period1={startdate_timestamp}&period2={enddate_timestamp}&interval=1d&events=history&crumb=hP2rOschxO0'
    url =  url.format(stockcode=stockcode,startdate_timestamp=startdate_timestamp,enddate_timestamp=enddate_timestamp)
    print(url)
    response = requests.post(url)
    rows = csv.reader(response.text.splitlines(), delimiter=',')

    print('download 個股股價資料 date : ' + str(startdate) + ' ~ ' + str(enddate))

    result = []
    for row in enumerate(rows):
        print(row)
        break
        data = row[1]
        try:
            datetime.strptime("%Y-%m-%d",data[0])
        except:
            continue

        result.append({
                'StockCode' : stockcode,
                'Date' : datetime.strptime("%Y-%m-%d",data[0]),
                'Open' : data[1],
                'High' : data[2],
                'Low' : data[3],
                'Close' : data[4],
                'Volume' : data[5]
            })
        print(len(result))
            
    return result

#加權每5秒委託成交統計
def download_MI_5MINS(date):
    url = 'https://www.twse.com.tw/exchangeReport/MI_5MINS?response=csv&date=' + datetime.strftime(date,'%Y%m%d')

    # 下載股價
    time.sleep(settings.twse_sleeptime)
    response = requests.post(url)
    rows = csv.reader(response.text.replace('=','').splitlines(), delimiter=',')

    print('download MI_5MINS (加權每5秒委託成交統計) date : ' + str(date))

    result = []
    for row in enumerate(rows):
        data = row[1]
        try:
            time.strptime(data[0], "%H:%M:%S")
        except:
            continue

        result.append({
                '時間': compute_tool.nowtime_to_datetime(date,data[0]),
                '累積委託買進筆數':data[1],
                '累積委託買進數量':data[2],
                '累積委託賣出筆數':data[3],
                '累積委託賣出數量':data[4],
                '累積成交筆數':data[5],
                '累積成交數量':data[6],
                '累積成交金額':data[7]
            })
            
    return result

#加權市場成交資訊
def download_FMTQIK(date):
    #https://www.twse.com.tw/zh/page/trading/exchange/FMTQIK.html
    url = 'https://www.twse.com.tw/exchangeReport/FMTQIK?response=csv&date=' + datetime.strftime(date,'%Y%m%d')
    # 下載股價
    time.sleep(settings.twse_sleeptime)
    response = requests.post(url)
    rows = csv.reader(response.text.replace('=','').splitlines(), delimiter=',')

    print('download MI_5MINS (加權市場成交資訊) date : ' + str(date))

    result = []
    for row in enumerate(rows):
        data = row[1]
        try:
            compute_tool.convert_republic_of_china_date(data[0])
        except:
            continue

        result.append({
                '日期': compute_tool.convert_republic_of_china_date(data[0]),
                '成交股數':data[1],
                '成交金額':data[2],
                '成交筆數':data[3],
                '發行量加權股價指數':data[4],
                '漲跌點數':data[5]
            })
            
    return result

