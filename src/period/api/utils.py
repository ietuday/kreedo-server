import traceback

from django.core.serializers import serialize
from django.db.models import Q
from django.core.exceptions import ValidationError

import json
import pdb
from datetime import datetime, timedelta, date, time
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


class PeriodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'

    def create(self, validated_data):
        try:
            p_qs = Period.objects.filter(start_date=validated_data['start_date'], end_date=validated_data['end_date'],
                                         start_time=validated_data['start_time'], end_time=validated_data['end_time']).count()
            if p_qs == 0:
                print("###################", validated_data)
                data = super(PeriodCreateSerializer,
                             self).create(validated_data)
                return data
            else:
                print("ALready Created")
                return ValidationError("Alreday Created")

        except Exception as ex:
            print("ERROR", ex)
            print("@@@@@", traceback.print_exc())
            raise ValidationError(ex)


""" Get All List """


def school_holiday(grade_dict):

    try:
        if SchoolHoliday.objects.filter(holiday_from__gte=grade_dict['start_date'], holiday_till__lte=grade_dict['end_date'], academic_session=grade_dict['acad_session'], ).exists():
            school_holiday_count = SchoolHoliday.objects.filter(
                holiday_from__gte=grade_dict['start_date'], holiday_till__lte=grade_dict['end_date'], academic_session=grade_dict['acad_session']).count()

            return school_holiday_count

        else:
            print("Holiday List Not Exist")
            return 0

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
            day = calendar.day_name[(
                start_date + timedelta(days=i+1)).weekday()]
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
            print("response_data--->2", response_data)
            return response_data
        else:
            print("Weak-Off List Not Exist")
            return []

    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        raise ex


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


def create_period(grade, section, start_date, end_date, acad_session, period_template):
    try:
        grade_dict = {
            "grade": grade,
            "section": section,
            "start_date": start_date,
            "end_date": end_date,
            "acad_session": acad_session,
            "period_template": period_template
        }
        print(grade, section, start_date, end_date, acad_session)
        from_date = datetime.strptime(start_date, '%Y-%m-%d')
        to_date = datetime.strptime(end_date, '%Y-%m-%d')
        delta = to_date - from_date  # as timedelta
        print("grade",grade_dict)
        period_qs = PeriodTemplateToGrade.objects.filter(academic_session=acad_session,
                                                                         start_date=start_date, end_date=end_date,period_template = period_template )
        
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",period_qs)
        if period_qs:
            period_qs[0].period_status = "PENDING"
            period_qs[0].save()

        for i in range(delta.days + 1):
            day = from_date + timedelta(days=i)
            day_according_to_date = check_date_day(str(day.date()))
            week_off = weakoff_list(grade_dict)[0]
            day_according_to_date = day_according_to_date.lower()
            print(week_off)
            for key, value in week_off.items():
                if key == day_according_to_date and value == False:
                    schoolHoliday_count = SchoolHoliday.objects.filter(Q(holiday_from=day.date()) | Q(
                        holiday_from=day.date()), academic_session=acad_session).count()

                    if schoolHoliday_count == 0:
                        period_list = PeriodTemplateDetail.objects.filter(
                            day=day_according_to_date.upper(), period_template=period_template)
                        period_dict = {}

                        for period in period_list:
                            print(period)
                            # pdb.set_trace()
                            period_dict['period_template_detail'] = period.id
                            period_dict['academic_session'] = [acad_session]
                            period_dict['name'] = period.name
                            # period_dict['description'] =  period.subject.name
                            period_dict['subject'] = period.subject.id
                            period_dict['room'] = period.room.id
                            period_date = day.date()
                            period_time = period.start_time
                            period_dict['start_date'] = period_date
                            period_dict['end_date'] = period_date
                            period_dict['start_time'] = period.start_time
                            period_dict['end_time'] = period.end_time
                            period_dict['type'] = period.type
                            period_dict['is_active'] = True

                            p_qs = Period.objects.filter(start_date=period_dict['start_date'], end_date=period_dict[
                                                         'end_date'], start_time=period_dict['start_time'], end_time=period_dict['end_time'], period_template_detail=period.id, room=period.room.id).count()
                            if p_qs == 0:
                                period_serializer = PeriodCreateSerializer(
                                    data=period_dict)
                                if period_serializer.is_valid():
                                    period_serializer.save()

                                else:
                                    print("PERIOD-Serializer",
                                          period_serializer.errors)
                                    raise ValidationError(
                                        period_serializer.errors)
                            else:
                                print("Period Already Created")
        period_to_grade_qs = PeriodTemplateToGrade.objects.filter(academic_session=acad_session,
                                                         start_date=start_date, end_date=end_date,period_template = period_template)
        if period_to_grade_qs:
            period_to_grade_qs[0].is_applied = True
            period_to_grade_qs[0].period_status = "COMPLETE"
            period_to_grade_qs[0].save()

        return "Period Creating....."
    except Exception as ex:
        print(traceback.print_exc())
        period_qs = PeriodTemplateToGrade.objects.filter(academic_session=acad_session,
                                                                         start_date=start_date, end_date=end_date, period_template = period_template)
        if period_qs:
            period_qs[0].period_status = "FAILED"
            period_qs[0].save()

        logger.debug(ex)
        logger.info(ex)
        raise ValidationError(ex)


def check_date_day(date):
    day_name = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = datetime.strptime(date, '%Y-%m-%d').weekday()
    return day_name[day]


def get_seconds_removed(time):
    if time:
        time_list = time.split(":")
        time = ":".join(time_list[:2])
        return time
    else:
        return time


def validation_time_for_period_template_detail():
    try:
        print("@@@@@@@@")
    except Exception as ex:
        raise ValidationError(ex)
