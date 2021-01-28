from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import mongo
#爬取證交所資料睡眠時間
twse_sleeptime = 9

#歷史資料起始時間限制
history_limit_startdate = datetime(2019,1,1)

#今天日期 (最後開市日期)
#today = datetime.now() + relativedelta(days=-1)
today = mongo.get_last_date_FMTQIK()
#這個月第一天
today_month = today.replace(day=1)