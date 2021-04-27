from django.db.models import Q
from django.core.exceptions import ValidationError


import pdb
import datetime
import calendar
import logging

from holiday.models import*
from kreedo.conf.logger import*


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
            school_holiday_count = SchoolHoliday.objects.filter(
                holiday_from__gte=grade_dict['start_date'], holiday_till__lte=grade_dict['end_date'],academic_session=grade_dict['acad_session'])
            
            print("Holiday count----->",school_holiday_count)
            raise ValidationError("Holiday List Not Exist")

    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        raise ValidationError(ex)



def weekday_count(grade):
    try:
        print("GRADE", grade)
        start_date  = datetime.datetime.strptime(start, '%Y-%m-%d')
        end_date    = datetime.datetime.strptime(end, '%Y-%m-%d')
        week        = {}
        for i in range((end_date - start_date).days):
            day       = calendar.day_name[(start_date + datetime.timedelta(days=i+1)).weekday()]
            week[day] = week[day] + 1 if day in week else 1
        print("WEEK", week)
        return week

    except Exception as ex:
        print("Error", ex)
        logger.debug(ex)
        logger.info(ex)
        raise ValidationError(ex)



    





""" Get Weak-off List """


def weakoff_list(acadmic_session):
    try:
        print("Called", acadmic_session)
        if SchoolWeakOff.objects.filter(academic_session=acadmic_session).exists():
            print("WEAKOFF CALLED")
            weakoff_list = SchoolWeakOff.objects.filter(
                academic_session=acadmic_session)

            for weak_off in weakoff_list:
                print("Weak off", weak_off)
            return weakoff_list
        else:
            print("Not Exists")
            raise ValidationError("Weak-Off List Not Exist")

    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        print("ex", ex)
        raise ValidationError(ex)
