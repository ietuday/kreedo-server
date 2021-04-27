
from django.core.serializers import serialize

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
        for week in week_off:
            print("####################",week['monday'])

    except Exception as ex:
        print("Error", ex)
        logger.debug(ex)
        logger.info(ex)
        raise ValidationError(ex)


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
