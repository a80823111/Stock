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
stock.update_stockcode()

#----更新全部加權市場成交資訊----
stock.update_FMTQIK()

#----更新個股最新價格資料----
stock.update_individual_stockprice()

#----更新全部加權每5秒委託成交統計----
stock.update_MI_5MINS()

