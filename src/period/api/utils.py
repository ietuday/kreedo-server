
from django.core.serializers import serialize
from django.db.models import Q


from django.core.exceptions import ValidationError
import json

import pdb
from datetime import datetime, timedelta
import calendar
import logging

from holiday.models import*
from kreedo.conf.logger import*

# from holiday.api.serializer import *


""" Create Log for Utils"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)

logger.info("UTILS Period CAlled ")


""" Get All List """
 

def school_holiday(grade_dict):
    print(grade_dict)
   
    try:
        if SchoolHoliday.objects.filter(holiday_from__gte=grade_dict['start_date'], holiday_till__lte=grade_dict['end_date'], academic_session=grade_dict['acad_session'], ).exists():
            school_holiday_count = SchoolHoliday.objects.filter(
                holiday_from__gte=grade_dict['start_date'], holiday_till__lte=grade_dict['end_date'],academic_session=grade_dict['acad_session']).count()

            return school_holiday_count

        else:
            raise ValidationError("Holiday List Not Exist")

    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        raise ValidationError(ex)


def weekday_count(grade, week_off):
    try:
        print("GRADE", grade)
        start_date = datetime.strptime(grade['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(grade['end_date'], '%Y-%m-%d')
        print(start_date, end_date)
        week = {}
        for i in range((end_date - start_date).days):
            day = calendar.day_name[(start_date + timedelta(days=i+1)).weekday()]
            week[day] = week[day] + 1 if day in week else 1
        print("WEEK", week)
        print("WEEK", week_off)
        return calculate_total_week_off_days(week, week_off)

    except Exception as ex:
        print("Error", ex)
        logger.debug(ex)
        logger.info(ex)
        raise ValidationError(ex)


def calculate_total_week_off_days(week, week_off):
    total_weekoff_days = 0
    print("calculate_total_week_off_days Called")

    for wee in week_off:
        print("####################",wee['monday'])
        if wee['monday'] == True:
            total_weekoff_days = total_weekoff_days + week['Monday']

        if wee['tuesday'] == True:
            total_weekoff_days = total_weekoff_days + week['Tuesday']

        if wee['wednesday'] == True:
            total_weekoff_days = total_weekoff_days + week['Wednesday']

        if wee['thursday'] == True:
            total_weekoff_days = total_weekoff_days + week['Thursday']

        if wee['friday'] == True:
            total_weekoff_days = total_weekoff_days + week['Friday']

        if wee['saturday'] == True:
            total_weekoff_days = total_weekoff_days + week['Saturday']

        if wee['sunday'] == True:
            total_weekoff_days = total_weekoff_days + week['Sunday']
    
    print("total_weekoff_days",total_weekoff_days)
    
    return total_weekoff_days


""" Get Weak-off List """


def weakoff_list(grade_dict):
    try:
        print("Called", grade_dict)
        if SchoolWeakOff.objects.filter(academic_session=grade_dict['acad_session']).exists():
            print("WEAKOFF CALLED")
            week_off_list = SchoolWeakOff.objects.filter(
                academic_session=grade_dict['acad_session'])

            qs_json = json.loads(serialize('json', week_off_list))
            print(qs_json)
            response_data = []
            for qs in qs_json:
                print("$$$$$$$$$$$$$$$$$",qs['fields'])
                response_data.append(qs['fields'])
            # print("response_data@@@@@@@@@@@@@@@@", response_data)
            return response_data
        else:
            print("Not Exists")
            raise ValidationError("Weak-Off List Not Exist")

    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        print("ex", ex)
        raise ValidationError(ex)



def total_working_days(grade_dict, count_weekday):
    print("total_working_days")
    try:
        from_date = datetime.strptime(grade_dict['start_date'], '%Y-%m-%d')
        to_date = datetime.strptime(grade_dict['end_date'], '%Y-%m-%d')
        result = to_date - from_date
        resultant_data = (result.days + 1) - count_weekday
        return resultant_data

    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        print("ex", ex)
        raise ValidationError(ex)
 

def create_period(grade_dict):
    print("create_period",grade_dict)
    try:
            from datetime import date, timedelta

            from_date = datetime.strptime(grade_dict['start_date'], '%Y-%m-%d')
            to_date = datetime.strptime(grade_dict['end_date'], '%Y-%m-%d')
            delta = to_date - from_date # as timedelta
            for i in range(delta.days + 1):
                day = from_date + timedelta(days=i)
                print("!!!!!!!!!!!!!!!!!!",day.date())
                day_according_to_date = check_date_day(str(day.date()))
                week_off = weakoff_list(grade_dict)[0]
                print("week off------->", week_off,day_according_to_date)
                day_according_to_date = day_according_to_date.lower()
                for key,value in week_off.items():
                    print("KEY",key)
                    print("VALUE",value)
                    print("$$$$$$$$$$$$$$$$",day_according_to_date)
                    if key == day_according_to_date and value == False:
                        print("Create Period", key, value)
                        """Get Holiday List based on Acad session ----DB Query"""
                        """ Check day.date() is available on Holiday List--- """
                        """ If day.date() is not available on Holiday List then Create Period"""
                        schoolHoliday_count = SchoolHoliday.objects.filter(Q(holiday_from=day.date()) | Q(holiday_from=day.date()), academic_session=grade_dict['acad_session']).count()
                        if schoolHoliday_count == 0:
                            print("Creation")
                            

                    else:
                        print("Not created", key, value)

                

        
    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        print("ex", ex)
        raise ValidationError(ex)


def check_date_day(date):
    day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    day = datetime.strptime(date, '%Y-%m-%d').weekday()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@",day_name[day])
    return day_name[day]

