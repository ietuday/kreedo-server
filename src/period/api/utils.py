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


def school_holiday(acadmic_session):
    print("Called", acadmic_session)
    try:
        if SchoolHoliday.objects.filter(academic_session=acadmic_session).exists():
            holiday_list = SchoolHoliday.objects.filter(
                academic_session=acadmic_session)
            for holiday in holiday_list:
                print("HOLIDAY", holiday)
            return holiday_list

        else:
            print("NOT Exists")
            raise ValidationError("Holiday List Not Exist")

    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        print("Utils error", ex)
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
