from django.db.models import Q

from holiday.models import*
from django.core.exceptions import ValidationError
from kreedo.conf.logger import*
import logging


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


from datetime import datetime
import pdb

def days_caculate(holiday_list, grade_dict):
    pass
    
   


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
