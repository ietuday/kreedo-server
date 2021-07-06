from datetime import date, timedelta, datetime
from collections import OrderedDict

    
import calendar
from datetime import *

from holiday.models import*
from holiday.api.utils import*

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
        date1 = datetime.strptime(str(start_date), "%d-%m-%Y")
        date2 = datetime.strptime(str(end_date), "%d-%m-%Y")
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
import traceback

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

def checkWeekOff(checkdate, weekoff):
    if len(weekoff)!=0:
        intDay = checkdate.weekday()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        print(days[intDay])
        week_off = weekoff[0]
        print(weekoff)
        return week_off[days[intDay]]
    else: 
        return ""

def months_by_month(months,generated_month_list):
    print(len(generated_month_list))
    try:
        for mon in months:
            pass
            # yield date1 + timedelta(n)
    except Exception as Ex:
        print(Ex) 


def covert_month_by_month(month):
    pass

def calculate_working_days(month, year,date, request_data):
    try:
        total_no_of_days = calendar.monthrange(year,month)[1]
        date_range_by_month = get_month_day_range(date)
        print(request_data['calendar_type'])
        if request_data['calendar_type'] == 'school-calender':
            school_holiday_count = SchoolHoliday.objects.filter(holiday_from__lte=date_range_by_month['first_day'], holiday_till__gte=date_range_by_month['first_day'], school=request_data['school']).count()
            print("####",school_holiday_count)
            working_days = total_no_of_days - school_holiday_count
        elif request_data['calendar_type'] == 'academic-session-calendar':                                                                                                                               
            school_holiday_count = SchoolHoliday.objects.filter(holiday_from__lte=date_range_by_month['first_day'], holiday_till__gte=date_range_by_month['first_day'], academic_calender=request_data['academic_calendar']).count()
            print("####",school_holiday_count)
            working_days = total_no_of_days - school_holiday_count
        elif request_data['calendar_type'] == 'section-calendar':
            acadamic_session_qs = AcademicSession.objects.filter(grade=request_data['grade'], section=request_data['section'])
            school_holiday_count = SchoolHoliday.objects.filter(holiday_from__lte=date_range_by_month['first_day'], holiday_till__gte=date_range_by_month['first_day'], academic_session=acadamic_session_qs[0].id).count()
            print("####",school_holiday_count)
            working_days = total_no_of_days - school_holiday_count
        
        return working_days

    except Exception as Ex:
        print(Ex)
        print(traceback.print_exc())



def get_month_day_range(date):
    """
    For a date 'date' returns the start and end date for the month of 'date'.

    Month with 31 days:
    >>> date = datetime.date(2011, 7, 27)
    >>> get_month_day_range(date)
    (datetime.date(2011, 7, 1), datetime.date(2011, 7, 31))

    Month with 28 days:
    >>> date = datetime.date(2011, 2, 15)
    >>> get_month_day_range(date)
    (datetime.date(2011, 2, 1), datetime.date(2011, 2, 28))
    """
    first_day = date.replace(day = 1)
    last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])
    return {"first_day": first_day, "last_day": last_day}



