# Stock
功能 : 爬取股價資料並提供進出買賣的訊號

開發工具 : Python3.7 <br>
資料庫 :　MongodDb <br>
資料來源 : 直接爬取證交所網站 或 twstock(python package)  <br>
Package :  <br>
    talib, <br>
    pymongo, <br>
    twstock, <br>
    datetime, <br>
    requests, <br>
    csv, <br>
    dateutil.relativedelta, <br>
    calendar, <br>
    operator, <br>
    itertools, <br>
    numpy, <br>
    pandas, <br>
    matplotlib.pyplot <br>


檔案說明 <br>
process開頭的為main program <br>
process_history.py #爬取歷史資料 <br>
process_newst_price.py  #爬取最新的股價資料 <br>
process_technicalindex.py  #計算技術指標 <br>
process_trade.py  #交易策略 (未開發) <br>
 <br>
compute_tool.py #計算工具 <br>
download.py #下載檔案 (證交所的資料) <br>
mongo.py #操作MongoDB的封裝 <br>
settings.py #設定檔 <br>
stock.py #股票相關的工具 <br>
technicalindex.py  #技術指標相關 <br>
trade.py #交易策略 , 信號(未開發) <br>
