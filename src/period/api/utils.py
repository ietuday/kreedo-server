
from django.core.serializers import serialize
from django.db.models import Q


from django.core.exceptions import ValidationError
import json

import pdb
from datetime import datetime, timedelta , date, time
import calendar
import logging

from holiday.models import*
from kreedo.conf.logger import*
from .serializer import*
from ..models import *
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
        start_date = datetime.strptime(grade['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(grade['end_date'], '%Y-%m-%d')
        week = {}
        for i in range((end_date - start_date).days):
            day = calendar.day_name[(start_date + timedelta(days=i+1)).weekday()]
            week[day] = week[day] + 1 if day in week else 1
        return calculate_total_week_off_days(week, week_off)

    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        raise ValidationError(ex)


def calculate_total_week_off_days(week, week_off):
    total_weekoff_days = 0

    for wee in week_off:
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
    
    
    return total_weekoff_days


""" Get Weak-off List """


def weakoff_list(grade_dict):
    try:
        if SchoolWeakOff.objects.filter(academic_session=grade_dict['acad_session']).exists():
            week_off_list = SchoolWeakOff.objects.filter(
                academic_session=grade_dict['acad_session'])

            qs_json = json.loads(serialize('json', week_off_list))
            response_data = []
            for qs in qs_json:
                response_data.append(qs['fields'])
            return response_data
        else:
            raise ValidationError("Weak-Off List Not Exist")

    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        raise ValidationError(ex)



def total_working_days(grade_dict, count_weekday):
    try:
        from_date = datetime.strptime(grade_dict['start_date'], '%Y-%m-%d')
        to_date = datetime.strptime(grade_dict['end_date'], '%Y-%m-%d')
        result = to_date - from_date
        resultant_data = (result.days + 1) - count_weekday
        return resultant_data

    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        raise ValidationError(ex)
 

def create_period(grade_dict):
    try:
            from datetime import date, timedelta

            from_date = datetime.strptime(grade_dict['start_date'], '%Y-%m-%d')
            to_date = datetime.strptime(grade_dict['end_date'], '%Y-%m-%d')
            delta = to_date - from_date # as timedelta
            for i in range(delta.days + 1):
                day = from_date + timedelta(days=i)
                day_according_to_date = check_date_day(str(day.date()))
                week_off = weakoff_list(grade_dict)[0]
                day_according_to_date = day_according_to_date.lower()
                for key,value in week_off.items():
                    if key == day_according_to_date and value == False:
                        schoolHoliday_count = SchoolHoliday.objects.filter(Q(holiday_from=day.date()) | Q(holiday_from=day.date()), academic_session=grade_dict['acad_session']).count()
                        if schoolHoliday_count == 0:
                            period_list = PeriodTemplateDetail.objects.filter(academic_session=grade_dict['acad_session'], days=day_according_to_date.upper())
                        
                            period_dict = {}
                        
                            for period in period_list:
                            
                                period_dict['academic_session'] = [period.academic_session.id]
                                period_dict['subject'] = period.subject.id
                                period_dict['room'] = period.room.id
                                period_date = day.date()
                                period_time =  period.start_time
                                period_dict['start_date'] = period_date
                                period_dict['end_date'] = period_date
                                period_dict['start_time'] = period.start_time
                                period_dict['end_time'] = period.end_time
                                period_dict['type'] = period.type
                                period_dict['is_active'] = "True"
 
                                p_qs = Period.objects.filter(start_date= period_dict['start_date'], end_date= period_dict['end_date'], start_time=period_dict['start_time'], end_time=period_dict['end_time']).count()
                                if p_qs == 0:
                                    period_serializer = PeriodCreateSerializer(data=period_dict)
                                    if period_serializer.is_valid():
                                        period_serializer.save()
                                    else:
                                        raise ValidationError(period_serializer.errors)
                                else:
                                    print("EXITS")


    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        
        raise ValidationError(ex)


def check_date_day(date):
    day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    day = datetime.strptime(date, '%Y-%m-%d').weekday()
    return day_name[day]

