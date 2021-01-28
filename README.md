# Stock
功能 : 爬取股價資料並提供進出買賣的訊號

開發工具 : Python3.7 <br>
資料庫 :　MongodDb
資料來源 : 直接爬取證交所網站 或 twstock(python package),
Package : 
    talib,
    pymongo,
    twstock,
    datetime,
    requests,
    csv,
    dateutil.relativedelta,
    calendar,
    operator,
    itertools,
    numpy,
    pandas,
    matplotlib.pyplot


檔案說明
process開頭的為main program
process_history.py #爬取歷史資料
process_newst_price.py  #爬取最新的股價資料
process_technicalindex.py  #計算技術指標
process_trade.py  #交易策略 (未開發)


compute_tool.py #計算工具
download.py #下載檔案 (證交所的資料)
mongo.py #操作MongoDB的封裝
settings.py #設定檔
stock.py #股票相關的工具
technicalindex.py  #技術指標相關
trade.py #交易策略 , 信號(未開發)
