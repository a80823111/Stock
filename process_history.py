import pymongo
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import calendar
import twstock

import stock
import technicalindex

#----更新股票產品代碼----
stock.update_stockcode()

#----更新個股全部價格資料----
stock.update_all_individual_stockprice()

#----更新全部加權市場成交資訊----
stock.update_all_FMTQIK()

#----更新全部加權每5秒委託成交統計----
stock.update_all_MI_5MINS()








