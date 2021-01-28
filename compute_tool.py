from datetime import datetime, timedelta
import time

#計算漲幅百分比
def percent(origin,target):
    try:
        return ((target - origin) / origin) * 100
    except:
        return 0.0

#更新指定日期的時分秒
def nowtime_to_datetime(nowdate,time):  
    time_array = time.split(':')
    nowdate = nowdate.replace(hour=int(time_array[0]),minute=int(time_array[1]),second=int(time_array[2]))
    return nowdate 

#民國日期轉西園日期 format 109/01/01 to 2020/01/01
def convert_republic_of_china_date(date_str):
    date_str_array = date_str.split('/')

    year = int(date_str_array[0]) + 1911
    month = int(date_str_array[1])
    day = int(date_str_array[2])

    return datetime(year,month,day)

