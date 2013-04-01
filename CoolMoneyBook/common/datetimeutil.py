#!/usr/bin/python 
''''' 
Filename: "utildate.py" 
author:   "zhangsong" 
date  :   "2009-03-24" 
version:  "1.00" 
''' 
from time import strftime, localtime 
from datetime import datetime, timedelta, date
import calendar 
  
year = strftime("%Y",localtime()) 
month  = strftime("%m",localtime()) 
day  = strftime("%d",localtime()) 
hour = strftime("%H",localtime()) 
min  = strftime("%M",localtime()) 
sec  = strftime("%S",localtime()) 
  
  
def today(): 
    ''''' 
    get today,date format="YYYY-MM-DD" 
    ''' 
    return date.today() 
  
def todaystr(): 
    ''''' 
    get date string 
    date format="YYYYMMDD" 
    ''' 
    return year+month+day 
  
def datetime(): 
    ''''' 
    get datetime,format="YYYY-MM-DD HH:MM:SS" 
    ''' 
    return strftime("%Y-%m-%d %H:%M:%S",localtime()) 
  
def datetimestr(): 
    ''''' 
    get datetime string 
    date format="YYYYMMDDHHMMSS" 
    ''' 
    return year+month+day+hour+min+sec 
  
def getdayofday(begindate=date.today, n=0): 
    ''''' 
    if n>=0,date is larger than today 
    if n<0,date is less than today 
    date format = "YYYY-MM-DD" 
    ''' 
    if(n<0): 
        n = abs(n) 
        return begindate-timedelta(days=n) 
    else: 
        return begindate+timedelta(days=n) 
  
def getdaysofmonth(year,mon): 
    ''''' 
    get days of month 
    ''' 
    return calendar.monthrange(year, mon)[1] 
  
def getfirstdayofmonth(year,mon): 
    ''''' 
    get the first day of month 
    date format = "YYYY-MM-DD" 
    ''' 
    days="01" 
    if(int(mon)<10): 
        mon = "0"+str(int(mon)) 
    arr = (year,mon,days) 
    return "-".join("%s" %i for i in arr) 
  
def getlastdayofmonth(year,mon): 
    ''''' 
    get the last day of month 
    date format = "YYYY-MM-DD" 
    ''' 
    days=calendar.monthrange(year, mon)[1] 
    mon = addzero(mon) 
    arr = (year,mon,days) 
    return "-".join("%s" %i for i in arr) 
  
def get_firstday_month(n=0): 
    ''''' 
    get the first day of month from today 
    n is how many months 
    ''' 
    (y,m,d) = getyearandmonth(n) 
    d = "01" 
    arr = (y,m,d) 
    return "-".join("%s" %i for i in arr) 
  
def get_lastday_month(n=0): 
    ''''' 
    get the last day of month from today 
    n is how many months 
    ''' 
    return "-".join("%s" %i for i in getyearandmonth(n)) 
   
def get_today_month(n=0): 
    ''''' 
    get last or next month's today 
    n is how many months 
    date format = "YYYY-MM-DD" 
    ''' 
    (y,m,d) = getyearandmonth(n) 
    arr=(y,m,d) 
    if(int(day)<int(d)): 
        arr = (y,m,day) 
    return "-".join("%s" %i for i in arr) 
  
def getyearandmonth(n=0): 
    ''''' 
    get the year,month,days from today 
    befor or after n months 
    ''' 
    thisyear = int(year) 
    thismon = int(month) 
    totalmon = thismon+n 
    if(n>=0): 
        if(totalmon<=12): 
            days = str(getdaysofmonth(thisyear,totalmon)) 
            totalmon = addzero(totalmon) 
            return (year,totalmon,days) 
        else: 
            i = totalmon/12 
            j = totalmon%12 
            if(j==0): 
                i-=1 
                j=12 
            thisyear += i 
            days = str(getdaysofmonth(thisyear,j)) 
            j = addzero(j) 
            return (str(thisyear),str(j),days) 
    else: 
        if((totalmon>0) and (totalmon<12)): 
            days = str(getdaysofmonth(thisyear,totalmon)) 
            totalmon = addzero(totalmon) 
            return (year,totalmon,days) 
        else: 
            i = totalmon/12 
            j = totalmon%12 
            if(j==0): 
                i-=1 
                j=12 
            thisyear +=i 
            days = str(getdaysofmonth(thisyear,j)) 
            j = addzero(j) 
            return (str(thisyear),str(j),days) 
  
def addzero(n): 
    ''''' 
    add 0 before 0-9 
    return 01-09 
    ''' 
    nabs = abs(int(n)) 
    if(nabs<10): 
        return "0"+str(nabs) 
    else: 
        return nabs 

import datetime

# input datetime1, and an month offset
# return the result datetime
def datetime_offset_by_month(datetime1, n = 1):
    # create a shortcut object for one day
    one_day = datetime.timedelta(days = 1)

    # first use div and mod to determine year cycle
    q,r = divmod(datetime1.month + n, 12)

    # create a datetime2
    # to be the last day of the target month
    datetime2 = datetime.datetime(
        datetime1.year + q, r + 1, 1, datetime1.hour, datetime1.minute, datetime1.second) - one_day

    # if input date is the last day of this month
    # then the output date should also be the last
    # day of the target month, although the day
    # may be different.
    # for example:
    # datetime1 = 8.31
    # datetime2 = 9.30
    if datetime1.month != (datetime1 + one_day).month:
        return datetime2

    # if datetime1 day is bigger than last day of
    # target month, then, use datetime2
    # for example:
    # datetime1 = 10.31
    # datetime2 = 11.30
    if datetime1.day >= datetime2.day:
        return datetime2

    # then, here, we just replace datetime2's day
    # with the same of datetime1, that's ok.
    return datetime2.replace(day = datetime1.day)