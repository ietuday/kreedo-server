from datetime import date, timedelta, datetime
from collections import OrderedDict

    
import calendar
from datetime import *

""" Genarte list of dates """
def Genrate_Date_of_Year(start_date, end_date):
    try:
        sdate = start_date   # start date
        edate = end_date  # end date

        delta = edate - sdate       # as timedelta
        date_list =[]
       
        for i in range(delta.days + 1):
            date_dict = {}
            day = sdate + timedelta(days=i)
            print("DAY-------->",day)
            date_dict['date'] = day
            week=check_date_day(day)
            print("name-------------",week)
            date_dict['week_name'] = week
            date_list.append(date_dict)

        
        return date_list

    except Exception as ex:
        print("UTIL ERROR ------->", ex)


def check_date_day(date):
    day_name = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = datetime.strptime(str(date), '%Y-%m-%d').weekday()
    return day_name[day]



""" Genrate List of month """
def Genrate_Month(start_date, end_date):
    try:
        date1 = datetime.strptime(str(start_date), "%Y-%m-%d")
        date2 = datetime.strptime(str(end_date), "%Y-%m-%d")
        date1 = date1.replace(day = 1)
        date2 = date2.replace(day = 1)
        months_str = calendar.month_name
        months = []
        while date1 <= date2:
            month = date1.month
            year  = date1.year
            month_str = months_str[month][0:3]
            months.append("{0}-{1}".format(month_str,str(year)))
            next_month = month+1 if month != 12 else 1
            next_year = year + 1 if next_month == 1 else year
            date1 = date1.replace( month = next_month, year= next_year)
        return months


    except Exception as ex:
        print("ERROR", ex)



from datetime import timedelta, date

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def checkFirstDay(date):
    if date.day == 1:
        return True
    else:
        return False

def checkHoliday(date, holiday_list):
    for holiday in holiday_list:
        start = datetime.strptime(holiday['holiday_from'], '%Y-%m-%d').date()
        end = datetime.strptime(holiday['holiday_till'], '%Y-%m-%d').date()
        if start <= date <= end:
            return True
        else:
            return False


def checkHolidayType(date, holiday_list):
    for holiday in holiday_list:
        start = datetime.strptime(holiday['holiday_from'], '%Y-%m-%d').date()
        end = datetime.strptime(holiday['holiday_till'], '%Y-%m-%d').date()
        if start <= date <= end:
            return holiday['holiday_type']['holiday_type']
        else:
            return ''


def checkHolidayColor(date, holiday_list):
    for holiday in holiday_list:
        start = datetime.strptime(holiday['holiday_from'], '%Y-%m-%d').date()
        end = datetime.strptime(holiday['holiday_till'], '%Y-%m-%d').date()
        if start <= date <= end:
            return holiday['holiday_type']['color_code']
        else:
            return ''


def checkStartEndDate(date1, date2):
    # date2 = datetime.strptime(date2, '%d-%m-%Y').date()
    print(date1, date2)
    # date1 = date1.date()
    print(date1, date2)
    if date1 == date2:
        return True
    else:
        return False


